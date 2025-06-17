from dlt_example.validation.oracle import is_valid_db_object_name

import pytest

test_data = [
    ("select", False),
    ("_", False),
    ("0a", False),
    ("", False),
    ("a___", True),
    ("Space ", False),
    ("Ccaret^", False),
    ("A_string_with_more_than_30chars", False),
    (1, False),
]


@pytest.mark.parametrize("value,validation_result", test_data)
def test_is_valid_relation_name(value, validation_result):
    assert is_valid_db_object_name(value) == validation_result
