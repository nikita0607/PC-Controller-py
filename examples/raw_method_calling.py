import pcclient


api = pcclient.API("nikita0607", "RoBo")


@api.main
async def main():
    data = {"name": "test", "text": "Tap here!"}  # Raw data

    await api.call_method("button.add", **data)   # Calling method with raw data

    await api.call_method("button.add", name="test", text="Or tap here!")  # You can do this!!

    await api.call_method("computer.disconnect")   # You can call methods without raw data


api.run("http://127.0.0.1:8000/api")

