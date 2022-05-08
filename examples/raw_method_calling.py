import pcclient


api = pcclient.API("http://127.0.0.1:8000", "nikita0607", "RoBo")


@api.main
async def main():
    data = {"name": "test", "text": "Tap here!"}  # Raw data

    await api.call_method("button.add", **data)   # Calling method with raw data

    await api.call_method("button.add", name="test", text="Or tap here!")  # You can do this!!

    await api.call_method("computer.disconnect")  # You can call methods without raw data
    # You can use it, but library do autodisconnecting

api.run()

