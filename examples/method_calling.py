import lib


api = lib.API()
api.connect("nikita0607", "RoBot", "http://0.0.0.0")

api.button.add("test", "Tap here!")  # Call method
api.button.delete_all()  # Delete all created buttons for this PC

api.computer.disconnect()
