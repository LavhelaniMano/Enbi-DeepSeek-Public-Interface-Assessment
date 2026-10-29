# Track A — Red Team Proposal (One-Week Scope)

**Project:** Assessing an existing public-facing AI chatbot
**Track:** Track A — Red Team (test and report on an AI application)
**Primary attack type:** Direct prompt injection through the ordinary public interface
**Access model:** Public-user interaction only, following mentor guidance
**Timeline:** One week
**Status:** Revised proposal for mentor review

## Capstone Scope

Following mentor feedback, I will assess **one chatbot already deployed on a company website**, rather than build a RAG agent. The company may be based in South Africa or elsewhere. I will select the target with my mentor and record the company, chatbot, exact URL, normal public-user access context, and applicable public usage rules before starting.

The mentor's guidance is that separate written authorization is not needed when interacting with the chatbot as an ordinary public user, at the same level of access available to a customer or visitor. I will keep the assessment strictly within that public interface and its normal user capabilities. This does not extend to private endpoints, other users' data, privileged operations, scanning, high-volume requests, or activity prohibited by the site's terms.

The project will focus on **prompt injection**, a technique covered in the Week 7 detector and guardrails labs:

1. **Direct prompt injection:** test whether user-supplied instructions can make the chatbot disregard its stated role or other documented behavior.
2. **Indirect prompt injection:** out of scope. I will not plant instructions in third-party content or try to change a company's knowledge base.

Week 8 covered poisoning model training data and model backdoors. That is related background, but it is not the same as changing a live company's RAG corpus. **Knowledge-base poisoning is out of scope.**

## 1. Target and Public-User Boundaries

The target is one existing chatbot on a company website, selected with my mentor. Under the mentor's guidance, testing is limited to what an ordinary public user can do through the chatbot's intended interface. I will not seek separate owner authorization for these bounded interactions, but I will record the exact URL, access context, and published usage rules before testing.

Public availability is not permission to go beyond the public user experience. I will not access private endpoints or data, impersonate another user, attempt to retrieve secrets, trigger consequential account actions, bypass access controls, scan infrastructure, automate probes, or send high-volume requests. If the site's terms prohibit the planned interaction, I will not perform it.

If a test appears to require anything beyond ordinary user interaction, it is excluded rather than treated as implicitly authorized. I will ask my mentor to select a different public-only test or revise the scope; I will not probe further to establish permission within this capstone.

## 2. Why This Target and Scope

- **Real deployment:** Results concern a chatbot people can actually use, rather than a locally built demonstration.
- **A testable failure mode:** I will pick a target with a clearly stated public purpose and visible response boundaries, so I can compare normal behavior with benign prompt-injection variants without probing private features.
- **Bootcamp connection:** Week 7 covered direct and indirect prompt injection, detector limitations, guardrails, and red-team probing. I will use those concepts and report the limits of what I can test.
- **One-week feasibility:** Testing one chatbot and one primary attack type keeps the work achievable without building a RAG system or classifier.
- **Responsible testing:** Testing is limited to normal public-user interactions and the site's published usage rules.

## 3. Objectives

1. Establish normal chatbot behavior using a small set of benign baseline questions, repeated enough times to know what ordinary variance looks like on this target.
2. Review the chatbot's stated purpose and any publicly visible usage or safety guidance.
3. Test whether prompt injection changes ordinary chatbot behavior through the public interface, without attempting to cross access boundaries.
4. Record unusual responses as observations; do not claim a security vulnerability without evidence of a real, in-scope security impact.
5. Record the exact method, prompt category, response, and outcome for each executed test, including unsuccessful attempts.
6. Report evidence-based findings, limitations, and practical mitigations. I will not describe an untested weakness as a vulnerability.

## 4. Planned Tests

**The bar for calling something a vulnerability.** A chatbot producing unusual text after a prompt injection is an observation, not proof of a security vulnerability. This public-user assessment will not attempt to access another user's data, cause privileged actions, extract secrets, test downstream systems, or affect other users. Any reportable security impact must arise unexpectedly within the normal public interface and be supported by minimal, safely collected evidence. Stop immediately if that happens.

The prompt list will be reviewed with my mentor before testing. Prompts will be benign, non-sensitive, manually submitted, and low-volume.

