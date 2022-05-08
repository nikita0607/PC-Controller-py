"""
This module 

"""

import asyncio
import json

import aiohttp

from . import error
from . import method
from . import result


__version__ = "2.1.3"


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

    def __init__(self, _ip: str, username: str, name: str, password: str = None, hash_key: str = None):
        self.method = method.Methods(self)

        self.adr = _ip+"/api"

        self._main = None

        self.username = username
        self.name = name
        self.password = password
        self.hash_key = hash_key
        self.c_hash_key = None

    def register(self, password: str) -> result.ResultABC:
        """
        Register new user
        :param password: New password
        :return: Result
        """
        return asyncio.run(self._register(password))

    async def _register(self, password: str) -> result.ResultABC:
        return await self.call_method("user.register", username=self.username, password=password)

    def run(self, raise_error: bool = True, auto_disconnect: bool = True):
        """
        Initialize connection with server
        :param raise_error: Raise error from server
        :param auto_disconnect: Disconnect after work main function
        :return: None
        """
        exp = None
        try:
            asyncio.run(self._run(raise_error, auto_disconnect))
        except BaseException as ex:
            exp = ex

        if auto_disconnect and self.c_hash_key:
            print("Disconnectig")
            asyncio.run(self.method.computer.disconnect())

        if exp:
            raise exp

    async def _run(self, raise_error, auto_disconnect):
        """
        Asyncronyos running main async function
        :param raise_error: Raise error?
        :param auto_disconnect: Autodisconnecting after main function return
        """
        if self.password is None:
            if self.hash_key is None:
                await self.method.computer.connect()

        if self._main:
            listen_events = await self._main()
            if listen_events:
                await self._listen_events()

        else:
            await self._listen_events()

        if auto_disconnect:
            await self.method.computer.disconnect()

    async def _listen_events(self):
        pass

    async def json_info(self) -> dict:
        data = {"username": self.username, "name": self.name}

        if self.password:
            data["password"] = self.password
        else:
            data["hash_key"] = self.hash_key
        
        if self.c_hash_key:
            data["c_hash_key"] = self.c_hash_key

        return data

    async def response(self, data: dict) -> dict:
        """
        Do response on server
        :param data: Data for send
        :return: Actions
        """
        async with aiohttp.ClientSession() as s:
            async with s.post(self.adr, json=data) as resp:
                _result = await resp.json()

        return _result

    async def call_method(self, method: str, raise_error: bool = False, **kwargs) -> result.ResultABC:
        """
        Call method
        :param method: Calling method
        :param raise_error: Raise error
        :param kwargs: Additional data
        :return: Actions
        """
        data = await self.json_info()
        data["method"] = method
        data.update(kwargs)

        _result = await self.response(data)
        _result = result.ResultFabric(method, _result)

        if _result == result.ResultError and raise_error:
            _result.raise_error()

        return _result

    def main(self, fn):
        self._main = fn

        return fn


if __name__ == "__main__":
    pass
