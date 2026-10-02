"""Initial suite, written from the goal alone. Each assertion cites a goal clause.

G1 returns total seconds as int
G2 recognizes h, m, s suffixes
G3 raises ValueError on malformed input
"""

from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        ("2h", 7200),  # G2 (h), G1
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
    assert parse_duration(text) == seconds


def test_result_is_int(parse_duration):
    # G1: "as int"
    assert type(parse_duration("1h30m")) is int


@pytest.mark.parametrize("text", ["abc", "1x", "1h2x"])
def test_malformed_raises_value_error(parse_duration, text):
    # G3. 1x / 1h2x: x is not among the suffixes G2 recognizes.
    with pytest.raises(ValueError):
        parse_duration(text)
