import pytest

from amslint.utils.buildingblocks import Identifier


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