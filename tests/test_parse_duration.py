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


# --- Amended clauses (R1, human-approved) -------------------------------------
# G4 h,m,s order; G5 lowercase only; G6 no whitespace; G7 each unit at most once;
# G8 digit-only integers. Each case below is malformed per its cited clause.


@pytest.mark.parametrize("text", ["30m1h", "15s1m", "45s2h"])
def test_out_of_order_is_malformed(parse_duration, text):  # G4, G3
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("text", ["1H", "30M", "45S", "1h30M"])
def test_uppercase_suffix_is_malformed(parse_duration, text):  # G5, G3
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("text", ["1h 30m", " 45s", "45s ", "1h\t30m", "1h\n30m"])
def test_whitespace_is_malformed(parse_duration, text):  # G6, G3
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("text", ["1h1h", "30m30m", "1s2s"])
def test_repeated_unit_is_malformed(parse_duration, text):  # G7, G3
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize("text", ["1.5h", "1.5s", "0.5m"])
def test_decimal_is_malformed(parse_duration, text):  # G8, G3
    with pytest.raises(ValueError):
        parse_duration(text)
