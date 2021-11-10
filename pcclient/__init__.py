"""
This module 
"""

import json

import requests

__version__ = "0.1.0"


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
        self.session = requests.Session()

        self.method = Methods(self)
        self.broadcast_method = Methods(self, True)

        self.adr = None
        self.hash_key = None

    def connect(self, user_name: str, computer_name: str, _ip: str, hash_key: str = None):
        """
        Initialize connection with server
        :param user_name: Your user name on web site
        :param computer_name: Name of this device
        :param _ip: Server ip
        :param hash_key: Your hash key
        :return: None
        """
        data = {"user_name": user_name, "name": computer_name}
        self.adr = f"{_ip}:5005/api"
        self.hash_key = hash_key

        return self.response(data)

    def response(self, data: dict, get_actions: bool = False) -> dict:
        """
        Do response on server
        :param data: Data for send
        :param get_actions: Get event actions from server
        :return: Actions
        """

        data["get_actions"] = get_actions

        actions = self.session.post(self.adr, json=jsonify(data)).json()
        return actions

    def call_method(self, method: str, get_actions: bool = False, **kwargs) -> dict:
        """
        Call method
        :param method: Calling method
        :param get_actions: Get event actions from server
        :param kwargs: Additional data
        :return: Actions
        """
        data = {"action": "method", "type": method, "get_actions": get_actions}
        data.update(kwargs)

        return self.response(data, get_actions)

    def call_broadcast_method(self, method: str, get_actions: bool = False, **kwargs) -> dict:
        """
        Call broadcast method
        :param method: Calling method
        :param get_actions: Get event actions from server
        :param kwargs: Additional data
        :return: Actions
        """
        data = {"action": "broadcast_method", "type": method, "get_actions": get_actions, "hash_key": self.hash_key}
        data.update(kwargs)

        return self.response(data, get_actions)

    def get_actions(self) -> dict:
        """
        Get event actions from server
        :return: Actions from server
        """

        actions = self.response({}, True)
        return actions


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

    def call(self, method: str, **data) -> dict:
        """
        Call method
        :param method: Method type
        :param data: Additional data
        :return:
        """
        if not self.broadcast:
            return self.parrent.call_method(method, **data)
        return self.parrent.call_broadcast_method(method, **data)


class ButtonMethods(Method):
    """
    Contains button methods
    """

    def add(self, button_name: str, button_text: str):
        """
        Add button in to computer in dashboard
        :param button_name: If button is clicked, then server returns this name
        :param button_text: Text of button
        :return: Actions from server
        """

        data = {"name": button_name, "text": button_text}

        return self.call("button.add", **data)

    def delete_all(self) -> dict:
        """
        Delete all buttons in dashboard
        :return: Actions from server
        """

        return self.call("button.delete_all")


class ComputerMethods(Method):
    """
    Contains computer methods
    """

    def disconnect(self):
        """
        Disconnect this device from server
        :return: Actions from server
        """
        return self.call("computer.disconnect")


if __name__ == "__main__":
    pass
