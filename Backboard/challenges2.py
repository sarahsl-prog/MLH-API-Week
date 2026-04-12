import asyncio
import os
from backboard import BackboardClient
import dotenv
dotenv.load_dotenv()

async def main():
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))

    # create an assistant
    assistant = await client.create_assistant(
        name="My Challenge Assistant",
        system_prompt="You are a helpful assistant that responds concisely."
    )

    print(f"Created assistant: {assistant.assistant_id}")

# create a thread and send a message to the assistant
    thread = await client.create_thread(assistant_id=assistant.assistant_id)
    # print out the thread ID
    print(f"Created thread: {thread.thread_id}")

    #create a message in the thread and print the response
    response = await client.add_message(
        thread_id=thread.thread_id,
        content="Hello! I'm excited to get started.",
        memory="Auto",
        stream=False,
    )
    print(f"Assistant response: {response.content}")

asyncio.run(main())