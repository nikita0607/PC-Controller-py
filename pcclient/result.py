from abc import ABC, abstractmethod, ABCMeta
from . import error


class IsInstanceMeta(ABCMeta):
    def __eq__(self, other):
        return self.eq(other)


class AnyMethod:
    def __eq__(self, other):
        return True

    def __str__(self):
        return "any_method"


class BoolServerResult:
    def __eq__(self, other):
        return isinstance(other, bool)


class AneServerResult:
    def __eq__(self, other):
        return True


class ResultABC(ABC, metaclass=IsInstanceMeta):

    method = AnyMethod()
    result = "error"

    @abstractmethod
    def __init__(self, _raw: dict):
        pass

    @classmethod
    def check(cls, method, _result) -> bool:
        return cls.method == method and cls.result == _result

    @classmethod
    def eq(cls, other):
        return isinstance(other, cls)

    def __str__(self):
        return f"Result(called_method={self.method}, result={self.result})"


class ResultTypes:
    results: list[ResultABC] = []

    @classmethod
    def result(cls, result_cls):
        cls.results.append(result_cls)
        return result_cls

    @classmethod
    def find_result_object(cls, method, result) -> ResultABC:
        for res in cls.results:
            if res.check(method, result):
                return res


class ResultFabric:

    @classmethod
    def __new__(cls, called_method: str, _raw: dict) -> ResultABC:
        return ResultTypes.find_result_object(called_method, _raw["result"])(_raw)


@ResultTypes.result
class ResultError(ResultABC):
    def __init__(self, _raw: dict):
        self.errors = list(map(error.ErrorFabric.gen_error, _raw["errors"]))

    def raise_error(self):
        raise self.errors[0]

    def __str__(self):
        return super().__str__()[:-1] + f"errors={self.errors})"


@ResultTypes.result
class ResultEmpty(ResultABC):
    result = AneServerResult()

    def __init__(self, _raw):
        pass

    def __str__(self):
        return "Result(Empty)"
