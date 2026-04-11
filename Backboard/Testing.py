# pip install backboard-sdk
import asyncio
from backboard import BackboardClient

async def main():
    client = BackboardClient(api_key="espr_bRoCaNMhiynqVMiaJDZNjm-TnVbTxc1R47rrJ1lIYcM")

    response = await client.add_message(
        thread_id="429a0995-bc97-4618-8607-bc817435931a",
        content="Hello! I'm excited to get started.",
        memory="Auto",
        stream=False,
    )
    print(response.content)

asyncio.run(main())