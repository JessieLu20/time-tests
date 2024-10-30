import yaml
from times import *
import pytest

###
# Separate data and mocking services
# Tests may be more manageable if the data is stored outside the tests. 
# Also, there's no need to be hitting services every time you run your tests.
###

# Separating data from code # issue17
# Create a fixture.yaml file where you can store what you parametrised before
def load_test_yaml():
    with open("./fixture.yaml", "r") as f:
        test_cases = yaml.safe_load(f)
    return test_cases

# Convert YAML data to parametrization format
def load_test_cases():
    test_cases = load_test_yaml()
    for case in test_cases:
        for key, value in case.items():
            expected_results = [tuple(item) for item in value["expected"]]
            yield pytest.param(
                time_range(*value["time_range_1"]),
                time_range(*value["time_range_2"]),
                expected_results,
                id=key
            )
# Parametrize test using YAML data
@pytest.mark.parametrize("first_range, second_range, expected_overlap", load_test_cases())
def test_time_range_overlap_yaml(first_range, second_range, expected_overlap):
    # expected_overlap_tuples = [tuple(item) for item in expected_overlap]
    result = compute_overlap_time(first_range, second_range)
    assert (
        result == expected_overlap
    ), f"Expected: {expected_overlap}, but Result: {result}, doesn't match!"