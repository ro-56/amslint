import pytest

from amslint.utils.buildingblocks import Identifier
from amslint.reports.handlers import Message, Report


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
        Identifier(name='Main_basic', type_='Model', declared_at=3, ends_at=5),
        Identifier(name='Main_basic', type_='Model', declared_at=4, ends_at=4)
    ]
    return ams_file, identifiers


@pytest.fixture
def basic_report():
    report = Report(
        title='Basic Report', details='Basic Report Description', 
        type='BUG', reporter='Basic Reporter', id=None, messages=None
    )
    return report


@pytest.fixture
def basic_message_low():
    message = Message(
        title='Basic Message (low severity)', summary='Basic Message', details='Basic Message Description',
        type='CODE_SMELL', severity="LOW", path='', line=None, id=None
    )
    return message