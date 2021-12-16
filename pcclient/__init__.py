"""
This module 
"""

import json

import aiohttp
import asyncio
import contextlib


__version__ = "2.0.0"


def jsonify(data) -> str:
    """
    Transform data to json
    :param data: Object
    :return: JSON strong with object
    """
    return json.dumps(data)


class API:
    """
    Main class for working with pc-controller API
    """

    def __init__(self):
        self.method = Methods(self)

        self.adr = None

        self._main = None

    def run(self, username: str, computer_name: str, _ip: str, hash_key: str = None):
        """
        Initialize connection with server
        :param username: Your user name on web site
        :param computer_name: Name of this device
        :param _ip: Server ip
        :param hash_key: Your hash key
        :return: None
        """
        data = {"username": username, "name": computer_name, "method": "computer.connect"}
        self.adr = f"{_ip}:8000/api"

        asyncio.run(self._run(data))

    async def _run(self, data):
        result = await self.response(data)
        print(result)

        if self._main:
            await self._main()

    async def response(self, data: dict) -> dict:
        """
        Do response on server
        :param data: Data for send
        :return: Actions
        """
        async with aiohttp.ClientSession() as s:
            async with s.post(self.adr, json=data) as resp:
                result = await resp.json()
        return result

    async def call_method(self, method: str, **kwargs) -> dict:
        """
        Call method
        :param method: Calling method
        :param kwargs: Additional data
        :return: Actions
        """
        data = {"method": method}
        data.update(kwargs)

        return await self.response(data)

    @staticmethod
    def main(fn):
        def decorator(*args, **kwargs):
            fn(*args, **kwargs)
        return decorator


class Methods:
    """
    Contains all available methods
    """

    def __init__(self, parrent_api: API, broadcast: bool = False):
        self.button = ButtonMethods(parrent_api, broadcast)
        self.computer = ComputerMethods(parrent_api, broadcast)


class Method:
    """
    Parent of methods group
    """

    def __init__(self, parent_api: API, broadcast: bool = True):
        self.parrent = parent_api
        self.broadcast = broadcast

    async def call(self, method: str, **data) -> dict:
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

        return self.call("computer.button.add", **data)

    async def click(self, button_name: str):

        data = {"button_name": button_name}

        return self.call("computer.button.click")


class ComputerMethods(Method):
    """
    Contains computer methods
    """

    async def disconnect(self):
        """
        Disconnect this device from server
        :return: Actions from server
        """
        return self.call("computer.disconnect")


if __name__ == "__main__":
    pass
