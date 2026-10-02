"""Differential: real parse_duration vs the corpus reference.

Exhaustive part : every string of length <= 4 over an 18-char ASCII alphabet that
                  includes ALL digits 0-9 (the first differential had only 0,1,2).
Sampled part    : seeded random token strings (multi-digit runs, any order, mixed case,
                  stray whitespace/dots/junk) up to ~12 chars, so inputs like "90m",
                  "1h30m15s" and malformed near-misses are actually exercised.
Also reports how many compared strings were ACCEPTED, since a differential in which
nearly everything raises says little about the success path.
Unicode digits are probed separately and are NOT part of the agreement count.
"""

from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from corpus.adversaries import reference_literal
from duration_parser import parse_duration


def run(f, s):
    try:
        return ("ok", f(s))
    except ValueError:
        return ("ValueError", None)


def compare(strings):
    n = diff = accepted = 0
    first = []
    for s in strings:
        n += 1
        a, b = run(parse_duration, s), run(reference_literal, s)
        accepted += a[0] == "ok"
        if a != b:
            diff += 1
            if len(first) < 5:
                first.append((s, a, b))
    return n, diff, accepted, first


def exhaustive(alpha, max_len):
    for length in range(max_len + 1):
        for t in itertools.product(alpha, repeat=length):
            yield "".join(t)


def sampled(count, seed=0):
    rng = random.Random(seed)
    for _ in range(count):
        parts = []
        for _ in range(rng.randint(0, 4)):
            digits = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 3)))
            parts.append(digits + rng.choice("hhhmmmsssHMSx"))
        if rng.random() < 0.3:
            rng.shuffle(parts)
        s = "".join(parts)
        if rng.random() < 0.25 and s:
            i = rng.randrange(len(s) + 1)
            s = s[:i] + rng.choice([" ", ".", "\t", "\n", "-", "+", "5"]) + s[i:]
        if rng.random() < 0.1 and s:
            s = s[: rng.randrange(len(s))]
        yield s


if __name__ == "__main__":
    alpha = "0123456789hmsHM .\t"
    print(f"exhaustive: alphabet={alpha!r} ({len(alpha)} chars), lengths 0-4")
    n, d, a, first = compare(exhaustive(alpha, 4))
    print(f"  strings={n} accepted_by_impl={a} disagreements={d} first={first}")
    print("sampled: 300000 seeded token strings (seed=0), up to ~12 chars")
    n, d, a, first = compare(sampled(300_000))
    print(f"  strings={n} accepted_by_impl={a} disagreements={d} first={first}")
    print("unicode digit probes (outside the goal; NOT counted above):")
    for ch in ["\u0663", "\uff13", "\u00b2", "\u2460"]:
        s = ch + "h"
        print(f"  {ch!r}+'h': impl={run(parse_duration, s)} reference={run(reference_literal, s)}")
