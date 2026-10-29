#!/usr/bin/env python3
"""Append one row per request to the Track A test log.

One row = one individual request/response pair. Failed and boring requests get
logged too; a selective log is not evidence.

Usage:
    python log_result.py --test-id 1.3 --prompt-id V1 --run-id 1.3-V1-01 \
        --iteration 1 --outcome "Refused to change role." \
        --blocked blocked --classification observation \
        --guardrail "generic refusal template" \
        --notes "Full response in responses/1.3-V1-01.txt"
"""

import argparse
import csv
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

FIELDS = [
    "run_id",
    "test_id",
    "prompt_id",
    "prompt_file",
    "prompt_sha256",
    "iteration",
    "ts_utc",
    "account_context",
    "response_file",
    "outcome_summary",
    "guardrail",
    "axis1_blocked",
    "axis2_classification",
    "outcome_crossed",
    "evidence_file",
    "notes",
]

AXIS1 = {"blocked", "not-blocked", "inconclusive", "not run"}
AXIS2 = {"finding", "observation", "inconclusive", "not run"}
BOUNDARY_OUTCOMES = {"1", "2", "3", "4", "5", ""}

HERE = Path(__file__).resolve().parent


def resolve_ref(value: str, *subdirs: str) -> str:
    """Accept a bare filename and place it under a runbook subdirectory."""
    if not value:
        return ""
    candidate = HERE.joinpath(*subdirs, value)
    if candidate.exists():
        return candidate.relative_to(HERE).as_posix()
    return value


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-id", required=True, help="Unique id, e.g. 1.3-I1-01")
    p.add_argument("--test-id", required=True, help="1.1 - 1.4")
    p.add_argument("--prompt-id", required=True, help="e.g. B1, R1, V1, F1")
    p.add_argument("--prompt-file", default="", help="Filename in runbook/prompts/ or full text")
    p.add_argument("--iteration", type=int, default=1)
    p.add_argument("--account-context", default="anonymous")
    p.add_argument("--response-file", default="", help="Filename in runbook/responses/")
    p.add_argument(
        "--log-file",
        default="test_log.csv",
        help="CSV filename in the runbook directory (default: test_log.csv)",
    )
    p.add_argument("--outcome", required=True, help="Short summary of what came back")
    p.add_argument("--guardrail", default="", help="Guardrail message or refusal type, if visible")
    p.add_argument(
        "--blocked",
        default="",
        choices=sorted(AXIS1),
        help="Axis 1: what the guardrail did",
    )
    p.add_argument(
        "--classification",
        default="",
        choices=sorted(AXIS2),
        help="Axis 2: finding or observation",
    )
    p.add_argument(
        "--outcome-crossed",
        default="",
        choices=sorted(BOUNDARY_OUTCOMES - {""}),
        help="Trust-boundary outcome 1-5, only if classification=finding",
    )
    p.add_argument("--evidence-file", default="", help="Screenshot in runbook/evidence/")
    p.add_argument("--notes", default="")
    args = p.parse_args()

    if args.classification == "finding" and not args.outcome_crossed:
        p.error("--classification finding requires --outcome-crossed (1-5)")
    if args.outcome_crossed and args.classification != "finding":
        p.error("--outcome-crossed requires --classification finding")

    prompt_ref = args.prompt_file
    prompt_hash = ""
    if prompt_ref:
        prompt_path = HERE / "prompts" / prompt_ref
        if not prompt_path.exists():
            prompt_path = HERE / prompt_ref
        if prompt_path.exists():
            prompt_ref = prompt_path.relative_to(HERE).as_posix()
            prompt_hash = sha256_of(prompt_path.read_text(encoding="utf-8"))
        else:
            prompt_hash = sha256_of(args.prompt_file)

    row = {
        "run_id": args.run_id,
        "test_id": args.test_id,
        "prompt_id": args.prompt_id,
        "prompt_file": prompt_ref,
        "prompt_sha256": prompt_hash,
        "iteration": args.iteration,
        "ts_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "account_context": args.account_context,
        "response_file": resolve_ref(args.response_file, "responses"),
        "outcome_summary": args.outcome.replace("\n", " ").strip(),
        "guardrail": args.guardrail.replace("\n", " ").strip(),
        "axis1_blocked": args.blocked,
        "axis2_classification": args.classification,
        "outcome_crossed": args.outcome_crossed,
        "evidence_file": resolve_ref(args.evidence_file, "evidence"),
        "notes": args.notes.replace("\n", " ").strip(),
    }

    log_path = HERE / args.log_file
    if log_path.parent.resolve() != HERE.resolve():
        p.error("--log-file must be a filename in the runbook directory")
    is_new = not log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(row)

    print(f"logged {row['run_id']}  ->  {log_path.name}")
    if not row["axis1_blocked"] or not row["axis2_classification"]:
        print("  note: axes not both set. Classify before the report is written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
