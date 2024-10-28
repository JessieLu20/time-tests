# raise ImportError with from .times import *
from times import *
import pytest

def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    result = compute_overlap_time(large, short)
    expected = [
        ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
        ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
    ]
    assert (
        result == expected
    ), f"Expected: {expected}, but Result: {result}, doesn't match!"

def test_no_overlap():
    # wo time ranges that do not overlap
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 08:30:00", "2010-01-12 8:45:00", 2, 60)
    result = compute_overlap_time(large, short)
    expected = []
    assert (
        result == expected
    ), f"Expected: {expected}, but Result: {result}, doesn't match!"

def test_multiple_overlaps():
    # two time ranges that both contain several intervals each
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2, 0)
    short = time_range("2010-01-12 11:00:00", "2010-01-12 13:00:00", 2, 0)
    result = compute_overlap_time(large, short)
    expected = [("2010-01-12 11:00:00", "2010-01-12 12:00:00")]
    assert (
        result == expected
    ), f"Expected: {expected}, but Result: {result}, doesn't match!"

def test_touching_edges():
    # two time ranges that end exactly at the same time when the other starts
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2, 60)
    short = time_range("2010-01-12 12:00:00", "2010-01-12 13:45:00", 2, 60)
    result = compute_overlap_time(large, short)
    expected = []
    assert (
        result == expected
    ), f"Expected: {expected}, but Result: {result}, doesn't match!"

def test_bad():
    with pytest.raises(ValueError):
        time_range("2010-01-12 10:00:00", "2010-01-12 09:00:00")
        