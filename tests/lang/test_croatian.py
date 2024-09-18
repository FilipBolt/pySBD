# -*- coding: utf-8 -*-
import pytest

GOLDEN_HR_RULES_TEST_CASES = [
    ("Tvrtka je osnovana 7. travnja 2020. godine, no datum na ugovoru je 20. ožujka 2020. godine.",
     ["Tvrtka je osnovana 7. travnja 2020. godine, no datum na ugovoru je 20. ožujka 2020. godine."]),
]


@pytest.mark.parametrize('text, expected_sents', GOLDEN_HR_RULES_TEST_CASES)
def test_pl_sbd(hr_default_fixture, text, expected_sents):
    """Croatian language SBD tests"""
    segments = hr_default_fixture.segment(text)
    segments = [s.strip() for s in segments]
    assert segments == expected_sents
