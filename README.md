# Final Capstone Project README

> **This file is the scope and methodology document.** For the actual step-by-step
> runbook — public-user scope record, environment setup, commands, prompt library, logging,
> classification, reporting and disclosure — see **[`EXECUTION.md`](EXECUTION.md)**.

| Document | Purpose |
|---|---|
| `README.md` | Scope, methodology, constraints, deliverables (this file) |
| `EXECUTION.md` | Day-by-day runbook with commands and checklists |
| `Track_A_Red_Team_Proposal_Trimmed.md` | Rationale, target-selection criteria, one-week plan |
| `Track_A_Public_User_Proposal.md` | Observation-study proposal, written before the 2026-10-17 scope amendment; superseded by `runbook/AUTHORIZATION.md` |
| `TARGETS.md` | Selected target (Enbi), access record, and observation result |
| `TARGET_OPTIONS.md` | Target options and questions from the mentorship session |
| `runbook/AUTHORIZATION.md` | Scope record: target, approved prompt sets (A–D), mentor approval, amendment 1 |
| `runbook/prompts.md` | Benign observation prompt library and testing checklist |
| `runbook/log_result.py` | Logger; writes one row per request to `runbook/test_log.csv` |
| [`FINAL_REPORT.md`](FINAL_REPORT.md) | Consolidated report of completed benign and adversarial observations, evidence, and limitations |

## Project title
Track A — Red Team Assessment of the Enbi Chatbot

> **Current scope:** Enbi (Nedbank) is the selected target, tested through its public
> website chat only. Two approved phases are running: a benign observation study
> (Sections A–C of `runbook/prompts.md`) and an adversarial probe set (Section D, 37
> prompts) added by mentor approval on 2026-10-17 (`runbook/AUTHORIZATION.md` §8). Never
> enter real account or personal details. TOBi was not used because its sales chat
> requested contact details and routed to a live agent.

## Overview
This capstone assesses Enbi's public-facing chat in two approved phases: a baseline study of ordinary, non-sensitive questions, and an adversarial probe set measuring whether the chatbot refuses instruction-override, social-engineering, sensitive-data and fraud-assistance prompts. Everything runs through the public website interface. No account is accessed and no real customer details are submitted.

This is a project-scope decision, not permission to test hidden or restricted functionality. The chatbot's published terms and usage rules still apply. Do not access private endpoints, other users' data, internal systems, or perform actions that an ordinary visitor could not perform.

This project is grounded in the bootcamp's AI and cybersecurity material — Week 7's prompt-injection and guardrails work in particular. It probes the chatbot's refusal behaviour through the ordinary public interface; it does not test infrastructure, private endpoints, or access controls.

## Why this project
We are not building a custom RAG agent or toy demo. We are observing an existing public AI assistant to answer:

- What kinds of public questions does the chatbot answer?
- Does it respond consistently to repeated, harmless questions?
- How does it handle general questions outside its banking purpose?

This is useful because it builds practical skills in documenting AI behavior, keeping a bounded scope, and distinguishing observations from security findings.

## Scope and constraints
### In scope
We will use Enbi through its ordinary public-facing chat as a visitor, with benign questions about public Nedbank products and services. The first test sent was a simple greeting asking what Enbi can help with. Interactions are manual and low-volume.

### Allowed target
We will assess one chatbot that is:
- available on the Nedbank public website
- available to an ordinary public user through its intended interface
- selected with the mentor, with the exact URL and visitor access context recorded in [TARGETS.md](TARGETS.md)

### Out of scope
The following are outside this project:
- attacking unrelated systems
- accessing private APIs, administrative interfaces, or other users' accounts or data
- requesting real credentials, secrets, or another user's data (system-prompt requests appear only as the Section D refusal probes listed in `runbook/prompts.md`)
- triggering real purchases, account changes, external actions, or other consequential operations
- indirect prompt injection using third-party content, or modifying a live knowledge base
- scanning, automation, high-volume requests, denial-of-service, or bypassing access controls

