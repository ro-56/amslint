import pytest

from amslint.reports.handlers import Report


def test_basic_report_1(basic_report):
    expected_report_representation = {
        'title': 'Basic Report',
        'details': 'Basic Report Description',
        'report_type': 'BUG',
        'reporter': 'Basic Reporter',
        'result': "PENDING",
        'data': []
    }
    assert basic_report.get_as_dict() == expected_report_representation


def test_report_passed_with_no_messages(basic_report):
    assert basic_report.update_and_get_as_dict()['result'] == 'PASSED'


def test_report_invalid_type(basic_report):
    report_template = basic_report.get_as_dict()
    with pytest.raises(ValueError):
        Report(
            title=report_template['title'],
            details=report_template['details'],
            type='INVALID_TYPE',
            reporter=report_template['reporter'],
        )
