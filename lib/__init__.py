import json

import requests


class API:
    def __init__(self):
        self.session = requests.Session()

        self.button = ButtonMethods(self)
        self.computer = ComputerMethods(self)

        self.adr = None

    def jsonify(self, data) -> str:
        return json.dumps(data)
    
    def connect(self, user_name: str, computer_name: str, ip: str):
        data = {"user_name": user_name, "name": computer_name}
        self.adr = f"{ip}:5000/a"

        return self.response(data)

    def response(self, data: dict, get_actions: bool = False) -> dict:
        data["get_actions"] = get_actions

        actions = self.session.post(self.adr, json=self.jsonify(data)).json()
        return actions

    def call_method(self, method: str, get_actions: bool = False, **kwargs):
        data = {"action": "method", "type": method, "get_actions": get_actions}
        data.update(kwargs)

        return self.response(data, get_actions)

    def get_actions(self):
        actions = self.response({}, True)
        return actions


class Methods:
    def __init__(self, parrent_api: API):
        self.parrent = parrent_api


class ButtonMethods(Methods):
    def add(self, button_name: str, button_text: str):
        data = {"name": button_name, "text": button_text}

        return self.parrent.call_method("button.add", **data)

    def delete_all(self):
        return self.parrent.call_method("button.delete_all")


class ComputerMethods(Methods):
    def disconnect(self):
        return self.parrent.call_method("computer.disconnect")


if __name__ == "__main__":
    pass
