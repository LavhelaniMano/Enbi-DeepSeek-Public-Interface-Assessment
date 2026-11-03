# Enbi and the CIA Triad

## Overview

The CIA Triad — **Confidentiality**, **Integrity**, and **Availability** — is the foundation of information security. This note applies each principle to the Enbi public-interface observation project: first to the way the study itself handles data and evidence, and second to the security properties a public banking assistant of this kind should uphold.

The observations here are limited to the public chat interface. They do not describe Nedbank's internal architecture, model configuration, access controls, or backend logging. Read the project's [final report](../docs/FINAL_REPORT.md) and the [adversarial observation report](../docs/ADVERSARIAL_OBSERVATION_REPORT.md) for the underlying evidence.

---

## Confidentiality

**Definition:** Ensuring that information is accessible only to authorised individuals and is protected from unauthorised access.

### How the project relates

The study deliberately avoids real customer data. Every run was entered by hand through the public webpage, with no login, no account session, and no real credentials. Adversarial prompts use synthetic values only — a `0000` PIN, `[dummy name]`, and an all-zero ID number. No response recorded in the logs disclosed account balances, transactions, or customer records.

That said, a public chatbot is still an untrusted data channel. A visitor may paste personal information without thinking, and the provider may log the conversation. For this project, the confidentiality questions are:

- **What is stored:** prompt text, verbatim response transcripts in `datasets/text/responses/`, screenshots in `tests/evidence/`, and CSV rows in `datasets/text/`.
- **Where it is published:** the repository is public, so any unredacted screenshot or transcript is effectively disclosed.
- **Who else sees it:** the DeepSeek comparison sends prompts to a third-party model provider, so the prompt text leaves the local machine.
- **What could leak indirectly:** screenshots may capture browser chrome, session identifiers, timestamps, or unrelated page content.

No real customer data was collected, but the Red Team proposal mentions synthetic canary records in its original design. Those were not used in the completed runs.

### How it can be enhanced

- **Data minimisation:** never submit real account numbers, card numbers, PINs, OTPs, ID numbers, or customer names. Keep using synthetic placeholders.
- **Redaction pass:** review every screenshot and transcript before committing. Crop browser chrome and blur any incidental identifiers.
- **Access control:** keep raw, unredacted captures in private storage and publish only redacted derivatives.
- **Retention limit:** define how long raw captures are kept and delete them once the report is finalised.
- **Encryption:** keep evidence on encrypted storage and transfer it over HTTPS only.
- **Provider review:** read the chatbot and model-provider privacy terms before sending anything sensitive; assume prompts may be retained or reviewed.
- **Treat the chat as public:** a public assistant should warn users not to share credentials, and should never ask for them.

---

## Integrity

**Definition:** Ensuring that data is accurate, complete, and has not been tampered with.

### How the project relates

The study's main integrity control is provenance. Each run has a prompt ID, a prompt file, a response transcript, a timestamp, and a row in a CSV. The benign and adversarial runs are kept in separate logs, and `datasets/text/test_log.csv` records a truncated SHA-256 hash of the prompt in `prompt_sha256`. Failed, boring, and excluded runs are retained rather than deleted, so the sample cannot be quietly improved after the fact.

The completed runs also exposed several integrity weaknesses:

- **Prompt-entry errors:** the chat box dropped the first character on P1, P5, S1, and S2. Those runs are invalid as exact-prompt runs and are marked for re-run.
- **Partial transcripts:** the P1 and P5 response texts are incomplete.
- **Incomplete captures:** the P5 screenshot shows the response but not the prompt, and the S2 screenshot is cropped at the bottom.
- **Model self-report:** in the DeepSeek comparison, P6 claimed to be "made by OpenAI" — a statement that conflicts with the logged provider and cannot be verified from the response alone.
- **Unverified specifics:** several responses contain rates, fees, hotline numbers, timeframes, and legal claims that were not checked against an official source. These are flagged in the assessment and notes columns rather than presented as facts.

### How it can be enhanced

- **Hash the evidence:** record SHA-256 hashes for response files as well as prompts, so a transcript can be checked against its log row.
- **Capture prompt and response together:** one screenshot per run showing both sides of the exchange, plus the timestamp and HTTP status.
- **Dual review:** compare each transcript with its screenshot before logging; a second reader is better.
- **Append-only corrections:** never rewrite a logged row. Add a correction row or note with the date and reason.
- **Separate observation from interpretation:** keep the raw response, the outcome summary, and the assessment in distinct columns.
- **Verify identity claims externally:** treat a model's self-description as untrusted output, not as metadata.
- **Version the dataset:** tag or checksum the CSV and transcript set at each reporting milestone.

---

## Availability

**Definition:** Ensuring that systems and data are accessible and operational when needed by authorised users.

### How the project relates

Enbi is a third-party service, so its availability is outside the study's control. The observation plan depends on the public page being reachable through an ordinary browser, at a low manual rate. Availability events recorded during the project include:

- One B1 run returned **HTTP 440** for a page resource while still showing the welcome menu. The cause was not established, and the event was recorded as a browser/resource error rather than chatbot content.
- Earlier scripted browser attempts also hit HTTP 440 and were excluded from the dataset.
- TOBi was rejected as a backup target because its public chat required a mobile number and SMS verification and then handed the conversation to a human agent.

If the service blocks, rate-limits, CAPTCHA-challenges, or changes its interface, collection stops. The study must not attempt to evade those controls. Locally, the evidence set is also a single point of failure if it is not backed up.

### How it can be enhanced

- **Record status, not just content:** log the HTTP status, timestamp, and visible error for every run. Mark failures `inconclusive`, never as missing data.
- **Keep a fallback target:** agree a second public chatbot in advance, with the same scope and stop conditions.
- **Back up the evidence:** keep a second copy of `datasets/text/`, `tests/evidence/`, and `tests/runs.pdf` outside the working machine.
- **Version the dataset:** use git tags or checksums so a lost or altered file can be detected.
- **Respect service limits:** low volume, manual entry, and an immediate stop on rate-limiting or blocking.
- **For a deployed assistant:** add monitoring and alerting, redundancy, graceful degradation to a human handoff, and rate limiting that protects availability without locking out legitimate customers.

---

## Summary

| CIA principle | Current state in this project | Recommended enhancement |
|---|---|---|
| Confidentiality | Public chat only; synthetic credentials; transcripts and screenshots stored in a public repo | Minimise data, redact captures, restrict raw evidence, set a retention limit |
| Integrity | Prompt hashes, separate logs, verbatim transcripts, excluded-run record; some entry errors and partial captures | Hash responses too, capture prompt and response together, dual review, append-only corrections |
| Availability | Third-party uptime; HTTP 440 observed; low-volume manual collection; local evidence only | Log status and timestamps, back up evidence, keep a fallback target, never evade limits |

Applying the CIA Triad makes the difference between a collection of screenshots and a defensible observation record. The project cannot certify Enbi's security, but it can protect the people whose data is discussed, keep its own evidence trustworthy, and stay honest about the conditions under which the observations were made.
