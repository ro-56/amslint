import enum


class Annotation():


    class AnnotationSeverity(enum.Enum):
        """Possible types:
        CRITICAL, HIGH, MEDIUM, LOW
        """
        CRITICAL = 4
        HIGH = 3
        MEDIUM = 2
        LOW = 1
    

    class AnnotationType(enum.Enum):
        """Possible types:
        VULNERABILITY, CODE_SMELL, BUG
        """
        VULNERABILITY = enum.auto()
        CODE_SMELL = enum.auto()
        BUG = enum.auto()
        
    __id: str
    __title: str
    __summary: str
    __details: str
    __type: AnnotationType
    __severity: AnnotationSeverity
    __path: str
    __line: int


    def title(self) -> str:
        return self.__title


    def __init__(
        self, title: str, summary: str, details: str, type: str,
        severity: str, path: str, line: int, id: str = None
    ) -> None:
        
        if severity not in Annotation.AnnotationSeverity.__members__:
            raise ValueError(f"Invalid severity: {severity}")
        
        if type not in Annotation.AnnotationType.__members__:
            raise ValueError(f"Invalid type: {type}")

        self.__id = id if id else ""
        self.__title = title
        self.__summary = summary
        self.__details = details
        self.__type = Annotation.AnnotationType[type]
        self.__severity = Annotation.AnnotationSeverity[severity]
        self.__path = path
        self.__line = line


    def get_as_dict(self) -> dict:
        return {
            "external_id": self.__id,
            "title": self.__title,
            "annotation_type": self.__type.name if self.__type else None,
            "summary": self.__summary,
            "details": self.__details,
            "severity": self.__severity.name if self.__severity else None,
            "path": self.__path,
            "line": self.__line,
        }


    def __str__(self) -> str:
        return str(self.get_as_dict())


class ReportData():


    class ReportDataType(enum.Enum):
        """Possible types:
        BOOLEAN, DATE, DURATION, LINK, NUMBER, PERCENTAGE, TEXT
        """
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
        """Possible types:
        SECURITY, COVERAGE, TEST, BUG
        """
        SECURITY = enum.auto()
        COVERAGE = enum.auto()
        TEST = enum.auto()
        BUG = enum.auto()


    class ResultType(enum.Enum):
        """Possible types:
        PASSED, FAILED, PENDING
        """
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
    __messages: list[Annotation]


    def __init__(
        self, title: str, details: str, type: str, reporter: str,
        id: str = None, messages: list[Annotation] = None
    ) -> None:
        
        if type not in Report.ReportType.__members__:
            raise ValueError(f"Invalid type: {type}")

        self.__id = id if id else ""
        self.__title = title
        self.__details = details
        self.__type = Report.ReportType[type]
        self.__reporter = reporter
        self.__result = self.ResultType.PENDING
        self.__report_data = []
        self.__messages = messages if messages else []

        self.__passing_threshold = 2
    

    def get_as_dict(self) -> dict:
        return {
            "title": self.__title,
            "details": self.__details,
            "report_type": self.__type.name if self.__type else None,
            "reporter": self.__reporter,
            "result": self.__result.name if self.__result else None,
            "data": [item.get_as_dict() for item in self.__report_data],
        }


    def update_and_get_as_dict(self) -> dict:
        self.update_report_result()
        return self.get_as_dict()
    

    def update_report_result(self) -> None:
        for message in self.__messages:
            if message.severity > self.__passing_threshold:
                self.__result = Report.ResultType.FAILED
                return None
        self.__result = Report.ResultType.PASSED
        return None


    def __str__(self) -> str:
        return str(self.get_as_dict())
