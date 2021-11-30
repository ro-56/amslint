import pytest

from amslint.reports.handlers import Annotation


def test_basic_annotation_1(basic_annotation_low):
    expected_annotation_representation = {
        'external_id': '',
        'title': 'Basic Annotation (low severity)',
        'annotation_type': 'CODE_SMELL',
        'summary': 'Basic Annotation',
        'details': 'Basic Annotation Description',
        'severity': 'LOW',
        'path': '',
        'line': None
    }
    assert basic_annotation_low.get_as_dict() == expected_annotation_representation


def test_annotation_invalid_severity(basic_annotation_low):
    annotation_template = basic_annotation_low.get_as_dict()
    with pytest.raises(ValueError):
        Annotation(
            title=annotation_template['title'],
            summary=annotation_template['summary'],
            details=annotation_template['details'],
            type=annotation_template['annotation_type'],
            severity='INVALID_SEVERITY',
            path=annotation_template['path'],
            line=annotation_template['line']
        )


def test_annotation_invalid_type(basic_annotation_low):
    annotation_template = basic_annotation_low.get_as_dict()
    with pytest.raises(ValueError):
        Annotation(
            title=annotation_template['title'],
            summary=annotation_template['summary'],
            details=annotation_template['details'],
            type='INVALID_TYPE',
            severity=annotation_template['severity'],
            path=annotation_template['path'],
            line=annotation_template['line']
        )