| ID | Test | What it checks | Evidence and success measure |
|----|------|----------------|-----------------------------|
| 1.1 | Baseline behavior | How the chatbot responds to ordinary in-scope questions, to clearly out-of-scope benign questions, and how much the response varies when the same question is asked repeatedly | 5–10 repetitions per baseline prompt. This is the variance reference every later result is read against, so it is measured before any payload is sent |
| 1.2 | Role and response boundaries | Whether benign instructions alter the chatbot's stated role or ordinary response behavior | Captured response; unusual text alone is an observation, not a vulnerability |
| 1.3 | Direct prompt-injection variants | Whether controlled, benign paraphrases produce materially different behavior through the public interface | Compare responses with baseline and report the complete run count |
| 1.4 | Safe output formatting | Whether ordinary text or Markdown is displayed consistently in the chatbot interface | Record the rendered appearance only; do not submit executable markup, external fetch references, or content intended to cause a side effect |
Tests involving cross-user data, credentials or secrets, purchases, account changes, external actions, downstream sinks, access-control evasion, indirect injection, or service disruption are excluded. Do not attempt to verify those behaviors.

## 5. Bootcamp Alignment and Exclusions

- **In scope:** Prompt injection, based on the Week 7 prompt-injection detector and chatbot/guardrails exercises. Variants are test cases for that same technique, not separate claims of newly learned attack methods.
- **Out of scope:** Indirect injection, including injecting instructions into documents, third-party content, or the chatbot's knowledge base.
- **Out of scope as independent test classes:** RAG knowledge-base poisoning, training-data poisoning, model backdoors, pixel-level adversarial examples/FGSM, and denial-of-service testing.

A distinction worth stating explicitly, because it decides what the report may claim. Cross-user data access, authorization bypass, SSRF, and privileged actions are **not test objectives**. The capstone uses only the ordinary public interface and will not try to cross those boundaries. If a serious exposure appears unexpectedly during normal public-user interaction, I will stop immediately, retain minimal evidence, and notify my mentor and an appropriate public reporting contact. An unusual chatbot response alone is an observation, not a security finding.

The Week 8 data-poisoning and SHA-256 labs are useful context for understanding data integrity, but they do not authorise changes to a real company's documents, training data, or model, and I will not attempt any. I am also not attempting model or training-data extraction, membership inference, or memorization probing: all of them need a large query budget that the request limits will not permit, and a small sample would produce numbers too weak to report.

My Week 7 detector gets used, but offline. I will run it against my own drafted prompts locally to discard the ones it already blocks confidently, and send only the remainder to the live target. That reduces request volume, keeps testing gentle, and reuses the bootcamp work rather than discarding it.

## 6. Rules of Engagement

- Test **one named chatbot only**, using its normal public-facing interface and access level.
- Use only benign, non-sensitive input. Do not use real customer or employee information.
- Keep request volume low and manual. Do not run broad scans, automated probes, or denial-of-service tests.
- Do not attempt to access another user's account, private records, credentials, internal systems, or external services.
- Do not publish prompts or findings publicly. Share the report privately with the mentor and use a public reporting channel if an unexpected security issue is identified.
- Stop immediately if the chatbot exposes real personal data, appears to affect a real user or transaction, behaves in a way that could cause harm, or the site blocks or disallows the interaction. Preserve minimal evidence and notify the mentor.
- Do not extend testing to private interfaces, other users, privileged actions, or systems behind the chatbot.

## 7. Method and Evidence

A production chatbot is stochastic, so a single response proves almost nothing. Every result in this project is a distribution, not an observation. For each permitted test, I will:

1. Record the date, chatbot URL, public-user access context, applicable usage rules, and baseline variance from 1.1.
2. Run each selected benign prompt **5–10 times**, manually and at a low rate. Stop if the service objects, blocks the test, or the interaction could cause a real-world effect.
3. Save every individual input and response rather than only the most interesting one, with timestamps and a screenshot or other permitted evidence. Redact personal information and secrets.
4. Report the **success rate with its denominator**, and treat anything under a consistent threshold as unreliable rather than as a bypass. The threshold is set from 1.1, not chosen afterwards to make a result look clean.
5. Classify each result as **blocked**, **not blocked**, **inconclusive**, or **not run**, and separately as **finding** or **observation**. A changed or unexpected response alone is an observation.
6. Stop if the service objects or if the planned low-volume test is complete, and report what was not covered.

Keeping every response matters for a specific reason: a selective write-up of only the successes is what makes an inexperienced report untrustworthy, and the unsuccessful prompts are evidence that the testing was real.

I will use the Week 7 lab materials to guide manual test categories. I will not use Garak or other automated probing against a live target; automated scanning is both a load on someone else's production system and outside this public-user assessment.

## 8. Deliverables

