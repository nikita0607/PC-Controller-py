from abc import ABC, abstractmethod, ABCMeta
from typing import List

from . import error


class IsInstanceMeta(ABCMeta):
    def __eq__(self, other):
        return self.eq(other)


class CallingMethod(ABC):
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass


class AnyMethod(CallingMethod):
    def __eq__(self, other):
        return True

    def __str__(self):
        return "any"


class ServerResult(ABC):
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass


class BoolServerResult(ServerResult):
    def __eq__(self, other):
        return isinstance(other, bool)

    def __str__(self):
        return "bool"


class DictServerResult(ServerResult):
    def __eq__(self, other):
        return isinstance(other, dict)

    def __str__(self):
        return "dict"


class AneServerResult(ServerResult):
    def __eq__(self, other):
        return True

    def __str__(self):
        return "any"


class ResultABC(ABC, metaclass=IsInstanceMeta):

    method = AnyMethod()
    result = "error"

    @abstractmethod
    def __init__(self, _raw: dict):
        self._raw = _raw

    @classmethod
    def check(cls, method, _result) -> bool:
        return cls.method == method and cls.result == _result

    @classmethod
    def eq(cls, other):
        return type(other) is cls

    def __str__(self):
        return self.__class__.__name__ + f"(called_method={self.method}, result={self.result})"

    def __getitem__(self, item):
        return self._raw[item]


class ResultTypes:
    results: List[ResultABC] = []

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

    def __new__(cls, called_method: str, _raw: dict) -> ResultABC:
        return ResultTypes.find_result_object(called_method, _raw["result"])(_raw)


@ResultTypes.result
class ResultError(ResultABC):
    def __init__(self, _raw: dict):
        super().__init__(_raw)
        self.errors = list(map(error.ErrorFabric.gen_error, _raw["errors"]))

    def raise_error(self):
        raise self.errors[0]

    def __str__(self):
        return super().__str__()[:-1] + f", errors={self.errors})"


@ResultTypes.result
class ResultConnect(ResultABC):
    method = "computer.connect"
    result = BoolServerResult()

    def __init__(self, _raw: dict):
        super().__init__(_raw)

    def __str__(self):
        return super().__str__()


@ResultTypes.result
class ResultInfo(ResultABC):
    method = "computer.get_info"
    result = DictServerResult()

    def __init__(self, _raw):
        super().__init__(_raw)

    def __str__(self):
        return super().__str__()[:-1] + f", result_dict={self._raw['result']})"

    def result_dict(self):
        return self._raw["result"]


@ResultTypes.result
class ResultEmpty(ResultABC):
    result = AneServerResult()

    def __init__(self, _raw):
        super().__init__(_raw)

    def __str__(self):
        return "Result(Empty)"
