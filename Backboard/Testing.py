# pip install backboard-sdk
import asyncio
from backboard import BackboardClient

async def main():
    client = BackboardClient(api_key="espr_JRGzExFskOUG16Zm6UA58D7ZuSnOxUaytcAk-5HQIYI")

    response = await client.add_message(
        thread_id="76e24358-b14f-4a7e-93b8-0088732e2597",
        content="Hello! I'm excited to get started.",
        memory="Auto",
        stream=False,
    )
    print(response.content)

asyncio.run(main())