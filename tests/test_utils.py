"""Test cases for utilities module."""

import pytest

from src.utils import sort_by_field


def test_sort_success():
    data = [
        {"issued_at": "2023-01-01T08:00:00.000+05:30"},
        {"issued_at": "2022-09-25T05:30:00.000+05:30"},
        {"issued_at": "2021-06-10T05:30:00.000+05:30"},
    ]
    sorted_data = sort_by_field(data)
    assert sorted_data[0]["issued_at"] == "2023-01-01T08:00:00.000+05:30"
    assert sorted_data[-1]["issued_at"] == "2021-06-10T05:30:00.000+05:30"


def test_sort_missing_key_returns_original():
    data = [
        {"issued_at": "2023-01-01T08:00:00.000+05:30"},
        {"wrong_key": "2022-09-25T05:30:00.000+05:30"},
    ]
    result = sort_by_field(data)
    assert result == data  # unchanged due to KeyError caught inside func


def test_sort_empty_list_returns_empty():
    data = []
    result = sort_by_field(data)
    assert result == []


def test_sort_invalid_field_raises_valueerror():
    data = [{"issued_at": "2023-01-01T08:00:00.000+05:30"}]

    with pytest.raises(ValueError):
        sort_by_field(data, field="invalid_field")
