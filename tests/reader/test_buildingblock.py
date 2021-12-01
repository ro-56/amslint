import pytest

from amslint.utils.buildingblocks import FileContents


def test_get_file_contents(basic_ams_file):
    ams_file, _, _ = basic_ams_file
    expected_contents_format = [(i+1, item) for i, item in enumerate(ams_file)]
    assert FileContents(contents=ams_file).contents == expected_contents_format


def test_get_file_identifiers(basic_ams_file):
    ams_file, _, expected_identifiers = basic_ams_file
    assert FileContents(contents=ams_file).identifiers[0] == expected_identifiers[0]
