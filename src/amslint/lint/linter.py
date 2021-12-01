from amslint.lint.lintermanager import BasicLinter
from amslint.messages.errorcodes import ErrorCodes
from amslint.utils.buildingblocks import FileContents, Identifier
from amslint.constants import TAG_IGNORE

class IdentifierLinter(BasicLinter):


    def __init__(self, files: list[FileContents]):
        super().__init__(files)
    
    def analyze_files(self):
        print('fas')
        for file in self.files():
            for identifier in file.identifiers:
                if [(attrib.get('name') == 'Comment' 
                    and TAG_IGNORE in attrib.get('value'))
                for attrib in identifier.attributes]:
                    self.add_message(location=identifier.declared_at, path=file.filename, code='E000')
                    return





                # self.__analyze_identifier(identifier)
    
    # def __analyze_identifier(self, identifier: Identifier):
        

        # if identifier.type_ == 'Variable':
        #     if not identifier.attributes.get('name')
        #     pass
