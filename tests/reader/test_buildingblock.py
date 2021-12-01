import pytest

from amslint.utils.buildingblocks import FileContents
from amslint.constants import TAG_IGNORE


def test_get_file_contents(basic_ams_file):
    ams_file, _, _ = basic_ams_file
    expected_contents_format = [(i+1, item) for i, item in enumerate(ams_file)]
    assert FileContents(contents=ams_file).contents == expected_contents_format


def test_get_file_identifiers(basic_ams_file):
    ams_file, _, expected_identifiers = basic_ams_file
    assert FileContents(contents=ams_file).identifiers[0] == expected_identifiers[0]


def test_identifiers_add_attibute_wrong_format(basic_identifier):
    attributes = [
            'Comment',
            TAG_IGNORE,
            'singleline',
        ]
    with pytest.raises(ValueError):
        basic_identifier.add_attribute(attributes)


def test_identifiers_has_attibute(basic_identifier):
    attributes = [
        {
            'name': 'Comment',
            'value': TAG_IGNORE,
            'type': 'singleline',
        }
    ]
    basic_identifier.add_attribute(attributes)
    assert basic_identifier.has_attribute('Comment')
