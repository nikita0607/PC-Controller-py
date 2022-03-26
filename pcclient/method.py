from .result import ResultABC, ResultError, ResultEvents
from typing import Union

class Methods:
    """
    Contains all available methods
    """

    def __init__(self, parrent_api, broadcast: bool = False):
        self.button = ButtonMethods(parrent_api, broadcast)
        self.computer = ComputerMethods(parrent_api, broadcast)


class Method:
    """
    Parent of methods group
    """

    def __init__(self, parent_api, broadcast: bool = True):
        self.parrent = parent_api
        self.broadcast = broadcast

    async def call(self, method: str, **data) -> ResultABC:
        """
        Call method
        :param method: Method type
        :param data: Additional data
        :return:
        """
        return await self.parrent.call_method(method, **data)


class ButtonMethods(Method):
    """
    Contains button methods
    """

    async def add(self, button_name: str, button_text: str):
        """
        Add button in to computer in dashboard
        :param button_name: If button is clicked, then server returns this name
        :param button_text: Text of button
        :return: Actions from server
        """

        data = {"button_name": button_name, "button_text": button_text}

        return await self.call("computer.button.add", **data)

    async def click(self, button_name: str):

        data = {"button_name": button_name}

        return await self.call("computer.button.click", **data)


class ComputerMethods(Method):
    """
    Contains computer methods

    """

    event_start_id = 0

    async def connect(self):
        _result = await self.call("computer.connect")
        if _result.result != "error":
            self.parrent.hash_key = _result["hash_key"]
        return _result

    async def get_info(self, raise_error: bool = False, start_id=None):
        return await self.call("computer.get_info", raise_error=raise_error)
    
    async def get_events(self, raise_error: bool = False, start_id=None):
        if start_id is None:
            start_id = self.event_start_id+1
        
        res: Union[ResultEvents, ResultError] = await self.call(
                method="computer.get_events", 
                raise_error=raise_error,
                start_id=start_id)

        if ResultError == res:
            return res
        
        if len(res.events_list()):
            self.event_start_id = res.events_list()[-1]["id"]
        return res

    async def disconnect(self):
        """
        Disconnect this device from server
        :return: Actions from server
        """
        return await self.call("computer.disconnect")
