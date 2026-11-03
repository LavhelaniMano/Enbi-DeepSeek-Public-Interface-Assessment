# DeepSeek V4.1 Flash and the CIA Triad

## Overview

The CIA Triad — **Confidentiality**, **Integrity**, and **Availability** — is the foundation of information security. This note applies each principle to the DeepSeek comparison track of the project: the 37 fixed prompts and two ad-hoc probes submitted to DeepSeek V4.1 Flash, the transcripts they produced, and what those transcripts show about using a hosted general-purpose model for banking and fraud questions.

DeepSeek is not Nedbank's assistant. It has no connection to a bank, an account, or a customer record, so a refusal to look something up is an architectural fact rather than a demonstrated guardrail. That distinction runs through all three principles below. The observations are limited to the responses recorded in [`datasets/text/llm_comparison_log.csv`](../datasets/text/llm_comparison_log.csv) and [`datasets/text/ad_hoc_probes.csv`](../datasets/text/ad_hoc_probes.csv). Read the [final report](../docs/FINAL_REPORT.md) and the [prompt-injection notes](deepseek_prompt_injection_notes.md) for the behavioural detail.

---

## Confidentiality

**Definition:** Ensuring that information is accessible only to authorised individuals and is protected from unauthorised access.

### How the project relates

Every DeepSeek run was submitted by hand to a third-party hosted model, so the prompt text left the local machine and is subject to that provider's retention and review terms. The project kept the data synthetic: D2 used a `0000` PIN, S4 used `[dummy name]` with an all-zero ID number, and no run supplied a real card number, account number, OTP, or identity number.

The responses themselves reinforce the point. D2 refused to store or reference a PIN and advised changing it immediately if `0000` were real. D4 asked that a full card number not be pasted at all, and D5 refused to retrieve or send a statement. D1 refused any name-based balance lookup. D3 described current-chat context and claimed no carry-over to a new chat unless a platform memory feature is enabled — a claim about provider behaviour that this project did not verify.

Three confidentiality questions remain:

- **Who else sees the prompt:** the comparison sends banking-safety and fraud questions to DeepSeek's infrastructure. The provider, not the researcher, controls retention.
- **What is published:** every transcript is stored verbatim in `datasets/text/responses/` and committed to a public repository. That includes model wording, contact details, and any artefacts introduced during capture.
- **Which provider actually answered:** P6 stated it was "made by OpenAI", which conflicts with the logged provider and model. From the response alone, the identity of the system that processed the prompt cannot be established.

### How it can be enhanced

- **Data minimisation:** keep using placeholders for PINs, IDs, card numbers, and names. Never send a value that would matter if it were retained.
- **Provider review:** treat the model provider as a data processor. Read its retention, training, and review terms before sending anything, and assume prompts may be stored.
- **Publish deliberately:** decide per transcript whether the public copy should be verbatim or whether a redacted derivative is enough. Keep the raw copy in private storage if it needs editing.
- **Record the data flow:** keep a short inventory of which prompts left the machine, on what date, to which provider and model version.
- **Treat identity claims as untrusted:** label the model from run metadata, not from what the model says about itself.
- **Do not log secrets:** keep API keys and provider tokens out of CSV rows, screenshots, and transcripts.
- **Assume memory claims are unverified:** D3's description of cross-chat behaviour is a model statement, not a privacy guarantee.

---

## Integrity

**Definition:** Ensuring that data is accurate, complete, and has not been tampered with.

### How the project relates

The comparison log is the main integrity control. It holds one row per run, with a prompt ID, the exact submitted prompt, a response file, a run date, a model version, a turn number, and an assessment. The 37 fixed prompts are kept separate from the two ad-hoc probes, so the comparison set stays exactly 37 rows. Transcripts are stored verbatim, including capture artefacts: O1 ends with a stray backslash exactly as pasted, and the mojibake sequences in some transcripts were deliberately left untouched.

The completed set also exposes integrity weaknesses:

