# chat_router.py 文件
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Dict
from backend.models.message_model import Message, ChatGroupMember, ChatGroup
from backend.core.database import SessionLocal
from datetime import datetime
from fastapi import Depends
import json
from fastapi import Query
from backend.models.message_model import Message
from backend.schemas.message_schema import MessageOut
from sqlalchemy import or_, and_
from typing import List

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
async def chat_endpoint(websocket: WebSocket, sender_role: int, sender_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    print(f"WebSocket connection accepted for {sender_role}_{sender_id}")

    # 存储用户的 WebSocket 连接
    user_key = f"{sender_role}_{sender_id}"
    active_connections[user_key] = websocket

    try:
        while True:
            # 接收前端发送的数据
            data = await websocket.receive_text()
            print(f"Received message: {data}")

            # 解析消息内容
            message_data = json.loads(data)
            receiver_role = int(message_data["receiver_role"])
            receiver_id = int(message_data["receiver_id"])
            content = message_data["content"]
            is_group = message_data.get("is_group", False)
            is_location = message_data.get("is_location", False)
            latitude = message_data.get("latitude")
            longitude = message_data.get("longitude")
            # 获取位置归属者，默认设为发送者
            location_owner_id = sender_id if is_location else None
            location_owner_role = sender_role if is_location else None

            print(f"Received location: latitude={latitude}, longitude={longitude}")
            # 存储消息到数据库
            db_message = Message(
                sender_id=sender_id,
                sender_role=sender_role,
                receiver_id=receiver_id,
                receiver_role=receiver_role,
                content=content,
                is_group=is_group,
                is_read=False,
                is_location=is_location,
                latitude=latitude if is_location else None,
                longitude=longitude if is_location else None,
                # 获取位置归属者，默认设为发送者
                location_owner_id=location_owner_id,
                location_owner_role=location_owner_role


            )
            print(f"存进数据库的消息: {db_message}")

            db.add(db_message)
            db.commit()
            db.refresh(db_message)

            # 群聊逻辑：广播给所有连接，找相同角色和角色 ID 的连接
            if is_group:
                for user_key, ws in active_connections.items():
                    u_role, u_id = user_key.split("_")
                    if int(u_role) == receiver_role:
                        await ws.send_text(json.dumps({
                            "from": f"{sender_role}_{sender_id}",
                            "content": content,
                            "timestamp": db_message.timestamp.isoformat(),
                            "is_group": True
                        }))
            else:
                # 私聊逻辑：只发送给特定用户
                recipient_key = f"{receiver_role}_{receiver_id}"
                if recipient_key in active_connections:
                    message_payload = {
                        "from": f"{sender_role}_{sender_id}",
                        "content": content,
                        "timestamp": db_message.timestamp.isoformat(),
                        "is_group": is_group,
                        "is_location": is_location,
                        "latitude": latitude,
                        "longitude": longitude,
                        "location_owner_id": location_owner_id,
                        "location_owner_role": location_owner_role

                    }
                    await active_connections[recipient_key].send_text(json.dumps(message_payload))

    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
        await websocket.close()
        del active_connections[user_key]



# # 私聊逻辑
# @router.websocket("/ws/chat/{sender_role}/{sender_id}")
# async def chat_endpoint(websocket: WebSocket, sender_role: int, sender_id: int, db: Session = Depends(get_db)):
#     await websocket.accept()
#     print(f"WebSocket connection accepted for {sender_role}_{sender_id}")
#
#     # 存储用户的 WebSocket 连接
#     user_key = f"{sender_role}_{sender_id}"
#     active_connections[user_key] = websocket
#
#     try:
#         while True:
#             # 接收前端发送的数据
#             data = await websocket.receive_text()
#             print(f"Received message: {data}")
#
#             # 解析消息内容
#             # message_data = json.loads(data)
#             # receiver_role = int(message_data["receiver_role"])
#             # receiver_id = int(message_data["receiver_id"])
#             # content = message_data["content"]
#             # is_group = message_data.get("is_group", False)
#
#             message_data = json.loads(data)
#             receiver_role = int(message_data["receiver_role"])
#             receiver_id = int(message_data["receiver_id"])
#             content = message_data["content"]
#             is_group = message_data.get("is_group", False)
#             is_location = message_data.get("is_location", False)
#             latitude = message_data.get("latitude")
#             longitude = message_data.get("longitude")
#
#             # 存储消息到数据库
#             # db_message = Message(
#             #     sender_id=sender_id,
#             #     sender_role=sender_role,
#             #     receiver_id=receiver_id,
#             #     receiver_role=receiver_role,
#             #     content=content,
#             #     is_group=is_group,
#             #     is_read=False
#             # )
#
#             db_message = Message(
#                 sender_id=sender_id,
#                 sender_role=sender_role,
#                 receiver_id=receiver_id,
#                 receiver_role=receiver_role,
#                 content=content,
#                 is_group=is_group,
#                 is_read=False,
#                 is_location=is_location,
#                 latitude=latitude if is_location else None,
#                 longitude=longitude if is_location else None
#             )
#             db.add(db_message)
#             db.commit()
#             db.refresh(db_message)
#
#             # 群聊逻辑：广播给所有连接，找相同角色和角色 ID 的连接
#             if is_group:
#                 for user_key, ws in active_connections.items():
#                     u_role, u_id = user_key.split("_")
#                     if int(u_role) == receiver_role:
#                         await ws.send_text(json.dumps({
#                             "from": f"{sender_role}_{sender_id}",
#                             "content": content,
#                             "timestamp": db_message.timestamp.isoformat(),
#                             "is_group": True
#                         }))
#             else:
#                 # 私聊逻辑：只发送给特定用户
#                 # recipient_key = f"{receiver_role}_{receiver_id}"
#                 # if recipient_key in active_connections:
#                 #     await active_connections[recipient_key].send_text(json.dumps({
#                 #         "from": f"{sender_role}_{sender_id}",
#                 #         "content": content,
#                 #         "timestamp": db_message.timestamp.isoformat(),
#                 #         "is_group": False
#                 #     }))
#                 recipient_key = f"{receiver_role}_{receiver_id}"
#                 if recipient_key in active_connections:
#                     message_payload = {
#                         "from": f"{sender_role}_{sender_id}",
#                         "content": content,
#                         "timestamp": db_message.timestamp.isoformat(),
#                         "is_group": is_group,
#                         "is_location": is_location,
#                         "latitude": latitude,
#                         "longitude": longitude
#                     }
#                     await active_connections[recipient_key].send_text(json.dumps(message_payload))
#
#
#
#
#     except WebSocketDisconnect:
#         print(f"WebSocket connection closed for {user_key}")
#         # 删除断开的连接
#         if user_key in active_connections:
#             del active_connections[user_key]
#
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         # 如果有错误，也要确保删除该连接
#         if user_key in active_connections:
#             del active_connections[user_key]

# 获取私聊聊天历史的接口

# 最新能用
# @router.get("/messages/history", response_model=List[MessageOut])
# def get_chat_history(
#     sender_id: int,
#     sender_role: int,
#     receiver_id: int,
#     receiver_role: int,
#     db: Session = Depends(get_db)
# ):
#     messages = db.query(Message).filter(
#         or_(
#             and_(
#                 Message.sender_id == sender_id,
#                 Message.sender_role == sender_role,
#                 Message.receiver_id == receiver_id,
#                 Message.receiver_role == receiver_role
#             ),
#             and_(
#                 Message.sender_id == receiver_id,
#                 Message.sender_role == receiver_role,
#                 Message.receiver_id == sender_id,
#                 Message.receiver_role == sender_role
#             )
#         )
#     ).order_by(Message.timestamp.asc()).all()
#     return messages


@router.get("/messages/history", response_model=List[MessageOut])
def get_chat_history(
    sender_id: int,
    sender_role: int,
    receiver_id: int,
    receiver_role: int,
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        or_(
            and_(
                Message.sender_id == sender_id,
                Message.sender_role == sender_role,
                Message.receiver_id == receiver_id,
                Message.receiver_role == receiver_role
            ),
            and_(
                Message.sender_id == receiver_id,
                Message.sender_role == receiver_role,
                Message.receiver_id == sender_id,
                Message.receiver_role == sender_role
            )
        )
    ).order_by(Message.timestamp.asc()).all()

    # 使用 MessageOut 来转换查询结果
    return [MessageOut.from_orm(message) for message in messages]