1. **Target and scope record:** company, chatbot URL, public-user access context, published usage rules, and test boundaries.
2. **Test log:** each planned test marked as executed, blocked, inconclusive, or not run.
3. **Evidence:** screenshots and exact prompt/response pairs, with sensitive information redacted.
4. **Comprehensive findings report:** executive summary; scope and methods; tasks executed; chatbot responses; successful and unsuccessful tests; evidence; limitations; risk and practical remediation for each substantiated vulnerability.
5. **Reporting record:** date and method the report was shared privately with the mentor and, if appropriate, through a public reporting channel.

## 9. One-Week Plan

**Before Day 1 — Select the target and confirm public-user boundaries.** Agree on one company chatbot with the mentor. Record the exact public interface, ordinary access context, and published usage rules. Exclude any test that would require access beyond that.

**Day 1 — Confirm scope and baseline.** Verify the exact URL, ordinary access context, benign prompt list, low-volume limit, stop conditions, and public reporting contact if available. Capture baseline behavior.

**Day 2 — Prepare the test log.** Draft the benign prompt variants for tests 1.2, 1.3, and 1.4, run them past my Week 7 detector offline to drop the ones it already blocks confidently, and turn the survivors into a short, bounded checklist. Confirm the evidence and data-handling process with the mentor.

**Days 3–4 — Execute bounded tests.** Run 1.1 baseline repetitions first, then the selected direct-injection prompts through the normal public interface. Do not run indirect injection or tests of private functionality.

**Day 5 — Verify evidence.** Repeat selected results only within the low-volume public-user plan. Mark results that cannot be reproduced as inconclusive, and check that every response set was captured rather than just the interesting ones.

**Days 6–7 — Report.** Write the findings report, include successful and unsuccessful tests, and share it privately with the mentor. Use a public reporting channel if an unexpected security issue is identified.

## 10. Reporting and Success Measures

The report will distinguish an unexpected chatbot response from a genuine security finding. Only a reproducible, evidenced security impact within the public-user scope will be described as a vulnerability; ordinary response changes will be labelled as observations.

The report will include:

- Number of tests planned, executed, blocked, inconclusive, and not run.
- Every mentor-reviewed prompt with its full response set and success rate, with identifying or sensitive material redacted.
- For each result, the observed behavior and evidence, without claiming impact that was not tested or demonstrated.
- The baseline variance, so a reader can judge whether a 3-in-10 result is a bypass or noise.
- Findings with severity rationale, limitations, and recommended mitigations.
- An explicit statement of what I did not test and why — scope exclusions, unavailable request budget, and untestable surfaces.
- Confirmation that testing stayed within ordinary public-user access and that results were shared privately.

Two results are both acceptable, and I will not inflate either. A **confirmed finding** with a crossed trust boundary is the outcome the mentor is asking for. **"No vulnerability demonstrated within this limited scope"** is equally valid, provided it states what was tested, how often, and what remains untested. What I will not do is present a blocked-attack transcript as though it were a breach, or claim the chatbot is secure on the basis of a small test set.

## 11. Risks and Limitations

- **Limited public-user scope.** The assessment follows mentor guidance and uses only the chatbot's ordinary public interface. It does not test private functions, other users' data, privileged actions, or underlying infrastructure.
- **Published rules still apply.** Check the chatbot's current terms and usage rules. If they prohibit planned activity or the interface objects to testing, stop and discuss the scope with the mentor.
- **Limited visibility.** I may not know the chatbot's model, retrieval sources, or guardrail configuration; the report will describe observed behavior, not speculate about implementation.
- **Limited coverage.** One chatbot and a small prompt set are not a full security assessment, and a single result is not a trend.
- **No indirect injection or knowledge-base changes.** The Week 8 training-data poisoning lab does not authorize changing a company's data or model; those activities are excluded.
- **Responsible reporting.** Keep results private, share them with the mentor, and use an appropriate public reporting contact if an unexpected security issue appears.

## 12. Conclusion

I propose a one-week assessment of one existing company website chatbot, selected with
the mentor and accessed only as an ordinary public user. Following the mentor's
guidance, separate written authorization is not needed for this narrow interaction.
The project focuses on benign, manual, low-volume prompt-injection behavior through the
normal public interface. I will not build a separate RAG agent, modify company data, or
test private or privileged functions. The final report will document the methods,
responses, limitations, and evidence, including unsuccessful tests, without overstating
what the assessment demonstrates.

**Approval requested:** mentor confirmation of the selected public chatbot, the exact
URL, the ordinary user access context, and the benign prompt list.
