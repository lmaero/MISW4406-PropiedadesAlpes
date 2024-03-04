import asyncio
import json

import websockets

from ui.pda.consumer import get_subscription_to_topic

consumer = None


async def process_events(websocket):
    global consumer
    print(f"====== Starts to process =======")
    while True:
        message = consumer.receive()
        json_dict = json.dumps(message.value())

        print(f"Message: {json_dict}")

        await websocket.send(json_dict)
        consumer.acknowledge(message)
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(process_events, "localhost", 5678):
        await asyncio.Future()


if __name__ == "__main__":
    consumer = get_subscription_to_topic()
    print("========= Start Server =========")
    asyncio.run(main())
