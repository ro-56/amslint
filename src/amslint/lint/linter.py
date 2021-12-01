from amslint.lint.lintermanager import BasicLinter
from amslint.messages.errorcodes import ErrorLevels
from amslint.utils.buildingblocks import FileContents, Identifier
from amslint.constants import TAG_IGNORE

class IdentifierLinter(BasicLinter):

    error_codes ={
        'A000': {
            'decription': 'Identifier was marked as ignored',
            'level': ErrorLevels.DEBUG
            },
        'A001': {
            'decription': 'Identifier with definition without property NoSave',
            'level': ErrorLevels.WARNING
            }
    }

    def __init__(self, files: list[FileContents]):
        super().__init__(files)
    
    def analyze_files(self):
        print('fas')
        for file in self.files():
            for identifier in file.identifiers:
                ignored = self.check_if_ignored(identifier, file.filename)
                

    def check_if_ignored(self, identifier: Identifier, current_file: str = '') -> bool:

        VALID_TYPES = None
        if VALID_TYPES and identifier.type not in VALID_TYPES:
            return
        
        print([(attrib.get('name') == 'Comment' 
                and TAG_IGNORE in attrib.get('value'))
                for attrib in identifier.attributes])
        if [(attrib.get('name') == 'Comment' 
                and TAG_IGNORE in attrib.get('value'))
                for attrib in identifier.attributes]:
            self.add_message(location=identifier.declared_at, path=current_file, code='A000')
            return
        return False
    
    def check_identifier_defined_nosave(self, identifier: Identifier, current_file: str = '') -> None:
        if [(attrib.get('name') == 'Definition')
                and (attrib.get('name') == 'Property' 
                    and not 'nosave' in attrib.get('value').lower())
                for attrib in identifier.attributes]:
            self.add_message(location=identifier.declared_at, path=current_file, code='A001')

        return


