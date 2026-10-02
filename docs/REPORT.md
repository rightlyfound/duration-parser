# Report: parse_duration under the corpus-gated protocol

**Convention root: INFERRED.** The convention record (docs/CONVENTIONS.md) is itself a
convention. No tool in this loop verified it, and nothing below claims it VERIFIED
(prompt 7.5, 7.6). C-GOAL is human-supplied; C-ADV and C-CANARY are agent-defined and
unreviewed externally.

## Measurable verdict (prompt Section 5)

- Test run: (passes=30, failures=0, unknowns=0)
- Corpus: (caught=10, survived=0)  [initial: caught=4, survived=6]
- Report: (VERIFIED=16, INFERRED=3, UNSUPPORTED=0)
- Convention: (supplied=1 [C-GOAL], INFERRED=3 [C-GOAL-R1, C-CANARY, C-ADV], UNSUPPORTED=0); not STALE (revised to R1 this run)
- Exit condition: **Conditional** (TRUSTED_PASS, zero survivors, zero UNSUPPORTED, convention root INFERRED). This is the highest status reachable from inside the loop.

## Substitutions and deviations from the prompt (all disclosed)

- `check_audit` -> `tools/audit_suite.py` (C14).
- `run_checked` -> `check-audit verify` from branch `verify-wrapper` of check-audit-harness (as the handoff directed).
- Prompt 7.2 (every adversary cites a violated clause) is impossible for silent classes; adversaries declare `violates: None` there (CONVENTIONS.md, C-ADV).
- A reference implementation lives in the corpus so the audit can prove non-vacuity before step 7.
- The suite author had seen the corpus. Authorship independence is NOT established.
- Not pushed to GitHub (C15); delivered as a git bundle.
- The first differential (C8) was narrow; C8b widens it. C11 (Unicode digits) was found by code reading, not by any differential.

## Claims

