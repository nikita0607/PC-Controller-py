import lib

from time import sleep


api = lib.API()
api.connect("nikita0607", "Test", "http://192.168.0.102")

api.button.delete_all()
ans = api.call_method("button.add")
print(ans)

while True:
    sleep(2)

    print(api.get_actions())