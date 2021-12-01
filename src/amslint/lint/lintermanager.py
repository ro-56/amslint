from amslint.utils.buildingblocks import FileContents
from amslint.reports.handlers import Report, Annotation
from amslint.messages.handler import MessageHandler
from abc import ABC, abstractmethod


class BasicLinter(ABC):

    __files: list[FileContents]
    __message_handler: MessageHandler

    def __init__(self, files: list[FileContents]) -> None:
        self.__files = files
        self.__message_handler = MessageHandler()

    def message_handler(self):
        return self.__message_handler
    
    def files(self):
        return self.__files

    @abstractmethod
    def analyze_files(self):
        """Should be implemented at every subclass"""
        raise NotImplementedError("Must override __analyze_file")
    
    def get_messages(self):
        return self.message_handler().get_messages()
    
    def add_message(self, location: int, path: str, code: str):
        return self.message_handler().add(location=location, path=path, code=code)

