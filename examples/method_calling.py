import pcclient


api = pcclient.API("nikita0607", "RoBo")


@api.main
async def main():
    await api.method.button.add("test", "Tap here!")  # Call method


api.run("http://127.0.0.1:8000/api")
