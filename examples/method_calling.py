import pcclient


api = pcclient.API()
api.connect("nikita0607", "RoBot", "http://0.0.0.0")

api.method.button.add("test", "Tap here!")  # Call method
api.method.button.delete_all()  # Delete all created buttons for this PC

api.method.computer.disconnect()