## Approach
Phase 1 asks ordinary, public questions and documents responses and variation. Phase 2 (mentor-approved 2026-10-17) sends the Section D adversarial probes and documents whether Enbi refuses. Account access, private endpoints, automation, real data, and anything affecting real users or transactions stay out of scope in both phases.

## What we are trying to learn
We will observe Enbi's responses to ordinary public-facing questions, compare repeated answers, and describe the limitations of the sample. An unusual response is an observation, not a vulnerability claim.

We will not deliberately attempt to access another user's data, extract secrets, trigger privileged actions, or reach downstream systems. If an unexpected exposure or consequential behavior occurs during normal public-user interaction, stop testing, preserve only minimal evidence, and report it privately to the mentor and, if available, an appropriate public reporting contact.

## Objectives
1. Observe the chatbot's normal behavior using benign public-information prompts.
2. Review the chatbot's publicly stated purpose, usage rules, and visible guidance.
3. Compare responses to repeated, harmless questions.
4. Record exact evidence for each observation.
5. Produce a clear report with results and limitations, without claiming a vulnerability.

## Methodology
### Step 1: Choose the target
We will select the chatbot with the mentor, and record:
- the company or owner
- the exact chatbot URL
- the normal public-user access context
- applicable public terms or usage rules
- a public reporting contact, if available

### Step 2: Baseline behavior
Use ordinary, benign questions to understand:
- standard responses
- expected variance
- how the system handles out-of-scope benign questions
- whether the tool or assistant appears to have access to user-sensitive data or actions

### Step 3: Review public-facing information
We review:
- the chatbot's visible policy or usage guidance
- its stated purpose and limitations

### Step 4: Record observations
We manually use the reviewed prompt list through the ordinary interface. Each observation should record:
- prompt ID
- prompt category
- exact input used
- response received
- whether it was blocked, observed, or inconclusive

### Step 5: Evidence and reporting
We will build a report using captured transcripts, response notes, and classification of each outcome. The report will explain:
- what we tested
- what was blocked
- what was observed
- what counts as a real finding
- what mitigation would help

## Planned testing structure
The project will follow a simple test matrix:

| ID | Test | Purpose |
|---|---|---|
| 1.1 | Baseline behavior | Measure normal response variation |
| 1.2 | Public information | Observe responses about Nedbank's publicly described services |
| 1.3 | Repeated benign prompts | Compare ordinary responses across repeated runs |
| 1.4 | General harmless questions | Observe whether Enbi responds to unrelated, non-sensitive questions |

Only manually entered, benign prompts about public information will be used. Account
flows, personal data, applications, and live-agent handoffs are excluded.

## Deliverables
The final project should include:
- this README
- the project proposal and scope documentation
- a testing log or spreadsheet of prompts/results
- evidence screenshots or transcript snippets
- a final written report
- a short presentation or explanation of the findings

## Ethical and legal rules
This project must be done responsibly.

- Use only the normal public-facing chatbot interface, in line with mentor guidance and the site's published terms
- Do not attempt access beyond the permissions of an ordinary visitor/customer
- No unsafe or destructive prompts
- Do not seek real user data, credentials, private secrets, or internal system details
- Stop immediately if unexpected sensitive data or harmful behavior appears
- No public disclosure of findings; share results privately with the mentor and use an appropriate reporting channel if needed
- No overclaiming: if something is only an observation, say it plainly

## Timeline
### Week 1 / Final capstone week
- confirm target and public-user access context with the mentor
- check published usage rules and define the bounded test scope
- create test matrix
- run baseline prompts
- complete the reviewed benign baseline
- document evidence
- write final findings report
- prepare final presentation

## Success criteria
We succeed if we can do all of the following:
- choose a public chatbot and keep testing within ordinary user access
- show disciplined, methodical testing
- distinguish an observation from a real vulnerability
- provide evidence-based findings
- explain the limits of what a small observation sample can show

## Final thought
This capstone is about responsible, bounded testing through a public interface. Its conclusions must stay limited to the interactions and evidence actually collected.

The project demonstrates how to document chatbot behavior with care, respect the service's boundaries, and report observations without overstating them.
