# Target Options for Mentorship Session

> Select one chatbot with the mentor and document its ordinary public-user interface
> in [`runbook/AUTHORIZATION.md`](runbook/AUTHORIZATION.md).

## Mentor guidance

Separate written authorization is not needed for this capstone when tests are limited
to interacting with the chatbot as a public visitor or customer, at the same access
level offered through its normal interface. This does not include private endpoints,
other users' data, privileged actions, automated probing, or activity that violates
published usage rules.

## Target selection criteria

Choose one chatbot that:

- is currently available through a public website or app;
- has a clearly identified ordinary user interface and stated purpose;
- can be assessed with benign, manual, low-volume prompts; and
- has public terms or usage rules that can be checked before testing.

Potential targets discussed include Enbi, TOBi / SuperTOBi, and public service or
retail chatbots. Verify that the selected chatbot is actually available to an ordinary
visitor and record the precise URL. A target is not suitable if the planned tests would
require access beyond normal public-user functionality.

## Selection checklist

1. Which single chatbot and exact URL will be used?
2. What can an ordinary visitor or customer do in the chatbot?
3. What published usage rules apply?
4. What benign prompts fit its stated purpose?
5. What is the public reporting route if unexpected sensitive behavior appears?

Discuss the answers with the mentor and record the decision in
[`runbook/AUTHORIZATION.md`](runbook/AUTHORIZATION.md). If no suitable public interface
is available, revise the target with the mentor rather than seeking access to private
functionality.
