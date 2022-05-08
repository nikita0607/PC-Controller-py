from abc import ABC, abstractmethod, ABCMeta
from typing import List, Type

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

class ListServerResult(ServerResult):
    def __eq__(self, other):
        return isinstance(other, list)
    def __str__(self):
        return "list"


class AnyServerResult(ServerResult):
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
    results: List[Type[ResultABC]] = []

    @classmethod
    def result(cls, result_cls):
        cls.results.append(result_cls)
        return result_cls

    @classmethod
    def find_result_object(cls, method, result) -> Type[ResultABC]:
        for res in cls.results:
            if res.check(method, result):
                return res


class ResultFabric:

    def __new__(cls, called_method: str, _raw: dict) -> ResultABC:
        return ResultTypes.find_result_object(called_method, _raw["result"])(_raw)


class ResultOnlyBool(ResultABC):
    result = BoolServerResult()

    def __init__(self, _raw: dict):
        super().__init__(_raw)
        self.status = _raw["result"]

    def __str__(self):
        return super().__str__()[:-1] + f", status={self.status})"


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
class ResultConnect(ResultOnlyBool):
    method = "computer.connect"


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
class ResultButtonClick(ResultOnlyBool):
    method = "computer.button.click"


@ResultTypes.result
class ResultEvents(ResultABC):
    method = "computer.get_events"
    result = ListServerResult()

    def __init__(self, _raw):
        super().__init__(_raw)

    def __str__(self):
        return super().__str__()[:-1] + f", events={self._raw['result']})"

    def events_list(self):
        return self._raw['result']


@ResultTypes.result
class ResultComputers(ResultABC):
    method = "user.get_computers"
    result = ListServerResult()

    def __init__(self, _raw):
        super().__init__(_raw)

    def __str__(self):
        return super().__str__()[:-1] + f", computers={self._raw['result']})"

    @property
    def computers(self):
        return self._raw["result"]


@ResultTypes.result
class ResultEmpty(ResultABC):
    result = AnyServerResult()

    def __init__(self, _raw):
        super().__init__(_raw)

    def __str__(self):
        return "Result(Empty)"
