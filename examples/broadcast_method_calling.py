import pcclient


api = pcclient.API()
api.connect("nikita0607", "RoBot", "http://0.0.0.0", "Your hash key")
api.broadcast_method.button.add("Name", "Text")
