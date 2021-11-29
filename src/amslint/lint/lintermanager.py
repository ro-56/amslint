from amslint.utils.buildingblocks import FileContents
from amslint.reports.handlers import Report, Message


class BasicLinter():

    __report: Report
    __files: list[FileContents]

    def __init__(self, report: Report, files: list[FileContents]) -> None:
        self.__report = report
        self.__files = files


    def report(self) -> Report:
        return self.__report


    def analyze_files(self) -> None:
        for file in self.__files:
            self.__analyze_file(file)
        return None


    def __analyze_file(self, file: FileContents) -> None:
        """Should be implemented at every subclass"""
        pass






# class LinterManager():

#     __file_contents: FileContents
#     __active_linters: list[Linter]


#     def __init__(self, file_contents: FileContents, active_linters: list[Linter] = None, message_handler: MessageHandler = None) -> None:
#         self.__file_contents = file_contents
#         self.__active_linters = active_linters
#         if message_handler is None:
#             self.__message_handler = MessageHandler()
#         else:
#             self.__message_handler = message_handler


#     def analyse_file(self) -> None:
#         for linter in self.__active_linters:
#             linter.analyze(self.__file_contents, self.__message_handler)


#     def set_linters(self, linters: list[Linter]) -> None:
#         self.__active_linters = linters
#         return None


#     def get_active_linters(self) -> list[Linter]:
#         return self.__active_linters


#     def get_filename(self) -> str:
#         return self.__filename