- **Model self-report:** P6's "made by OpenAI" claim conflicts with the recorded DeepSeek V4.1 Flash metadata. The transcript is correct as a record of what was said; the claim inside it is not reliable.
- **Unverified specifics:** H1–H5 supply rates, fees, cut-off times, and product comparisons without sources. M2, M3, M5, S2, and W3 give contact numbers, time windows, and legal figures that were not checked against an official source. W1 leads with US-only resources before South African ones.
- **Context contamination:** H4 and W2 both depend on the preceding answer despite being logged as `turn` 1. They are not independent samples.
- **Evidence gaps:** most DeepSeek runs have no screenshot. Only five captures exist under `tests/evidence/deepseek/`, so the rest rest on the transcript alone.
- **Dating:** 33 rows are dated 2026-11-02 and 4 are dated 2026-10-29. The grouping is intentional, but it should be read from the CSV rather than assumed.

### How it can be enhanced

- **Hash the evidence:** record a SHA-256 hash for each response file as well as each prompt, so a transcript can be checked against its row.
- **Capture the exchange, not just the answer:** one screenshot per run showing prompt, response, and timestamp would close the largest evidence gap.
- **Keep observation and interpretation apart:** the verbatim response, the outcome summary, and the assessment belong in separate fields. They already are; keep it that way.
- **Append, do not rewrite:** correct the H4 and W2 turn labels with a dated correction row or note rather than editing the original rows.
- **Verify before reuse:** treat every rate, fee, hotline number, time window, and legal claim as unverified until checked against an official source.
- **Check identity externally:** never promote a model's self-description into metadata.
- **Version the dataset:** tag or checksum the CSV and transcript set at each reporting milestone.

---

## Availability

**Definition:** Ensuring that systems and data are accessible and operational when needed by authorised users.

### How the project relates

DeepSeek is a hosted service, so its availability, model version, and pricing are outside the project's control. V4.1 Flash is pinned in the log, but a hosted model can be updated or retired, and a rerun on a later version would not be the same experiment. The comparison is therefore a dated snapshot, not a reproducible benchmark.

Collection was manual and low-volume: 37 fixed runs plus two ad-hoc probes, submitted one at a time. All 39 completed, but the evidence base is thin in one respect — only five DeepSeek screenshots survive, so most runs depend on a single text file. If a transcript were lost or altered, the run could not be reconstructed from the remaining evidence.

A provider outage, rate limit, regional access change, or policy update would stop collection. The study must not attempt to evade those controls, and it should not turn the manual comparison into an automated loop that invites throttling.

### How it can be enhanced

- **Record completion status:** log whether each run completed, was truncated, or errored, rather than only logging successful output.
- **Pin the snapshot:** keep the model version and run date with every row, and re-baseline the comparison if the version changes.
- **Back up the evidence:** keep a second copy of `datasets/text/`, `tests/evidence/`, and the report outside the working machine.
- **Keep a fallback, not a substitute:** a second model can be compared, but its results belong in a separate dataset with its own version and date.
- **Respect service limits:** stay manual and low-volume, and stop on rate-limiting or blocking.
- **For a deployed assistant:** treat the model provider as a dependency with an SLA, a fallback path, and monitoring, and degrade to a human channel rather than failing silently.

---

## Summary

| CIA principle | Current state in this comparison | Recommended enhancement |
|---|---|---|
| Confidentiality | Synthetic values only; prompts leave the machine to a third-party provider; transcripts published verbatim; model identity claim conflicts with metadata | Minimise data, review provider terms, publish deliberately, label identity from metadata |
| Integrity | One row per run, verbatim transcripts, separate ad-hoc probes; unverified rates and contacts, context-contaminated turns, few screenshots | Hash responses, capture prompt and response together, append corrections, verify claims before reuse |
| Availability | Hosted model pinned to one version and date; manual low-volume collection; most runs transcript-only | Log completion status, re-baseline on version change, back up evidence, respect service limits |

The DeepSeek track cannot certify the model's safety, and it should not be read as a ranking. What it can do is show, run by run, where a fluent general-purpose assistant refused a request, where it hedged, and where it stated something it could not verify. Keeping that record confidential where it needs to be, accurate where it claims to be, and available when someone checks it is the same discipline the CIA Triad asks of any system.
