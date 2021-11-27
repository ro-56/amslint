import re


class Identifier():
    """Identifier object
    Used to store identifiers information on a easy to use way
    """
    name: str
    type_: str
    declared_at: int
    to_from: int
    attributes: list

    def __init__(self, name: str, type_: str, declared_at: int = -1, ends_at: int = -1, attributes: list = None):
        self.name = name
        self.type_ = type_
        self.declared_at = declared_at
        self.ends_at = ends_at
        self.attributes = attributes if attributes else [] 
    
    def __eq__(self, other) : 
        if other.__class__ is self.__class__: 
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


class FileContents():
    """FileContents object
    Used to store file contents information on a easy to use way
    """
    
    contents: list[tuple[(int, list[str])]]
    identifiers: list[Identifier]

    def __init__(self, contents) -> None:
        self.contents = [(i+1, line) for i, line in enumerate(contents)]
        self.identifiers = self.__make_list(contents)
        for ident in self.identifiers:
            ident.declared_at, ident.ends_at = self.__find_declaration_line_number(ident)

    def __find_declaration_line_number(self, ident: Identifier):
        """Finds the specific line in the file where the Identifier ident was declared"""
        declaration_line = -1
        end_line = -1
        
        for idx, line in self.contents:
            if f'{ident.type_} {ident.name} {{\n' in line:
                declaration_line = idx
                break
            elif f'{ident.type_} {ident.name};' in line:
                declaration_line = idx
                end_line = idx
                return declaration_line, end_line
        
        lvl = len(self.contents[declaration_line-1][1]) - len(self.contents[declaration_line-1][1].lstrip('\t'))

        for idx, line in self.contents:
            if idx < declaration_line:
                continue
            end_tag = '\t'*lvl + '}'
            if end_tag == line.removesuffix('\n'):
                end_line = idx
                break

        return declaration_line, end_line


    def __make_list(self, file_contents, identifier_list: list=None, indent_lvl: int=0, indent_bumb: int=1):
        if identifier_list == None:
            identifier_list = []
        
        if isinstance(file_contents, list):
            file_contents = '\n'.join(file_contents)

        regex_one_line_identifier = r'(?s)(?:^|\n)\s{'+str(indent_lvl)+'}(\w+)\s(\w*);'
        for match in re.finditer(regex_one_line_identifier, file_contents):
            identifier = Identifier(match.groups()[1], match.groups()[0])
            identifier_list.append(identifier)
        
        regex_multi_line_identifier = r'(?s)(?:^|\n)\s{'+str(indent_lvl)+'}(\w+)\s(\w*)\s\{\n(\s+.+?)\n\s{'+str(indent_lvl)+'}\}'
        for match in re.finditer(regex_multi_line_identifier, file_contents):
            identifier = Identifier(match.groups()[1], match.groups()[0])
            
            attrib_list = []
            regex_one_line_attrib = r'(?s)(?:\n)\s{'+str(indent_lvl+indent_bumb)+'}(\w+):\s(?!{\n)(.+?);'
            identifier_contents = match.groups()[2]
            for attrib_match in re.finditer(regex_one_line_attrib, identifier_contents):
                attrib_list.append({
                    'name' : attrib_match.groups()[0],
                    'value' : attrib_match.groups()[1],
                    'type' : 'singleLine',
                })
            regex_multi_line_attrib = r'(?s)(?:^|\n)\s{'+str(indent_lvl+indent_bumb)+'}(\w+):\s\{\n\s+(.+?)\n\s{'+str(indent_lvl+indent_bumb)+'}\}'
            for attrib_match in re.finditer(regex_multi_line_attrib, identifier_contents):
                attrib_list.append({
                    'name' : attrib_match.groups()[0],
                    'value' : attrib_match.groups()[1],
                    'type' : 'multiLine',
                })
            
            identifier.attributes = attrib_list
            identifier_list.append(identifier)
            identifier_list = self.__make_list(match.groups()[2], identifier_list, indent_lvl=indent_lvl+indent_bumb, indent_bumb=indent_bumb)

        return identifier_list