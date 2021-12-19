import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Atribute():
    type: str
    value: str
    line: int
    multiline: bool = False


@dataclass()
class Identifier():
    """Identifier object
    Used to store identifiers information on a easy to use way
    """
    name: str
    type: str
    line: int
    parent_type: str = ""
    attributes: list[Atribute] = field(default_factory=list)

    def add_attribure(self, type: str, line: int, value: str, multiline: Optional[bool] = None) -> None:
        if multiline:
            self.attributes.append(Atribute(type=type, value=value, line=line, multiline=multiline))
        else:
            self.attributes.append(Atribute(type=type, value=value, line=line))
        return

    def get_attribute(self, type: str) -> Optional[Atribute]:
        for attribute in self.attributes:
            if attribute.type == type:
                return attribute
        return None


@dataclass()
class AMSFile():
    """FileContents object
    Used to store file contents information on a easy to use way
    """

    path: str
    name: str = ""
    content: list[tuple[int, str]] = field(default_factory=list)
    identifiers: list[Identifier] = field(default_factory=list)
    auto_initialize: int = 1

    def __post_init__(self):
        if self.auto_initialize:
            self.initialize()

    def initialize(self) -> None:
        file_content = self._get_contents(self.path)
        self.content = self._enum_file_content(file_content)
        self.identifiers = self._make_list(file_content)
        return

    def _get_contents(self, path: str) -> list[str]:
        with open(path, 'r') as file:
            return file.readlines()

    def _enum_file_content(self, content: list[str]) -> list[tuple[int, str]]:
        res = [(i+1, line) for i, line in enumerate(content)]
        return res

    def _find_identifier_declaration_line_number(self, identifier_name: str, identifier_type: str) -> int:
        """Finds the specific line in the file where the Identifier was declared"""
        declaration_line = -1
        for idx, line in self.content:
            if f'{identifier_type} {identifier_name} {{\n' in line:
                declaration_line = idx
                break
            elif f'{identifier_type} {identifier_name};' in line:
                declaration_line = idx
                break
        return declaration_line

    def _find_identifier_attribute_declaration_line_number(self, identifier: Identifier, attribute_name: str) -> int:
        declaration_line = -1
        for idx, line in self.content[identifier.line:]:
            if f'{attribute_name}: {{\n' in line:
                declaration_line = idx
                break
            elif f'{attribute_name}: ' in line:
                declaration_line = idx
                break
        return declaration_line

    def _make_list(self, file_contents, identifier_list=None, indent_lvl: int = 0, indent_bumb: int = 1, parent_type: str = ""):
        if identifier_list is None:
            identifier_list = []

        if isinstance(file_contents, list):
            file_contents = '\n'.join(file_contents)

        regex_one_line_identifier = r'(?s)(?:^|\n)\s{'+str(indent_lvl)+r'}(\w+)\s(\w*);'
        for match in re.finditer(regex_one_line_identifier, file_contents):
            identifier_type = match.groups()[0]
            identifier_name = match.groups()[1]
            identifier_line = self._find_identifier_declaration_line_number(identifier_name, identifier_type)
            identifier = Identifier(name=identifier_name, type=identifier_type, line=identifier_line, parent_type=parent_type)
            identifier_list.append(identifier)

        regex_multi_line_identifier = r'(?s)(?:^|\n)\s{'+str(indent_lvl)+r'}(\w+)\s(\w*)\s\{\n(\s+.+?)\n\s{'+str(indent_lvl)+r'}\}'
        for match in re.finditer(regex_multi_line_identifier, file_contents):
            identifier_type = match.groups()[0]
            identifier_name = match.groups()[1]
            identifier_line = self._find_identifier_declaration_line_number(identifier_name, identifier_type)
            identifier = Identifier(name=identifier_name, type=identifier_type, line=identifier_line, parent_type=parent_type)

            identifier_contents = match.groups()[2]
            regex_one_line_attrib = r'(?s)(?:\n)\s{'+str(indent_lvl+indent_bumb)+r'}(\w+):\s(?!{\n)(.+?);'
            for attrib_match in re.finditer(regex_one_line_attrib, identifier_contents):
                attribute_type = attrib_match.groups()[0]
                attribute_value = attrib_match.groups()[1]
                attribute_line = self._find_identifier_attribute_declaration_line_number(identifier, attribute_type)
                identifier.add_attribure(type=attribute_type, value=attribute_value, line=attribute_line)

            regex_multi_line_attrib = r'(?s)(?:^|\n)\s{'+str(indent_lvl+indent_bumb)+r'}(\w+):\s\{\n\s+(.+?)\n\s{'+str(indent_lvl+indent_bumb)+r'}\}'
            for attrib_match in re.finditer(regex_multi_line_attrib, identifier_contents):
                attribute_type = attrib_match.groups()[0]
                attribute_value = attrib_match.groups()[1]
                attribute_line = self._find_identifier_attribute_declaration_line_number(identifier, attribute_type)
                identifier.add_attribure(type=attribute_type, value=attribute_value, line=attribute_line, multiline=True)

            identifier_list.append(identifier)
            identifier_list = self._make_list(match.groups()[2], identifier_list, indent_lvl=indent_lvl+indent_bumb,
                                              indent_bumb=indent_bumb, parent_type=identifier_type)

        return identifier_list
