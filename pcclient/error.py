from typing import Type


class Error(ValueError):
    loc = ""
    type = "unknown_error"
    code = 0

    def __init__(self, loc: str = "", msg: str = ""):
        self.loc = loc
        super().__init__(msg)


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
class UnknownError(Error):
    code = 0
    type = "unknown_error"


@ErrorTypes.error
class NameBusy(Error):
    code = 1
    type = "name_busy"
