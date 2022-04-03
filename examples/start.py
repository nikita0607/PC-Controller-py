import pcclient


api = pcclient.API("http://127.0.0.1:8000", "nikita0607", "MyPC")  # Create API object


@api.main
async def main():
    pass


api.run()