| id | claim | status | evidence | depends_on |
|---|---|---|---|---|
| C1 | The reference implementation passed the suite BEFORE the audit ran (audit is non-vacuous). | VERIFIED | docs/evidence/initial_audit.txt: `reference_literal: exit 0, failed tests: []` | C-ADV |
| C2 | Initial corpus audit: 4 caught, 6 survived, 0 untrusted (the corpus gate fired). | VERIFIED | docs/evidence/initial_audit.txt: `Corpus: (caught=4, survived=6, untrusted=0)` | C-ADV, C-GOAL |
| C3 | The audit tool labelled 5 survivors spec gap and 1 test gap, computed from each adversary's declared `violates`. | VERIFIED | docs/evidence/initial_audit.txt: `any_order              Order_Dependence       None         0 SURVIVED   spec gap` | C-ADV |
| C3b | (same run) the single test-gap label: | VERIFIED | docs/evidence/initial_audit.txt: `zero_is_malformed      Zero_Treatment         G1           0 SURVIVED   test gap` | C-ADV |
| C4 | Those labels are correct readings of the goal: five classes are genuinely silent, and Zero_Treatment is NOT silent. Borderline: the counter-reading is that the goal never says zero is valid. | INFERRED | none (judgment; see C-GOAL / C-GOAL-R1) | C-GOAL |
| C5 | After amendments G4-G8 and before any new test, the unchanged suite still left 6 survivors, now all labelled test gap (each cites a clause). | VERIFIED | docs/evidence/post_amendment_audit.txt: `any_order              Order_Dependence       G4           0 SURVIVED   test gap` | C-GOAL-R1, C-ADV |
| C6 | After the closing tests, the corpus audit: 10 caught, 0 survived, 0 untrusted. Each adversary names its catching tests in the log. | VERIFIED | docs/evidence/final_audit.txt: `Corpus: (caught=10, survived=0, untrusted=0)` | C-GOAL-R1, C-ADV |
| C7 | The real implementation passes the closed suite with DURATION_IMPL unset. | VERIFIED | docs/evidence/real_suite.txt: `30 passed in 0.14s` | C-GOAL, C-GOAL-R1 |
| C8 | First differential: the implementation and the corpus reference never disagreed on 111,111 strings (alphabet '012hmsHM .', lengths 0-5). NARROW: only the digits 0, 1, 2 appear and nothing longer than 5 characters, so inputs like 45m or 1h30m15s are not covered here; see C8b. | VERIFIED | docs/evidence/differential.txt: `strings compared=111111  disagreements=0  first=None` | C-GOAL-R1, C-ADV |
| C8b | Wider differential: 0 disagreements on 300,000 seeded token strings (37,933 accepted by the implementation). The exhaustive part (all digits 0-9, lengths 0-4, 111,151 strings, 3,630 accepted) also found 0. | VERIFIED | docs/evidence/differential_extended.txt: `strings=300000 accepted_by_impl=37933 disagreements=0 first=[]` | C-GOAL-R1, C-ADV |
| C9 | run_checked (check-audit verify) with a real canary returned TRUSTED_PASS, exit 0. | VERIFIED | docs/evidence/run_checked_A.txt: `VERDICT: TRUSTED_PASS` | C-CANARY |
| C9b | (same run) exit code: | VERIFIED | docs/evidence/run_checked_A.txt: `EXIT=0` | C-CANARY |
| C10 | With the canary swapped for one that passes, run_checked returned UNTRUSTED, exit 2. | VERIFIED | docs/evidence/run_checked_B.txt: `VERDICT: UNTRUSTED` | C-CANARY |
| C10b | (same run) exit code: | VERIFIED | docs/evidence/run_checked_B.txt: `EXIT=2` | C-CANARY |
| C11 | The reference accepts Unicode decimal digits (Arabic-Indic, fullwidth) and the implementation rejects them; superscript and circled digits are rejected by both. FOUND BY READING THE CODE (reference uses \d, implementation checks ASCII digits) and confirmed by hand-picked probes. NO differential run covers it: every differential alphabet is ASCII. The goal is silent, so neither behavior is wrong and no test asserts either. | VERIFIED | docs/evidence/differential_extended.txt: `'٣'+'h': impl=('ValueError', None) reference=('ok', 10800)` | C-ADV, C-GOAL-R1 |
| C12 | The suite tracks the goal. Supported only as: no corpus adversary survives. The corpus is the agent's own and unreviewed; the suite was written after the agent saw the corpus; classes outside the corpus are untested. | INFERRED | none (judgment; see C-GOAL / C-GOAL-R1) | C-ADV, C-GOAL-R1 |
| C13 | No test asserts a spec choice the goal or amendments did not make (per-assertion mapping below). | INFERRED | none (judgment; see C-GOAL / C-GOAL-R1) | C-GOAL, C-GOAL-R1 |
| C14 | check_audit.core.audit() is hardwired to the dedupe goal, so a suite-vs-corpus adapter was substituted. | VERIFIED | check-audit-harness src/check_audit/core.py:122: `if not satisfies_goal(original, output):` | C-ADV |
| C15 | The result was NOT pushed to GitHub: the connector returned 403 on every write. | VERIFIED | docs/evidence/connector_errors.txt: `403 Resource not accessible by integration` | C-ADV |

## C13 detail: assertion -> goal clause

| Test | Inputs | Goal clause tested |
|---|---|---|
| test_total_seconds | 2h, 45m, 45s, 1h30m, 1h30m15s | G2 (suffix), G1 (total) |
| test_total_seconds | 0s, 0h, 1h0m | G2 + G1 (borderline: see C4) |
| test_result_is_int | 1h30m | G1 ("as int") |
| test_malformed_raises_value_error | abc, 1x, 1h2x | G3; x is not a G2 suffix |
| test_out_of_order_is_malformed | 30m1h, 15s1m, 45s2h | G4 (R1), G3 |
| test_uppercase_suffix_is_malformed | 1H, 30M, 45S, 1h30M | G5 (R1), G3 |
| test_whitespace_is_malformed | 5 whitespace variants | G6 (R1), G3 |
| test_repeated_unit_is_malformed | 1h1h, 30m30m, 1s2s | G7 (R1), G3 |
| test_decimal_is_malformed | 1.5h, 1.5s, 0.5m | G8 (R1), G3 |

Assertions marked as encoding an undocumented choice: **none**. Inputs deliberately NOT
tested because the goal is still silent: empty string, bare number, negatives, leading
zeros, values over 59, huge values, non-str arguments, Unicode digits.

## Appendix: pasted logs (unedited)

### docs/evidence/initial_audit.txt

