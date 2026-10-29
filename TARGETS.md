# Target Record — Track A (Public Observation)

## Scope of this record

This capstone assesses a single chatbot through its normal, intended public interface. It has two phases: a **public observation study** (how the chatbot behaves for an ordinary visitor) and, since the mentor approval of 2026-10-17, an **adversarial probe set** (`runbook/prompts.md` Section D — instruction-override, social-engineering, sensitive-data-handling, fraud-assistance, obfuscation, overclaiming, safety and multi-turn prompts; see `runbook/AUTHORIZATION.md` §8).

No prompt accesses another user's data, triggers a real action, or reaches beyond the public page. Real credentials, secrets, automation and account actions remain out of scope.

## Selected target

| Field | Value |
|---|---|
| Chatbot | **Enbi** |
| Owner / service | Nedbank (South Africa) |
| Entry point | `https://personal.nedbank.co.za/contact/Enbi-chat.html` |
| Access context | Ordinary website visitor; public webpage; no login, no customer details |
| Role | Primary target |

**Why Enbi, not TOBi:** TOBi hands the conversation over to a human agent, so a public
visitor does not get a stable, self-contained chatbot session to observe. Enbi answers
public questions directly without an immediate hand-off, which suits an observation study.

## Backup target

| Chatbot | Owner / service | Notes |
|---|---|---|
| TOBi / SuperTOBi | Vodacom (SA) | Public chat currently asks for a mobile number and SMS verification before use. On 2026-10-09, the user reported that after they provided a number and email it transferred to a human agent. That handoff was not re-enacted for this observation. Current entry screenshot: `runbook/evidence/TOBi-public-phone-required-2026-10-14.png`. |

## TOBi public-entry observation (2026-10-14)

The public TOBi sales-chat page displayed a “Welcome to TOBi” prompt requesting a mobile
number, with a Continue button and notice that continuing agrees to receive an SMS
verification code. No number was entered and no Continue action was taken during this
capture. See `runbook/responses/TOBi-public-entry-2026-10-14.txt` and
`runbook/evidence/TOBi-public-phone-required-2026-10-14.png`.

The separate live-agent handoff is user-reported from 2026-10-09, after the user supplied
their own contact details. There is no screenshot of that handoff in this evidence set;
it was not repeated because it would require submitting contact information and accepting
SMS verification again.

## Other candidates (for reference)

| # | Chatbot | Owner / service |
|---|---|---|
| 1 | Batho Pele AI Chatbot | DPSA / public service |
| 2 | Chat.co.za | Chat.co.za |
| 3 | Chatbotz / chatbot.co.za | Chatbotz |
| 4 | ChatBunny | ChatBunny.org; attempted public access on 2026-10-14, but the page failed to render and `/signup` returned 404. No registration was completed. See `runbook/responses/ChatBunny-public-access-2026-10-14.txt`. |

## Selection checks (reading only — completed before testing began)

- [x] Enbi's public chat is reachable by an ordinary visitor (captured 2026-10-09).
- [x] The exact public chatbot URL is recorded below.
- [ ] Enbi's published terms and usage rules have been read and recorded.
- [x] The planned prompts are the ordinary questions a customer would ask.
- [x] No planned prompt requires private access, another user's data, secrets, or a real action.
- [x] No planned prompt attempts to change the chatbot's role or extract hidden configuration.
- [x] The target and the prompt list have been reviewed with the mentor.

## Record

| Field | Value |
|---|---|
| Exact public URL | `https://personal.nedbank.co.za/contact/Enbi-chat.html` |
| Date availability confirmed | 2026-10-09 |
| Published terms / usage rules checked (URL or quote) | |
| Mentor review date | 2026-10-17 — prompt plan (prompts.md Sections A–C) reviewed and approved; record in `runbook/AUTHORIZATION.md` |
| Public reporting contact, if available | |

## Change log

| Date | Change | Who |
|---|---|---|
| 2026-10-09 | Recorded mentor guidance; selected Enbi; limited scope to public observation | |
| 2026-10-09 | Switched primary from TOBi to Enbi (TOBi hands off to a human agent) | |
| 2026-10-14 | Confirmed TOBi now requires a mobile number + SMS verification; ChatBunny page failed to render and `/signup`,`/login` returned 404. Enbi remains primary. | |
| 2026-10-17 | Mentor approved all sections of the prompting plan; testing on Enbi may proceed. Recorded in `runbook/AUTHORIZATION.md`. | Mentor / project owner |
