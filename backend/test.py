
import pytest
import websockets
import json

@pytest.mark.asyncio
async def test_websocket():
    uri = "ws://127.0.0.1:8002/ws/chat/1/1"
    try:
        async with websockets.connect(uri) as websocket:
            # 发送消息
            await websocket.send(json.dumps({
                "recipient_role": "1",
                "recipient_id": 2,
                "content": "再成功一次吧"
            }))
            print("Message sent")

            # 接收消息
            response = await websocket.recv()
            print("Message received:", response)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