```
reference_literal: exit 0, failed tests: []
adversary              class                  violates  exit verdict    classification
any_order              Order_Dependence       None         0 SURVIVED   spec gap
case_insensitive       Case_Blindness         None         0 SURVIVED   spec gap
zero_is_malformed      Zero_Treatment         G1           0 SURVIVED   test gap
tolerates_whitespace   Whitespace_Tolerance   None         0 SURVIVED   spec gap
sums_repeats           Repeat_Units           None         0 SURVIVED   spec gap
truncates_fractions    Fractional_Truncation  None         0 SURVIVED   spec gap
wrong_multiplier       Wrong_Total            G1           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_total_seconds[45m-2700]
    caught by: tests/test_parse_duration.py::test_total_seconds[1h30m-5400]
    caught by: tests/test_parse_duration.py::test_total_seconds[1h30m15s-5415]
returns_float          Wrong_Type             G1           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_result_is_int
swallows_malformed     No_Raise               G3           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[abc]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1x]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1h2x]
raises_wrong_type      Wrong_Exception        G3           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[abc]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1x]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1h2x]

Corpus: (caught=4, survived=6, untrusted=0)
```

### docs/evidence/post_amendment_audit.txt

```
reference_literal: exit 0, failed tests: []
adversary              class                  violates  exit verdict    classification
any_order              Order_Dependence       G4           0 SURVIVED   test gap
case_insensitive       Case_Blindness         G5           0 SURVIVED   test gap
zero_is_malformed      Zero_Treatment         G1           0 SURVIVED   test gap
tolerates_whitespace   Whitespace_Tolerance   G6           0 SURVIVED   test gap
sums_repeats           Repeat_Units           G7           0 SURVIVED   test gap
truncates_fractions    Fractional_Truncation  G8           0 SURVIVED   test gap
wrong_multiplier       Wrong_Total            G1           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_total_seconds[45m-2700]
    caught by: tests/test_parse_duration.py::test_total_seconds[1h30m-5400]
    caught by: tests/test_parse_duration.py::test_total_seconds[1h30m15s-5415]
returns_float          Wrong_Type             G1           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_result_is_int
swallows_malformed     No_Raise               G3           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[abc]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1x]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1h2x]
raises_wrong_type      Wrong_Exception        G3           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[abc]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1x]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1h2x]

Corpus: (caught=4, survived=6, untrusted=0)
```

### docs/evidence/final_audit.txt

```
reference_literal: exit 0, failed tests: []
adversary              class                  violates  exit verdict    classification
any_order              Order_Dependence       G4           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[30m1h]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[15s1m]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[45s2h]
case_insensitive       Case_Blindness         G5           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[1H]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[30M]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[45S]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[1h30M]
zero_is_malformed      Zero_Treatment         G1           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_total_seconds[0s-0]
    caught by: tests/test_parse_duration.py::test_total_seconds[0h-0]
    caught by: tests/test_parse_duration.py::test_total_seconds[1h0m-3600]
tolerates_whitespace   Whitespace_Tolerance   G6           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h 30m]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[ 45s]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[45s ]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h\t30m]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h\n30m]
sums_repeats           Repeat_Units           G7           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[1h1h]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[30m30m]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[1s2s]
truncates_fractions    Fractional_Truncation  G8           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[1.5h]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[1.5s]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[0.5m]
wrong_multiplier       Wrong_Total            G1           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_total_seconds[45m-2700]
    caught by: tests/test_parse_duration.py::test_total_seconds[1h30m-5400]
    caught by: tests/test_parse_duration.py::test_total_seconds[1h30m15s-5415]
returns_float          Wrong_Type             G1           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_result_is_int
swallows_malformed     No_Raise               G3           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[abc]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1x]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1h2x]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[30m1h]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[15s1m]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[45s2h]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[1H]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[30M]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[45S]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[1h30M]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h 30m]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[ 45s]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[45s ]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h\t30m]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h\n30m]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[1h1h]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[30m30m]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[1s2s]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[1.5h]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[1.5s]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[0.5m]
raises_wrong_type      Wrong_Exception        G3           1 CAUGHT     
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[abc]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1x]
    caught by: tests/test_parse_duration.py::test_malformed_raises_value_error[1h2x]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[30m1h]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[15s1m]
    caught by: tests/test_parse_duration.py::test_out_of_order_is_malformed[45s2h]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[1H]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[30M]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[45S]
    caught by: tests/test_parse_duration.py::test_uppercase_suffix_is_malformed[1h30M]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h 30m]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[ 45s]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[45s ]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h\t30m]
    caught by: tests/test_parse_duration.py::test_whitespace_is_malformed[1h\n30m]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[1h1h]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[30m30m]
    caught by: tests/test_parse_duration.py::test_repeated_unit_is_malformed[1s2s]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[1.5h]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[1.5s]
    caught by: tests/test_parse_duration.py::test_decimal_is_malformed[0.5m]

Corpus: (caught=10, survived=0, untrusted=0)
```

