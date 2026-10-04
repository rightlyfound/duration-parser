"""parse_duration: "1h30m" -> 5400.

Goal (docs/CONVENTIONS.md): returns total seconds as int (G1); recognizes h, m, s
suffixes (G2); raises ValueError on malformed input (G3). Amendments G4-G8: h,m,s
order; lowercase only; no whitespace; each unit at most once; ASCII-digit integers.

Behavior the goal does NOT specify (no test asserts any of it; changing it is not a
regression): the empty string and a bare number with no suffix raise ValueError;
values over 59 are accepted ("90m" is 5400); leading zeros are accepted; a non-str
argument raises TypeError.
"""

from __future__ import annotations

_SECONDS_PER_UNIT = {"h": 3600, "m": 60, "s": 1}
_UNIT_ORDER = "hms"
_ASCII_DIGITS = frozenset("0123456789")


def parse_duration(s: str) -> int:
    if not isinstance(s, str):
        raise TypeError(f"expected str, got {type(s).__name__}")
    if not s:
        raise ValueError("malformed duration: empty string")
    total = 0
    last_unit = -1
    i, n = 0, len(s)
    while i < n:
        j = i
        while j < n and s[j] in _ASCII_DIGITS:
            j += 1
        if j == i or j == n:  # no digits here, or digits with no suffix
            raise ValueError(f"malformed duration: {s!r}")
        unit = s[j]
        position = _UNIT_ORDER.find(unit)
        if position == -1:  # not h, m or s (includes uppercase and whitespace)
            raise ValueError(f"malformed duration: {s!r}")
        if position <= last_unit:  # out of order, or a repeated unit
            raise ValueError(f"malformed duration: {s!r}")
        total += int(s[i:j]) * _SECONDS_PER_UNIT[unit]
        last_unit = position
        i = j + 1
    return total
