"""Audit the pytest suite against the adversary corpus.

check_audit.core.audit() is hardwired to the dedupe goal, so this adapter keeps its
contract instead: adversaries are implementations, the suite is the check, and an
adversary is CAUGHT when the suite rejects it. Only pytest exit code 1 (tests failed)
counts as a catch. Exit codes 2-5 (interrupted/internal/usage/no tests) and timeouts
are UNTRUSTED, so a broken runner can never register as "caught".

The reference implementation must pass first, or the audit is vacuous.

Usage: python tools/audit_suite.py [--json PATH]
Exit:  0 audit valid (survivors are results, not errors); 2 audit invalid/untrusted.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from corpus.adversaries import ADVERSARIES

CAUGHT, SURVIVED, UNTRUSTED = "CAUGHT", "SURVIVED", "UNTRUSTED"


def run_suite(impl: str) -> tuple[int | None, list[str], str]:
    env = {**os.environ, "DURATION_IMPL": impl}
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-rf", "-p", "no:cacheprovider"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=120, check=False,
        )
    except subprocess.TimeoutExpired:
        return None, [], "timeout"
    failed = [ln.split(" - ")[0][7:] for ln in proc.stdout.splitlines()
              if ln.startswith("FAILED ")]
    return proc.returncode, failed, proc.stdout


def main(argv: list[str]) -> int:
    rc, failed, out = run_suite("reference_literal")
    print(f"reference_literal: exit {rc}, failed tests: {failed}")
    if rc != 0:
        print("AUDIT INVALID: the reference does not pass the suite.")
        print(out[-1500:])
        return 2
    rows = []
    for adv in ADVERSARIES:
        rc, failed, _ = run_suite(adv.name)
        verdict = {0: SURVIVED, 1: CAUGHT}.get(rc, UNTRUSTED) if rc is not None \
            else UNTRUSTED
        if verdict == CAUGHT and not failed:
            verdict = UNTRUSTED  # exit 1 without a named failing test: not a catch
        kind = ""
        if verdict == SURVIVED:
            kind = "test gap" if adv.violates else "spec gap"
        rows.append({"adversary": adv.name, "class": adv.input_class,
                     "violates": adv.violates, "exit": rc, "verdict": verdict,
                     "classification": kind, "failed_tests": failed})
    print(f"{'adversary':22} {'class':22} {'violates':9} {'exit':>4} "
          f"{'verdict':10} classification")
    for r in rows:
        print(f"{r['adversary']:22} {r['class']:22} {r['violates']!s:9} "
              f"{r['exit']!s:>4} {r['verdict']:10} {r['classification']}")
        for t in r["failed_tests"]:
            print(f"    caught by: {t}")
    caught = sum(r["verdict"] == CAUGHT for r in rows)
    survived = sum(r["verdict"] == SURVIVED for r in rows)
    untrusted = sum(r["verdict"] == UNTRUSTED for r in rows)
    print(f"\nCorpus: (caught={caught}, survived={survived}, untrusted={untrusted})")
    if "--json" in argv:
        Path(argv[argv.index("--json") + 1]).write_text(
            json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return 2 if untrusted else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
