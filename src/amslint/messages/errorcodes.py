import enum


class ErrorCodes():

    class ErrorLevels(enum.Enum):
        CRITICAL = 5
        ERROR = 4
        WARNING = 3
        INFO = 2
        DEBUG = 1

    error_codes = {
        "E001": {
            "description": "Invalid syntax",
            "level": ErrorLevels.ERROR
        }
    }

    def error_message(self, error_code):
        if error_code not in self.error_codes:
            raise Exception("Error code not found")
        return self.error_codes[error_code]
