from amslint.utils.buildingblocks import FileContents
from amslint.reports.handlers import Report, Annotation
from amslint.messages.handler import MessageHandler


class BasicLinter():

    __files: list[FileContents]
    __message_handler: MessageHandler

    def __init__(self, files: list[FileContents]) -> None:
        self.__files = files
        self.__message_handler = MessageHandler()

    @staticmethod
    def message_handler(self):
        return self.__message_handler

    @staticmethod
    def analyze_files(self) -> None:
        for file in self.__files:
            self.__analyze_file(file)
        return None
    
    @staticmethod
    def get_messages(self):
        return self.__message_handler.get_messages()

    def __analyze_file(self, file: FileContents) -> None:
        """Should be implemented at every subclass"""
        pass
