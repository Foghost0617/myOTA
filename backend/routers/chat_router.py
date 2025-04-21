# chat_router.py 文件
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Dict
from backend.models.message_model import Message
from backend.core.database import SessionLocal
from datetime import datetime
from fastapi import Depends
import json

print("✅ chat_router 被加载了")

router = APIRouter()

# 连接池（key: 角色_用户ID）
active_connections: Dict[str, WebSocket] = {}

# 数据库会话依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/ws/chat/{sender_role}/{sender_id}")
async def chat_endpoint(websocket: WebSocket, sender_role: str, sender_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    print(f"WebSocket connection accepted for {sender_role}_{sender_id}")
    user_key = f"{sender_role}_{sender_id}"
    active_connections[user_key] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")

            message_data = json.loads(data)
            receiver_role = message_data["receiver_role"]
            receiver_id = message_data["receiver_id"]
            content = message_data["content"]

            # 存入数据库
            db_message = Message(
                sender_id=sender_id,
                sender_role=sender_role,
                receiver_id=receiver_id,
                receiver_role=receiver_role,
                content=content,
                is_group=False,  # 视情况设定
                is_read=False
            )

            db.add(db_message)
            db.commit()
            db.refresh(db_message)

            # 向接收方发送消息（若在线）
            recipient_key = f"{receiver_role}_{receiver_id}"
            if recipient_key in active_connections:
                await active_connections[recipient_key].send_text(json.dumps({
                    "from": user_key,
                    "content": content,
                    "timestamp": db_message.timestamp.isoformat()
                }))
    except WebSocketDisconnect:
        print(f"WebSocket connection closed for {user_key}")
        if user_key in active_connections:
            del active_connections[user_key]
    except Exception as e:
        print(f"Error occurred: {e}")


