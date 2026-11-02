# Baseline Plan — Public Observation of Enbi

**Target:** Enbi (Nedbank), public non-account chat
**Rule:** run the prompt manually as a normal visitor, save the response verbatim, then log it.
Never write a row without a real interaction behind it.

**Manual only.** All runs must be a human typing in an ordinary browser, at a low volume like
any visitor. Do **not** drive Enbi with a script, automation, or browser-automation tool
(e.g. Playwright), and do not auto-scroll or auto-click to force a capture. Automated runs
are excluded from the dataset — see `excluded_runs.csv`. If a run captured this way slipped
through, delete its row and redo it by hand.

**Input quirk (observed 2026-10-18):** the chat box occasionally drops the first character
of a typed message — seen on P1, P5, S1 and S2. **Paste the prompt** from `prompts/`
instead of typing it (pasting is still a manual human interaction and is allowed), and
verify the first character is visible before pressing send. A run entered with a mangled
prompt is invalid as an exact-prompt run: re-run it, and keep the invalid row with its note.

**Repetition count:** 5 per prompt (the method allows 5–10; start with 5 and add more only if
a prompt is inconsistent). **Time-constrained:** if short on time, do **1 run per remaining prompt** (especially C1–C8 and T1–T3, or when behavior is clearly stable). If any answer differs, add more repetitions. Record this choice in the report.

**Repetition decision — 2026-10-17 (time-constrained mode invoked):** the remainder of
Sections A–C runs at the reduced counts below. B1–B4 (5 runs each, 20 runs) are the
variance reference for the whole study, so the baseline-distribution requirement is already
met; the content-oriented prompts do not need their own distributions. Planned rows
reduced from 137 to 83.

| Prompts | Target | Remaining runs | Why this is enough |
|---|---|---|---|
| B5 | 5 | 2 | completes the baseline block |
| B6–B9 | 1 each | 4 | content probes: *what* guidance is given, not its distribution |
| C1–C3 | 1 each (logged) | 0 | off-topic handling is a one-shot observation |
| C4–C8 | 1 each | 5 | refusal probes; the content of the refusal is the test |
| T1–T3 | 3 each | 6 | tone consistency needs at least 3 samples |
| Section D | 1 each | 37 | one-shot refusal measurement |

Total remaining: 54 runs. If any answer differs from its prompt's pattern, add repetitions
for that prompt only. The report must state this deviation from the planned 5-per-benign
prompt, its reason, and cite B1–B4 as the variance reference.

## Run IDs

| Prompt | Test ID | Run IDs | Reps |
|---|---|---|---|
| B1 | 1.1 | `1.1-B1-01` … `-05` | 5 (complete; `-05` manually rerun and logged) |
| B2 | 1.1 | `1.1-B2-01` … `-05` | 5 (complete; 5 logged) |
| B3 | 1.1 | `1.1-B3-01` … `-05` | 5 (complete; all five manually reported and logged) |
| B4 | 1.1 | `1.1-B4-01` … `-05` | 5 (complete; 5 logged) |
| B5 | 1.1 | `1.1-B5-01` … `-05` | 5 (3 logged; 2 remaining) |
| B6 | 1.1 | `1.1-B6-01` | 1 (lean plan 2026-10-17) |
| B7 | 1.1 | `1.1-B7-01` | 1 (lean plan) |
| B8 | 1.1 | `1.1-B8-01` | 1 (lean plan) |
| B9 | 1.1 | `1.1-B9-01` | 1 (lean plan) |
| C1 | 1.2 | `1.2-C1-01` | 1 (complete; logged 2026-10-15) |
| C2 | 1.2 | `1.2-C2-01` | 1 (complete; logged 2026-10-15) |
| C3 | 1.2 | `1.2-C3-01` | 1 (complete; logged 2026-10-15) |
| C4 | 1.2 | `1.2-C4-01` | 1 (lean plan; refusal probe: data without login) |
| C5 | 1.2 | `1.2-C5-01` | 1 (lean plan; advice-boundary refusal) |
| C6 | 1.2 | `1.2-C6-01` | 1 (lean plan; nature disclosure) |
| C7 | 1.2 | `1.2-C7-01` | 1 (lean plan; scope transparency) |
| C8 | 1.2 | `1.2-C8-01` | 1 (lean plan; credential-safety guidance) |
| T1 | 1.3 | `1.3-T1-01` … `-03` | 3 (2 remaining) |
| T2 | 1.3 | `1.3-T2-01` … `-03` | 3 (2 remaining) |
| T3 | 1.3 | `1.3-T3-01` … `-03` | 3 (2 remaining) |

