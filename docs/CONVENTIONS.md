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
