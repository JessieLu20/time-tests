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


# Multiple tests
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


# negative test
def test_bad():
    # an alternative sloution!
    expected_error_message = (
        "The end of the range has to come strictly after its start."
    )
    with pytest.raises(ValueError, match=expected_error_message):
        time_range("2010-01-12 10:00:00", "2010-01-12 09:00:00")


# Avoid code repetition with parametrize
@pytest.mark.parametrize(
    "first_range, second_range, expected_overlap",
    [
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
            [
                ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
                ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
            ],
        ),
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
            time_range("2010-01-12 12:30:00", "2010-01-12 12:45:00", 2, 60),
            [],
        ),
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 13:00:00", 3, 900),
            time_range("2010-01-12 10:40:00", "2010-01-12 11:20:00", 2, 120),
            [
                ("2010-01-12 10:40:00", "2010-01-12 10:50:00"),
                ("2010-01-12 11:05:00", "2010-01-12 11:20:00"),
            ],
        ),
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
            time_range("2010-01-12 11:00:00", "2010-01-12 12:45:00"),
            [],
        ),
    ],
)
def test_time_range_overlap(first_range, second_range, expected_overlap):
    result = compute_overlap_time(first_range, second_range)
    assert (
        result == expected_overlap
    ), f"Expected: {expected_overlap}, but Result: {result}, doesn't match!"


