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

    async def click(self, button_name: str, for_name: str = None):

        data = {"method": "computer.button.click",
                "button_name": button_name}
        if for_name:
            data["for_name"] = for_name

        return await self.call(**data)


class ComputerMethods(Method):
    """
    Contains computer methods
    """

    event_start_id = 0

    async def get_computers(self):
        """
        Get computers of this user
        """

        return await self.call("user.get_computers")

    async def connect(self):
        """
        Connect to server
        """
        _result = await self.call("computer.connect")
        print(_result)
        if _result.result != "error":
            self.parrent.c_hash_key = _result["c_hash_key"]
        return _result

    async def get_info(self, raise_error: bool = False, for_name: str = None):
        """
        Get info about connected computers
        :param raise_error: Raise error from server
        :return: None
        """
        data = {"method": "computers.get_info"}
        if for_name:
            data["for_name"] = for_name

        return await self.call(**data, raise_error=raise_error)
    
    async def get_events(self, raise_error: bool = False, start_id: int = None, for_name: str = None):
        """
        Get computer events from server
        :param raise_error: Raise error from server
        :param start_id: Get events from this id to end
        :param for_name: Call this method for computer with this name
        :return: None
        """
        if start_id is None:
            start_id = self.event_start_id+1

        data = {"method": "computer.get_events",
                "raise_error": raise_error,
                "start_id": start_id}

        if for_name:
            data["for_name"] = for_name
        
        res: Union[ResultEvents, ResultError] = await self.call(**data)

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
