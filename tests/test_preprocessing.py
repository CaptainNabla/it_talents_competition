import pytest
import pandas as pd

from data.preprocessing import date_to_numeric


def test_date_to_numeric_ignoreInput():
    expected = "1.34"
    actual = date_to_numeric(expected)

    assert expected == actual


def test_date_to_numeric_returnTranslation():
    input_row = "01 Mai"
    expected = "01.05"
    actual = date_to_numeric(input_row)

    assert expected == actual
