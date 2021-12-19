import pcclient


api = pcclient.API("user_name", "MyName")  # Create API object


@api.main
async def main():
    pass


api.run("http://0.0.0.0")