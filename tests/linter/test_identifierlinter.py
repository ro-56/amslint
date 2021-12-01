import pytest

from amslint.lint.linter import IdentifierLinter

def test_IdentifierLinter_variable_linting(basic_ams_file, basic_indentifier_variable):
    _, fileContents, _ = basic_ams_file
    fileContents.identifiers.append(basic_indentifier_variable)
    linter = IdentifierLinter(files=[fileContents])
    linter.analyze_files()
    a = linter.get_messages()[0]

    expected_message = 'path:ams_file.ams | location:1 | code:A000'
    assert a == expected_message

# def test_IdentifierLinter_variable_linting(basic_ams_file, basic_indentifier_variable):
#     _, fileContents, _ = basic_ams_file
#     fileContents.identifiers.append(basic_indentifier_variable)
#     linter = IdentifierLinter(files=[fileContents])
#     linter.analyze_files()
#     a = linter.get_messages()[0]

#     expected_message = 'path:ams_file.ams | location:1 | code:A000'
#     assert a == expected_message





# "EDIT THIS TEST | WIP"
# from amslint.utils.buildingblocks import Identifier, FileContents
# from amslint.constants import TAG_IGNORE

# ams_file = [
#         '## ams_version=1.0\n',
#         '\n',
#         'Model Main_basic {\n',
#         '	Section Private_Section;\n',
#         '}\n',
#     ]

# aa = FileContents(ams_file, filename="ams_file.ams")
# attributes = [
#         {
#             'name': 'Commrnt',
#             'value': TAG_IGNORE,
#             'type': 'singleline',
#         }
#     ]
# bb = Identifier(name='basic_variable', type='Variable', declared_at=1, ends_at=3, attributes=attributes)
# test_IdentifierLinter_variable_linting(['', aa, ''], bb)