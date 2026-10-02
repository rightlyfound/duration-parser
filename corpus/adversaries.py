"""Adversary corpus for parse_duration. Written BEFORE the real implementation.

`reference_literal` exists only so the audit can prove the suite is not vacuous (a
suite that fails everything "catches" everything). It is NOT the deliverable; the real
implementation is written later, after the suite is closed.

Each Adversary differs from the reference on exactly one input class and declares
`violates`: the goal clause it breaks (G1/G2/G3), or None where the goal is silent.
Goal (docs/CONVENTIONS.md, C-GOAL):
  G1 returns total seconds as int
  G2 recognizes h, m, s suffixes
  G3 raises ValueError on malformed input
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction

_UNIT = {"h": 3600, "m": 60, "s": 1}
_STRICT = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")


def reference_literal(s: str) -> int:
    match = _STRICT.fullmatch(s)
    if match is None or not any(g is not None for g in match.groups()):
        raise ValueError(f"malformed duration: {s!r}")
    h, m, sec = (int(g) if g is not None else 0 for g in match.groups())
    return h * 3600 + m * 60 + sec


@dataclass(frozen=True)
class Adversary:
    name: str
    input_class: str
    violates: str | None  # goal clause broken, or None when the goal is silent
    impl: Callable[[str], object]


def _any_order(s: str) -> int:
    parts = re.findall(r"(\d+)([hms])", s)
    if "".join(n + u for n, u in parts) != s or not parts:
        raise ValueError(s)
    units = [u for _, u in parts]
    if len(set(units)) != len(units):
        raise ValueError(s)
    return sum(int(n) * _UNIT[u] for n, u in parts)


def _case_insensitive(s: str) -> int:
    return reference_literal(s.lower())


def _zero_is_malformed(s: str) -> int:
    total = reference_literal(s)
    if any(int(n) == 0 for n in re.findall(r"\d+", s)):
        raise ValueError(f"zero component: {s!r}")
    return total


def _tolerates_whitespace(s: str) -> int:
    return reference_literal("".join(s.split()))


def _sums_repeats(s: str) -> int:
    if not s or re.fullmatch(r"(?:\d+h)*(?:\d+m)*(?:\d+s)*", s) is None:
        raise ValueError(s)
    return sum(int(n) * _UNIT[u] for n, u in re.findall(r"(\d+)([hms])", s))


def _truncates_fractions(s: str) -> int:
    pattern = r"(?:(\d+(?:\.\d+)?)h)?(?:(\d+(?:\.\d+)?)m)?(?:(\d+(?:\.\d+)?)s)?"
    match = re.fullmatch(pattern, s)
    if match is None or not any(g is not None for g in match.groups()):
        raise ValueError(s)
    parts = (Fraction(g) if g is not None else Fraction(0) for g in match.groups())
    return int(sum(p * mult for p, mult in zip(parts, (3600, 60, 1), strict=True)))


def _wrong_multiplier(s: str) -> int:
    match = _STRICT.fullmatch(s)
    if match is None or not any(g is not None for g in match.groups()):
        raise ValueError(s)
    h, m, sec = (int(g) if g is not None else 0 for g in match.groups())
    return h * 3600 + m * 100 + sec  # minutes worth 100 seconds


def _returns_float(s: str) -> float:
    return float(reference_literal(s))


def _swallows_malformed(s: str) -> int:
    try:
        return reference_literal(s)
    except ValueError:
        return 0


def _raises_wrong_type(s: str) -> int:
    try:
        return reference_literal(s)
    except ValueError as exc:
        raise KeyError(str(exc)) from exc


ADVERSARIES: tuple[Adversary, ...] = (
    Adversary("any_order", "Order_Dependence", None, _any_order),
    Adversary("case_insensitive", "Case_Blindness", None, _case_insensitive),
    Adversary("zero_is_malformed", "Zero_Treatment", "G1", _zero_is_malformed),
    Adversary("tolerates_whitespace", "Whitespace_Tolerance", None,
              _tolerates_whitespace),
    Adversary("sums_repeats", "Repeat_Units", None, _sums_repeats),
    Adversary("truncates_fractions", "Fractional_Truncation", None,
              _truncates_fractions),
    Adversary("wrong_multiplier", "Wrong_Total", "G1", _wrong_multiplier),
    Adversary("returns_float", "Wrong_Type", "G1", _returns_float),
    Adversary("swallows_malformed", "No_Raise", "G3", _swallows_malformed),
    Adversary("raises_wrong_type", "Wrong_Exception", "G3", _raises_wrong_type),
)

IMPLS: dict[str, Callable[[str], object]] = {
    "reference_literal": reference_literal,
    **{a.name: a.impl for a in ADVERSARIES},
}
