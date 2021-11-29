import enum


class Message():


    class MessageSeverity(enum.Enum):
        CRITICAL = enum.auto()
        HIGH = enum.auto()
        MEDIUM = enum.auto()
        LOW = enum.auto()
    

    class MessageType(enum.Enum):
        VULNERABILITY = enum.auto()
        CODE_SMELL = enum.auto()
        BUG = enum.auto()
        
    __id: str
    __title: str
    __summary: str
    __details: str
    __type: MessageType
    __severity: MessageSeverity
    __path: str
    __line: int


    def title(self) -> str:
        return self.__title


    def __init__(
        self, title: str, summary: str, details: str, type: MessageType,
        severity: MessageSeverity, path: str, line: int, id: str = None
    ) -> None:
        
        self.__id = id if id else ""
        self.__title = title
        self.__summary = summary
        self.__details = details
        self.__type = type
        self.__severity = severity
        self.__path = path
        self.__line = line


    def get_as_dict(self) -> dict:
        return {
            "external_id": self.__id,
            "title": self.__title,
            "annotation_type": self.__type.name,
            "summary": self.__summary,
            "details": self.__details,
            "severity": self.__severity.name,
            "path": self.__path,
            "line": self.__line,
        }


    def __str__(self) -> str:
        return str(self.get_as_dict())


class ReportData():


    class ReportDataType(enum.Enum):
        BOOLEAN = enum.auto()
        DATE = enum.auto()
        DURATION = enum.auto()
        LINK = enum.auto()
        NUMBER = enum.auto()
        PERCENTAGE = enum.auto()
        TEXT = enum.auto()


    __type: ReportDataType
    __title: str
    __value: None


    def __init__(self, title: str, type: ReportDataType, value: str) -> None:
        if not self._check_value_format(type, value):
            raise ValueError("Invalid value type")

        self.__title = title
        self.__type = type
        self.__value = value


    def _check_value_format(self, type: ReportDataType, value: str) -> bool:
        if ((type == self.ReportDataType.NUMBER and isinstance(value, float))
            or (type == self.ReportDataType.PERCENTAGE and isinstance(value, float))
            or (type == self.ReportDataType.DURATION and isinstance(value, float))
            or (type == self.ReportDataType.DATE and isinstance(value, str))
            or (type == self.ReportDataType.BOOLEAN and isinstance(value, bool))
            or (type == self.ReportDataType.LINK and isinstance(value, str))
            or (type == self.ReportDataType.TEXT and isinstance(value, str))):
            return True
        else:
            return False


    def __str__(self) -> str:
        return str(self.get_as_dict())


    def get_as_dict(self) -> dict:
        return {
            "title": self.__title,
            "type": self.__type.name,
            "value": self.__value,
        }



class Report():


    class ReportType(enum.Enum):
        SECURITY = enum.auto()
        COVERAGE = enum.auto()
        TEST = enum.auto()
        BUG = enum.auto()


    class ResultType(enum.Enum):
        PASSED = enum.auto()
        FAILED = enum.auto()
        PENDING = enum.auto()

    
    __id: str
    __title: str
    __details: str
    __type: ReportType
    __reporter: str
    __result: ResultType
    __report_data: list[ReportData]
    __messages: list[Message]


    def __init__(
        self, title: str, details: str, type: ReportType, reporter: str,
        result: ResultType, id: str = None, messages: list[Message] = None
    ) -> None:
        
        self.__id = id if id else ""
        self.__title = title
        self.__details = details
        self.__type = type
        self.__reporter = reporter
        self.__result = result
        self.__messages = messages if messages else []
    

    def get_as_dict(self) -> dict:
        return {
            "title": self.__title,
            "details": self.__details,
            "report_type": self.__type.name,
            "reporter": self.__reporter,
            "result": self.__result.name,
            "data": [item.get_as_dict() for item in self.__report_data],
        }


    def __str__(self) -> str:
        return str(self.get_as_dict())
