from typing import Type


class Error(Exception):
    loc = ""
    type = "unknown_error"
    code = 0

    def __init__(self, loc: str = "", msg: str = ""):
        self.loc = loc
        self.msg = msg

    def __str__(self):
        return self.__name__+"({self.msg}. Type: {self.type}. Code: {self.code})"


class ErrorTypes:
    types = {}

    @classmethod
    def error(cls, error_cls: Type[Error]):
        cls.types[error_cls.type] = error_cls

        return error_cls

    @classmethod
    def error_from_type(cls, _type: str):
        if _type in cls.types:
            return cls.types[_type]
        return UnknownError


class ErrorFabric:
    @classmethod
    def gen_error(cls, _error: dict):
        loc, msg = _error["loc"], _error["msg"]
        return ErrorTypes.error_from_type(_error["type"])(loc, msg)


@ErrorTypes.error
class MissedValue(Error):
    code = 3
    type = "missed_value"

    def __init__(self, loc, msg):
        super().__init__(loc, msg)
        self.missed_value = loc

    def __str__(self):
        return f"MissedValue('{self.msg}' type: {self.type} missed_value: {self.missed_value})"


@ErrorTypes.error
class NameBusy(Error):
    code = 1
    type = "name_busy"


@ErrorTypes.error
class UnknownError(Error):
    code = 0
    type = "unknown_error"
