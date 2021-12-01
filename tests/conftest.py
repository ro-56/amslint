import pytest

from amslint.utils.buildingblocks import Identifier, FileContents
from amslint.reports.handlers import Annotation, Report
from amslint.constants import TAG_IGNORE


@pytest.fixture
def basic_ams_file():
    ams_file = [
        '## ams_version=1.0\n',
        '\n',
        'Model Main_basic {\n',
        '	Section Private_Section;\n',
        '}\n',
    ]
    identifiers = [
        Identifier(name='Main_basic', type='Model', declared_at=3, ends_at=5),
        Identifier(name='Main_basic', type='Model', declared_at=4, ends_at=4)
    ]
    return ams_file, FileContents(ams_file, filename="ams_file.ams"), identifiers

@pytest.fixture
def basic_identifier():
    return Identifier(name='Basic_Identifier', type='Parameter', declared_at=1, ends_at=1)

@pytest.fixture
def basic_report():
    report = Report(
        title='Basic Report', details='Basic Report Description',
        type='BUG', reporter='Basic Reporter', id=None, messages=None
    )
    return report


@pytest.fixture
def basic_annotation_low():
    annotation = Annotation(
        title='Basic Annotation (low severity)', summary='Basic Annotation',
        details='Basic Annotation Description',
        type='CODE_SMELL', severity="LOW", path='', line=None, id=None
    )
    return annotation

@pytest.fixture
def basic_indentifier_variable(basic_identifier):
    attributes = [
        {
            'name': 'Comment',
            'value': TAG_IGNORE,
            'type': 'singleline',
        }
    ]
    basic_identifier.add_attribute(attributes)
    return basic_identifier