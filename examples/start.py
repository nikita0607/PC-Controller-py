import pcclient


api = pcclient.API()  # Create API object
api.connect("user_name", "MyNaMe", "server_ip")  # Connect to server and send inform. about this PC

api.method.computer.disconnect()  # Disconnect this PC
