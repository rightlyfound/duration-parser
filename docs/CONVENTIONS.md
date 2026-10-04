# Convention record (prompt Section 7.1/7.2)

Status of this record: **INFERRED**. It is itself a convention (7.4). No tool in this
loop can verify it; an external party is required to move it (7.6).

Revision counter: R0 (initial). STALE if unrevised after N=3 runs.

## C-GOAL  (anchor: Goal)

- **C-A (assertion):** `parse_duration(s: str) -> int` "returns total seconds as int;
  recognizes h, m, s suffixes; raises ValueError on malformed input."
  Clauses, cited by the suite and the corpus:
  - **G1** returns total seconds as int
  - **G2** recognizes h, m, s suffixes
  - **G3** raises ValueError on malformed input
- **C-S (source):** supplied verbatim by the human in the task statement
  (this conversation). Not derived by the agent.
- **C-R (revision condition):** the human approves an amendment. The agent may only
  PROPOSE amendments (prompt Section 6 amendment); it may not apply them.

## C-CANARY  (anchor: Canary sibling)

- **C-A:** a canary is the same runner invocation as the real check (same command,
  same test files, same working directory) differing only in the implementation under
  test, which is a known-bad one that violates G1.
- **C-S:** agent-defined; sibling conditions are the testable predicates below.
  Predicates: (1) identical argv except the `DURATION_IMPL` environment variable;
  (2) exits non-zero; (3) its output contains the text `FAILED` and a test id.
- **C-R:** revise if the runner changes or if a canary ever exits 0 on the suite.

## C-ADV  (anchor: Adversary)

- **C-A:** each adversary is an alternative implementation of `parse_duration`
  differing from the literal reference on exactly one input class. Each declares
  `violates`: the goal clause it breaks, or `None` when the goal is silent.
  *Deviation from prompt 7.2:* 7.2 requires every adversary to cite a violated clause.
  An adversary probing a class the goal is silent on cannot, by definition. `None` is
  the honest value there, and the survivor is then classified a spec gap.
- **C-S:** agent-defined (`corpus/adversaries.py`). The corpus is the agent's own
  and has not been reviewed externally (prompt Section 9).
- **C-R:** revise when an input class is found that no adversary covers.

## Classification rule (fixed BEFORE the first audit run)

A corpus survivor is a **test gap** iff `violates` names a clause. That is, a goal
clause, applied literally to the deviating input, determines the output and the
adversary's output differs. It is a **spec gap** iff `violates` is `None`: the goal is
silent on the input class.

- Test gap -> add tests citing the clause. No approval needed.
- Spec gap -> PROPOSE a goal amendment, halt, await approval. No test.

Borderline declarations are listed in the report. They are judgments, not facts.

---

# Revision R1 (goal amendments, human-approved)

Revision counter: R1. Status of this record remains **INFERRED**.

All five amendments below were PROPOSED by the agent after the initial corpus audit
(5 spec-gap survivors) and APPROVED by the human in this conversation ("accept all
five as defaults"). C-S for every amendment is that approval, not the agent.
Each amendment is a claim with its own C-A / C-S / C-R, per 7.1.

| ID | C-A (assertion) | C-R (revise if) |
|----|-----------------|-----------------|
| **G4** | Components must appear in h, m, s order; out-of-order input is malformed. | a user needs `30m1h` to parse |
| **G5** | Suffixes are lowercase only; uppercase suffixes are malformed. | users report `1H` should parse |
| **G6** | No whitespace anywhere; any whitespace is malformed. | users need `1h 30m` to parse |
| **G7** | Each unit appears at most once; repeated units are malformed. | a use case needs `1h1h` summed |
| **G8** | Components are digit-only non-negative integers; decimals are malformed. | fractional durations become a feature |

All five are the conservative reading (reject more, accept less); relaxing any of them
is an explicit addition, not a silent assumption.

## Classification outcome under the R0 rule

- Zero_Treatment: classified **test gap** (adversary declares `violates: G1`).
  **Borderline:** the counter-reading is that the goal never says zero is valid, i.e.
  silent. This is a judgment, accepted by the human, and recorded here as one.
- The five spec gaps are closed by amendment G4-G8, not by tests written before it.

## Still silent (deliberately NOT asserted by any test)

Empty string, a bare number with no suffix (`"90"`), negative numbers, leading `+`,
leading zeros, unit values over 59 (`"90m"`), very large values, non-str arguments.
The goal and amendments make no choice here, so no test encodes one. The
implementation's behavior on these inputs is undocumented, not specified.

## C-CANARY revision (R1)

Predicate (1) is restated to match how the runner can actually express it:
the canary is the same command wrapped as `env DURATION_IMPL=<known-bad> <command>`;
the test command, files and working directory are identical. Predicates (2) and (3)
are unchanged. Reason: `check-audit verify` runs argv lists in a shared environment, so
a per-run variable is passed through `env`.
