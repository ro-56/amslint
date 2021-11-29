import pytest

from amslint.reports.handlers import Message

def test_basic_message_1(basic_message_low):
    expected_report_representation = {
        'external_id': '', 
        'title': 'Basic Message (low severity)', 
        'annotation_type': 'CODE_SMELL', 
        'summary': 'Basic Message', 
        'details': 'Basic Message Description', 
        'severity': 'LOW', 
        'path': '', 
        'line': None
    }
    assert basic_message_low.get_as_dict() == expected_report_representation

def test_message_invalid_severity(basic_message_low):
    message_template = basic_message_low.get_as_dict()
    with pytest.raises(ValueError):
        Message(
            title=message_template['title'], 
            summary=message_template['summary'], 
            details=message_template['details'],
            type=message_template['annotation_type'], 
            severity='INVALID_SEVERITY', 
            path=message_template['path'], 
            line=message_template['line']
        )


def test_message_invalid_type(basic_message_low):
    message_template = basic_message_low.get_as_dict()
    with pytest.raises(ValueError):
        Message(
            title=message_template['title'], 
            summary=message_template['summary'], 
            details=message_template['details'],
            type='INVALID_TYPE', 
            severity=message_template['severity'], 
            path=message_template['path'], 
            line=message_template['line']
        )