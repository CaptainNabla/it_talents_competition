import pytest

from data.preprocessing import date_to_numeric


def test_date_to_numeric_ignoreInput():
    expected = "1.34"
    actual = date_to_numeric(expected)

    assert expected == actual


def test_date_to_numeric_monthYear():
    input_row = "Mai 13"
    expected = "13.05"
    actual = date_to_numeric(input_row)

    assert expected == actual


def test_date_to_numeric_dayMonth():
    input_row = "13. Mai"
    expected = "13.05"
    actual = date_to_numeric(input_row)

    assert expected == actual