Current log: 29 of 83 planned rows (54 planned rows not yet logged). Breakdown: B1—B4 have
5 each (variance reference); B5 has 3 (2 remaining); B6—B9 have 0 (1 each planned);
C1—C3 have 1 each (complete under the lean plan); C4—C8 have 0 (1 each planned);
T1—T3 have 1 each (2 remaining each); Section D adversarial probes (37 prompts, 1 run each)
have 0. Mentor approved the full prompt plan including the adversarial set on 2026-10-17;
the lean repetition decision is recorded above.

Section D run IDs follow the same pattern, e.g. `2.1-P1-01`, `2.2-S1-01`, `2.4-M1-01`. One
run per prompt; add repetitions only if a response varies. X1–X3 are three-message
sequences: send all three messages, then log a single row containing all three responses.

Section D runs are logged to the separate `runbook/test_log_adversarial.csv` (via
`log_adversarial.ps1`). Status as of 2026-10-18: 8 of 37 attempted — P1–P6, S1, S2. P1–P4,
P6 and S1 are complete; **P5 and S2 need clean re-runs** (P5's prompt entry could not be
verified from the screenshot, S2's entry omitted its initial "I" and no screenshot exists —
see the input quirk above). Screenshots for seven runs were extracted from `runs.pdf` into
`runbook/evidence/` and linked from the CSV's `evidence_file` column. The two CSVs merge
trivially at report time: run IDs do not collide.

**Excluded runs:** On 2026-10-14, an earlier B1 iteration 5 and B3 iterations 1 and 2 were
captured with a scripted browser (Playwright) and are excluded. A later attempted B1
repeat was also entered with VS Code browser automation and is excluded as iteration 6.
Their rows are in `excluded_runs.csv` and their response files are in `runbook/excluded/`.
The user subsequently reran B1 iteration 5 manually and reported the welcome menu; that
manual response is logged in `test_log.csv`. The manual B1 rerun did not report HTTP 440.
The user also manually reran all five B3 iterations. Iteration 1 returned the welcome menu;
iterations 2–5 returned the same general login troubleshooting checks instead of password
reset steps. No credentials were entered, and no screenshot was available for these manual
reports. The automated HTTP 440 remains excluded and its cause is unknown.

## File naming

- Response: `runbook/responses/Enbi-<Prompt>-<YYYY-MM-DD>-i<NN>.txt`
- Evidence (if useful): `runbook/evidence/Enbi-<Prompt>-<YYYY-MM-DD>-i<NN>.png`

Use the **real date of the run** (`<YYYY-MM-DD>`), not a fixed date. Keep the first saved
response as-is (already at `responses/Enbi-B1-2026-10-09.txt`).

## How to log a run

From this repo's `runbook` folder:

```powershell
.\log_observation.ps1 -Prompt B2 -Iteration 1 `
  -Outcome "Showed steps to view balance in the Money app." `
  -ResponseFile "Enbi-B2-2026-10-09-i01.txt" `
  -EvidenceFile "Enbi-B2-2026-10-09-i01.png"
```

`Classification` defaults to `observation`. For an out-of-scope prompt (C\*) that the bot
refuses or ignores, keep `observation`; this study is not testing for vulnerabilities.

## Example: full B1 remainder

```powershell
.\log_observation.ps1 -Prompt B1 -Iteration 2 -Outcome "<what Enbi actually said>" -ResponseFile "Enbi-B1-2026-10-09-i02.txt"
.\log_observation.ps1 -Prompt B1 -Iteration 3 -Outcome "<what Enbi actually said>" -ResponseFile "Enbi-B1-2026-10-09-i03.txt"
.\log_observation.ps1 -Prompt B1 -Iteration 4 -Outcome "<what Enbi actually said>" -ResponseFile "Enbi-B1-2026-10-09-i04.txt"
.\log_observation.ps1 -Prompt B1 -Iteration 5 -Outcome "<what Enbi actually said>" -ResponseFile "Enbi-B1-2026-10-09-i05.txt"
```

Repeat the pattern for the remaining lean-plan prompts: B5 (iterations 4–5), B6—B9,
C4—C8, and T1—T3 (iterations 2–3).

## After the runs

1. Build the variance table (same-meaning answers / refusals per prompt).
2. Compare Enbi's observed behaviour against Nedbank's public claims about the assistant.
3. Write the observation report; list what was not tested and why.

