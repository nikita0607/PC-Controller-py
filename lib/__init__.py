import requests


class API:
    def __init__(self):
        self.session = requests.Session()

        self.button = ButtonMethods(self)
        self.adr = None
    
    def connect(self, user_name: str, computer_name: str, ip: str):
        data = {"user_name": user_name, "name": computer_name}
        self.adr = f"{ip}:5000/a"

        actions = self.session.post(f"{ip}:5000/a", data=data).json()
        return actions

    def call_method(self, method: str, get_actions: bool = False, **kwargs):
        data = {"method": method, "get_actions": get_actions}
        data.update(kwargs)

        actions = self.session.post(self.adr, data=data).json()
        return actions

    def get_actions(self):
        actions = self.session.post(self.adr).json()
        return actions


class ButtonMethods:
    def __init__(self, parrent_api: API):
        self.parrent = parrent_api

    def add(self, button_name: str, button_text: str):
        data = {"name": button_name, "text": button_text}

        self.parrent.call_method("button.add", **data)


if __name__ == "__main__":
    pass
