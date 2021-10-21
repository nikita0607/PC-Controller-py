import lib


api = lib.API()  # Create API object
api.connect("user_name", "MyNaMe", "server_ip")  # Connect to server and send inform. about this PC

api.computer.disconnect()  # Disconnect this PC
