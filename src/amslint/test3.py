
class Identifier():

    name: str
    type_: str
    declared_at: int
    to_from: int

    def __init__(self, name: str, type_: str, declared_at: int = -1, ends_at: int = -1):
        self.name = name
        self.type_ = type_
        self.declared_at = declared_at
        self.ends_at = ends_at


class FileContents():
    
    contents: list[tuple[(int, list[str])]]
    identifiers: list[Identifier]

    def __init__(self, contents) -> None:
        self.contents = [(i+1, line) for i, line in enumerate(contents)]
        self.identifiers = self.__make_list(contents)
        for ident in self.identifiers:
            ident.declared_at, ident.ends_at = self.__find_declaration_line_number(ident)

    def __find_declaration_line_number(self, ident: Identifier):
        decl_line_number = -1
        end_line_number = -1
        
        for idx, line in self.contents:
            if f'{ident.type_} {ident.name} {{\n' in line:
                decl_line_number = idx
                break
        
        lvl = len(self.contents[decl_line_number-1][1]) - len(self.contents[decl_line_number-1][1].lstrip('\t'))

        for idx, line in self.contents:
            if idx <= decl_line_number:
                continue
            end_tag = '\t'*lvl + '}'
            if end_tag == line.removesuffix('\n'):
                end_line_number = idx
                break

        return decl_line_number, end_line_number


    def __make_list(self, code, lst: list=None, indent_lvl: int=0, indent_bumb: int=1):
        if lst == None:
            lst = []
        
        if isinstance(code, list):
            code = '\n'.join(code)

        re_id = r'(?s)(?:^|\n)\s{'+str(indent_lvl)+'}(\w+)\s(\w*)\s\{\n(\s+.+?)\n\s{'+str(indent_lvl)+'}\}'
        for match in re.finditer(re_id, code):
            ident = Identifier(match.groups()[1], match.groups()[0])
            
            att_lst = []
            re_oneLineAttb_id = r'(?s)(?:\n)\s{'+str(indent_lvl+indent_bumb)+'}(\w+):\s(?!{\n)(.+?);'
            a = match.groups()[2]
            for attMatch in re.finditer(re_oneLineAttb_id, a):
                att_lst.append({
                    'name' : attMatch.groups()[0],
                    'value' : attMatch.groups()[1],
                    'type' : 'singleLine',
                })
            b = match.groups()[2]
            re_multiLineAttb_id = r'(?s)(?:^|\n)\s{'+str(indent_lvl+indent_bumb)+'}(\w+):\s\{\n\s+(.+?)\n\s{'+str(indent_lvl+indent_bumb)+'}\}'
            for attMatch in re.finditer(re_multiLineAttb_id, b):
                att_lst.append({
                    'name' : attMatch.groups()[0],
                    'value' : attMatch.groups()[1],
                    'type' : 'multiLine',
                })
            
            ident.attributes = att_lst
            lst.append(ident)
            lst = self.__make_list(match.groups()[2], lst, indent_lvl=indent_lvl+indent_bumb, indent_bumb=indent_bumb)

        return lst

    
import re

# with open('src/amslint/ams.ams') as f:
with open('basic/MainProject/basic.ams') as f:
    indented_text = f.readlines()

aaa = FileContents(indented_text)

pass