### docs/evidence/real_suite.txt

```
..............................                                           [100%]
30 passed in 0.14s
exit=0
```

### docs/evidence/differential.txt

```
alphabet='012hmsHM .' (10 chars), lengths 0-5
strings compared=111111  disagreements=0  first=None
unicode digit (outside suite & goal): ('ValueError', None) vs reference ('ok', 10800)
```

### docs/evidence/differential_extended.txt

```
exhaustive: alphabet='0123456789hmsHM .\t' (18 chars), lengths 0-4
  strings=111151 accepted_by_impl=3630 disagreements=0 first=[]
sampled: 300000 seeded token strings (seed=0), up to ~12 chars
  strings=300000 accepted_by_impl=37933 disagreements=0 first=[]
unicode digit probes (outside the goal; NOT counted above):
  '٣'+'h': impl=('ValueError', None) reference=('ok', 10800)
  '３'+'h': impl=('ValueError', None) reference=('ok', 10800)
  '²'+'h': impl=('ValueError', None) reference=('ValueError', None)
  '①'+'h': impl=('ValueError', None) reference=('ValueError', None)
```

### docs/evidence/run_checked_A.txt

```
VERDICT: TRUSTED_PASS
stamp duration_parser: /home/claude/duration-parser/src/duration_parser/__init__.py [ok]

--- canary: env DURATION_IMPL=wrong_multiplier python -m pytest -q -rf -p no:cacheprovider (exit 1); last output ---
            ("45m", 2700),  # G2 (m), G1
            ("45s", 45),  # G2 (s), G1
            ("1h30m", 5400),  # G2, G1: total seconds across suffixes
            ("1h30m15s", 5415),  # G2, G1
            ("0s", 0),  # G2 + G1: number 0 with a recognized suffix; total is 0
            ("0h", 0),  # G2 + G1
            ("1h0m", 3600),  # G2 + G1: zero component contributes nothing
        ],
    )
    def test_total_seconds(parse_duration, text, seconds):
>       assert parse_duration(text) == seconds
E       AssertionError: assert 6615 == 5415
E        +  where 6615 = <function _wrong_multiplier at 0x7f27fdac7420>('1h30m15s')

tests/test_parse_duration.py:27: AssertionError
=========================== short test summary info ============================
FAILED tests/test_parse_duration.py::test_total_seconds[45m-2700] - Assertion...
FAILED tests/test_parse_duration.py::test_total_seconds[1h30m-5400] - Asserti...
FAILED tests/test_parse_duration.py::test_total_seconds[1h30m15s-5415] - Asse...
3 failed, 27 passed in 0.17s

--- command: python -m pytest -q -rf -p no:cacheprovider (exit 0); last output ---
..............................                                           [100%]
30 passed in 0.15s
EXIT=0
```

### docs/evidence/run_checked_B.txt

```
VERDICT: UNTRUSTED
  - canary exited 0: this check cannot go red on known-bad input
stamp duration_parser: /home/claude/duration-parser/src/duration_parser/__init__.py [ok]

--- canary: env DURATION_IMPL=reference_literal python -m pytest -q -rf -p no:cacheprovider (exit 0); last output ---
..............................                                           [100%]
30 passed in 0.15s

--- command: python -m pytest -q -rf -p no:cacheprovider (exit 0); last output ---
..............................                                           [100%]
30 passed in 0.15s
EXIT=2
```

### docs/evidence/git_log_before_report.txt

```
7b599fe impl: parse_duration (scanner) passing the closed suite
fbbd098 test: tests for approved amendments G4-G8
183d217 test: close test gap Zero_Treatment (G1, G2)
b6cc638 corpus: adversaries now cite amended clauses G4-G8 (R1)
389031b docs: convention record R1 - approved goal amendments G4-G8
8c78367 tooling: suite-vs-corpus audit adapter (check_audit is not goal-parametric)
cdd6773 test: initial suite from the goal alone (G1-G3)
403d4e6 corpus: reference + 10 adversaries (6 input classes, 4 goal-violators)
cb57e97 docs: convention record R0 with pre-registered classification rule
91f2248 chore: scaffold (pytest config, gitignore)
af8264f Initial commit
```
