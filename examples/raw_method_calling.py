import lib


api = lib.API()
api.connect("nikita0607", "RoBot", "http://0.0.0.0")

data = {"name": "test", "text": "Tap here!"}  # Raw data
api.call_method("button.add", **data)   # Calling method with raw data

api.call_method("button.add", name="test", text="Or tap here!")  # You can do this!!

api.call_method("computer.disconnect")   # You can call methods without raw data
