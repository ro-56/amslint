"""Exception classes used by AmsLint."""


class AmsLintException(Exception):
    """Plain AmsLint exception."""


class ExecutionError(AmsLintException):
    """Exception raised during execution of AmsLint."""