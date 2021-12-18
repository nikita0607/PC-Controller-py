"""
This module 
"""

import asyncio
import json

import aiohttp

from . import error
from . import method
from . import result

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

    def __init__(self, username: str, name: str, password: str = None, hash_key: str = None):
        self.method = method.Methods(self)

        self.adr = None

        self._main = None

        self.username = username
        self.name = name
        self.password = password
        self.hash_key = hash_key

    def run(self, _ip: str, raise_error: bool = True):
        """
        Initialize connection with server
        :param _ip: Server ip
        :return: None
        """
        self.adr = _ip

        asyncio.run(self._run(raise_error))

    async def _run(self, raise_error):
        if self.password is None:
            if self.hash_key is None:
                await self.method.computer.connect()

        if self._main:
            await self._main()

    async def json_info(self) -> dict:
        data = {"username": self.username, "name": self.name}

        if self.password:
            data["password"] = self.password
        else:
            data["hash_key"] = self.hash_key

        return data

    async def response(self, data: dict) -> result.ResultABC:
        """
        Do response on server
        :param data: Data for send
        :return: Actions
        """
        async with aiohttp.ClientSession() as s:
            async with s.post(self.adr, json=data) as resp:
                _result = await resp.json()
                _result = result.ResultFabric(_result)

        return _result

    async def call_method(self, method: str, raise_error: bool = False, **kwargs) -> result.ResultABC:
        """
        Call method
        :param method: Calling method
        :param kwargs: Additional data
        :return: Actions
        """
        data = await self.json_info()
        data["method"] = method
        data.update(kwargs)

        _result = await self.response(data)

        if _result == result.ResultError and raise_error:
            _result.raise_error()

        return _result

    def main(self, fn):
        self._main = fn

        return fn


if __name__ == "__main__":
    pass
