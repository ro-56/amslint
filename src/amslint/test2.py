import enum

class IdentifierType(enum.Enum):
    """"""

    # SET = ''
    # CALENDAR = ''
    # HORIZON = ''
    # INDEX = ''
    # PARAMETER = ''
    ElementParameter = enum.auto()
    StringParameter = enum.auto()
    # UNIT_PARAMETER = ''
    # VARIABLE = ''
    # ELEMENT_VARIABLE = ''
    # COMPLEMENTARITY_VARIABLE = ''
    # CONSTRAINT = ''
    # ARC = ''
    # NODE = ''
    # UNCERTAINTY_VARIABLE = ''
    # UNCERTAINTY_CONSTRAINT = ''
    # ACTIVITY = ''
    # RESOURCE = ''
    # MATHEMATICAL_PROGRAM = ''
    # MACRO = ''
    # ASSERTION = ''
    # DATABASE_TABLE = ''
    # DATABASE_PROCEDURE = ''
    # FILE = ''
    Procedure = enum.auto()
    Function = enum.auto()
    # QUANTITY = ''
    # CONVENTION = ''
    LibraryModule = enum.auto()
    # MODULE = ''
    Section = enum.auto()
    # DECLARATION = ''


class Identifier():

    name: str
    type_: IdentifierType
    declared_at: int

    def __init__(self, name: str, type_: IdentifierType, declared_at: int = -1):
        self.name = name
        self.type_ = type_
        self.declared_at = declared_at


class FileContents():
    
    contents: list[tuple[(int, list[str])]]
    contents_json: dict
    identifiers: list[Identifier]

    def __init__(self, contents) -> None:
        self.contents = [(i, line) for i, line in enumerate(contents)]
        self.contents_json = make_list(self.__str_list_to_str(contents))
        self.identifiers = self.__get_identifiers_from_dict(self.contents_json)
        for ident in self.identifiers:
            ident.declared_at = self.__find_declaration_line_number(ident)

    def __get_identifiers_from_dict(self, code, identifiers_list = None):
        if identifiers_list == None:
            identifiers_list = []
        for itm in code:
            identifiers_list.append(Identifier(itm['name'], IdentifierType[itm['type']]))
            if 'child' in itm:
                self.__get_identifiers_from_dict(itm['child'], identifiers_list)
        return identifiers_list
    
    def __str_list_to_str(self, lst):
        return '\n'.join(lst)
    
    def __str_to_str_list(self, str):
        return str.split('\n')
    
    def __find_declaration_line_number(self, ident: Identifier):
        for idx, line in self.contents:
            if f'{ident.type_.name} {ident.name} {{\n' in line:
                return idx
        return -1
    

import re
def make_list(code, indent_level=0, indent_bumb=1):
    ID_list = []
    re_id = r'(?s)(?:^|\n)\s{'+str(indent_level)+'}(\w+)\s(\w*)\s\{\n(\s+.+?)\n\s{'+str(indent_level)+'}\}'
    for match in re.finditer(re_id, code):
        itm = {
            'type': match.groups()[0],
            'name': match.groups()[1],
            }
        # re_oneLineAttb_id = r'(?s)(?:\n)\s{'+str(indent_level+indent_bumb)+'}(\w+):\s(\w+);'
        # a = match.groups()[2]
        # for attMatch in re.finditer(re_oneLineAttb_id, a):
        #     itm[attMatch.groups()[0]] = attMatch.groups()[1]
        
        # b = match.groups()[2]
        # re_multiLineAttb_id = r'(?s)(?:^|\n)\s{'+str(indent_level+indent_bumb)+'}(\w+):\s\{\n\s+(.+?)\n\s{'+str(indent_level+indent_bumb)+'}\}'
        # for attMatch in re.finditer(re_multiLineAttb_id, b):
        #     itm[attMatch.groups()[0]] = attMatch.groups()[1]
        
        itm['child'] = make_list(match.groups()[2], indent_level+indent_bumb, indent_bumb)
        ID_list.append(itm)

    return ID_list


with open('src/amslint/ams.ams') as f:
    indented_text = f.readlines()

aaa = FileContents(indented_text)

pass

