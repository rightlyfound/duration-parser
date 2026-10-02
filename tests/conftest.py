"""Selects the implementation under test.

DURATION_IMPL=<name> loads that implementation from corpus.adversaries (used by the
audit and the canary). Unset, it loads the real duration_parser.parse_duration.
"""

from __future__ import annotations

import os

import pytest


@pytest.fixture
def parse_duration():
    name = os.environ.get("DURATION_IMPL")
    if name:
        from corpus.adversaries import IMPLS

        return IMPLS[name]
    from duration_parser import parse_duration as real

    return real
