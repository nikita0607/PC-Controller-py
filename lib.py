import requests


class API:
    def __init__(self):
        self.session = requests.session()
    
    def connect(user_name: str, compuer_name: str, ip: str):
        data = {"user_name": user_name, "name": name}
        
        self.session.post()

    def call_method(method: str, **kwargs):
        pass



if __name__ == "__main__":
    pass
