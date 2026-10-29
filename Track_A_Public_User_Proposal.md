# Track A — Public Observation Study of Enbi (Nedbank)

**Project:** Observe the normal public behaviour of one South African AI chatbot
**Track:** Track A — Red Team (test and report on an AI application)
**Method:** Ordinary public-user interaction only — no adversarial testing
**Target:** Enbi (Nedbank), public website chat
**Status:** Updated to reflect the observation-only scope agreed with the mentor

## 1. Project Scope

I will interact with Enbi as an ordinary website visitor, using only the same access any
member of the public has. The goal is to describe how the chatbot behaves in normal use:
what it answers, how it refuses, how consistent it is, and how that behaviour compares with
the company's own public statements about the assistant.

This study is **observational**. I will not send prompts that try to override the
chatbot's instructions, extract its system prompt or secrets, reach another user's data,
trigger an action, or probe how the application handles its output. Those are security
tests, not public use, and they are out of scope for this engagement.

Out of scope:

- Prompt injection or jailbreak attempts of any kind
- System-prompt, configuration, or secret extraction
- Cross-user data access, account actions, purchases, or any real-world side effect
- Indirect injection, knowledge-base changes, or output-sink/rendering tests
- Automation, scanning, or high-volume requests

## 2. Target

Primary: **Enbi (Nedbank)**, public website chat interface. No Nedbank ID, Money app,
Online Banking, or account feature will be used. TOBi (Vodacom) is the backup candidate,
but its sales chat requested contact details and routed to a live agent, so it was not
used. Details are recorded in [`TARGETS.md`](TARGETS.md).

Before starting I will confirm the exact public URL is reachable and read the published
terms and usage rules.

## 3. Objectives

1. Establish normal behaviour using benign baseline questions the chatbot is designed to answer.
2. Measure response variance by repeating each question several times.
3. Observe how the chatbot handles harmless out-of-scope questions and how it refuses.
4. Compare observed behaviour against the company's public claims about the assistant.
5. Document everything accurately and label observations as observations, not findings.

## 4. Method and Evidence

1. Open the chatbot in a normal browser as a visitor.
2. After mentor review, send the benign prompts in `runbook/prompts.md` (Section A) five times each, at a low manual rate.
3. Save the prompt, the verbatim response, and a timestamp for every run.
4. Screenshot where useful; redact anything sensitive.
5. Record refusals, response variance, and visible behaviour without guessing at hidden implementation.
6. Stop if sensitive data appears unexpectedly, the service objects, or the next step would
   require more than ordinary public access.

Deliverables: an observation log, saved responses, a short behaviour comparison, and a final
report that states the limitations plainly.

## 5. Rules of Engagement

- One named chatbot, through the ordinary public interface only.
- Ordinary, non-sensitive questions only. No instruction-override or extraction attempts.
- No personal data, credentials, or anything private submitted.
- No purchases, account changes, or real-world actions.
- Manual and low-volume only. No automation, scanning, or load.
- Keep prompts and results private; share with the mentor first.

## 6. Reporting Standard

A response that is surprising or inconsistent is an **observation**, not a vulnerability.
This study does not attempt to demonstrate impact and will not claim a vulnerability. If
sensitive data or a real-world effect appears unexpectedly, I will stop, capture minimal
evidence, and report it privately rather than repeat it.

## 7. Limitations

- Public observation shows behaviour, not security posture; it cannot test guardrails adversarially.
- No insight into the model, retrieval sources, or private configuration.
- A small prompt set is a behaviour sample, not an audit.
- Results vary between runs; unsuccessful and inconclusive runs are included.
- Adversarial prompt-injection testing is out of scope and is not attempted.

## 8. Timeline

| Day | Work |
|---|---|
| 1 | Confirm Enbi's public URL and usage rules; record in `TARGETS.md`; capture baseline |
| 2 | Run the benign baseline set; save every response verbatim |
| 3 | Repeat and measure variance; add benign out-of-scope questions |
| 4 | Compare behaviour with public claims about the assistant |
| 5 | Draft the observation report |
| 6–7 | Mentor review; prepare the presentation |

## 9. Conclusion

This capstone applies AI red-team concepts through a bounded, observational public-user
study of Enbi. It stays entirely within the chatbot's normal public interface and published
usage rules, records behaviour honestly, includes unsuccessful runs, and makes no claim of
a vulnerability. Adversarial prompt-injection testing is deliberately excluded; if it is
ever pursued, it belongs to a separate, authorized engagement.
