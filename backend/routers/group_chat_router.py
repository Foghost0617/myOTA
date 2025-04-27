import json
from idlelib.query import Query
from typing import List
from fastapi import APIRouter, WebSocket
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect


from backend.core.database import SessionLocal
from backend.models.message_model import ChatGroupMember, GroupMessageReceiver, Message
from backend.routers.chat_router import get_db
from backend.schemas.message_schema import CreateGroupChatResponse, CreateGroupChatRequest, GroupChatMessageOut, \
    GroupChatMessageIn
from backend.services.group_chat_service import  GroupChatService

router = APIRouter(
    prefix="/groupchats",
    tags=["群聊！"]
)

# 创建群聊
@router.post("/create", response_model=CreateGroupChatResponse)
def create_group_chat(request: CreateGroupChatRequest):
    db: Session = SessionLocal()
    try:
        group_chat_service = GroupChatService(db)
        group_chat = group_chat_service.create_group_chat(request)
        if not group_chat:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="创建群聊失败"
            )
        return group_chat
    finally:
        db.close()


@router.get("/available-members", response_model=List[dict])
def get_available_group_members(creator_id: int, creator_role: int):
    print('进入获取可拉取的路由')
    print(creator_id,creator_role)
    db: Session = SessionLocal()
    try:
        service = GroupChatService(db)
        member_ids, member_roles = service.get_valid_members(creator_id, creator_role)

        # 拼成前端要的格式
        members = [
            {"user_id": uid, "user_role": role}
            for uid, role in zip(member_ids, member_roles)
        ]
        print(members)
        return members
    except Exception as e:
        print("获取可选群聊成员出错：", str(e))
        raise HTTPException(status_code=500, detail="服务器内部错误")
    finally:
        db.close()



@router.get("/user-groups", response_model=List[dict])
def get_user_groups(user_id: int):
    db: Session = SessionLocal()
    try:
        service = GroupChatService(db)
        groups = service.get_user_groups(user_id)

        # 返回前端需要的格式
        result = [
            {
                "group_id": group.id,
                "group_name": group.name,
                "created_at": group.created_at
            }
            for group in groups
        ]

        return result

    except Exception as e:
        print("获取用户群聊列表失败：", str(e))
        raise HTTPException(status_code=500, detail="服务器内部错误")
    finally:
        db.close()



# 存储活动的 WebSocket 连接
active_connections: List[WebSocket] = []

# 用于保存每个群聊的 WebSocket 连接列表
group_connections = {}


@router.websocket("/ws/group-chat/{group_id}")
async def websocket_group_chat(websocket: WebSocket, group_id: int):
    await websocket.accept()
    print(f"WebSocket 连接成功：群聊 ID {group_id}")
    if group_id not in group_connections:
        group_connections[group_id] = []

    group_connections[group_id].append(websocket)


    try:
        while True:
            data = await websocket.receive_text()
            print(f"收到数据：{data}")  # ➡️ 打印收到的消息内容
            message_data = GroupChatMessageIn(**json.loads(data))
            print(f"解析后的 message_data: {message_data}")  # ➡️ 打印解析后的对象

            # 存储消息到数据库
            db: Session = SessionLocal()
            try:
                new_message = Message(
                    sender_id=message_data.sender_id,
                    sender_role=message_data.sender_role,
                    receiver_id=message_data.group_id,
                    receiver_role=0,
                    content=message_data.content,
                    is_group=True,
                    is_read=False,
                    is_location=message_data.is_location,
                    latitude=message_data.latitude,
                    longitude=message_data.longitude,
                )
                db.add(new_message)
                db.commit()
                print(f"消息存入数据库成功，消息ID: {new_message.id}")  # ➡️ 打印存储成功的信息

                message_out = GroupChatMessageOut(
                    message_id=new_message.id,
                    sender_id=message_data.sender_id,
                    sender_role=message_data.sender_role,
                    group_id=message_data.group_id,
                    content=message_data.content,
                    timestamp=new_message.timestamp,
                    is_location=message_data.is_location,
                    latitude=message_data.latitude,
                    longitude=message_data.longitude,
                )

                # 广播消息
                for connection in group_connections[group_id]:
                    await connection.send_text(message_out.json())
            except Exception as e:
                print(f"存储消息失败：{str(e)}")
                raise WebSocketDisconnect()
            finally:
                db.close()

    except WebSocketDisconnect:
        group_connections[group_id].remove(websocket)
        if not group_connections[group_id]:
            del group_connections[group_id]
        print(f"WebSocket 连接关闭，群聊 ID: {group_id}")



def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{group_id}/history", response_model=List[GroupChatMessageOut])
async def get_group_chat_history(group_id: int):
    """
    获取特定群聊的历史聊天记录
    """
    # 获取数据库会话
    db = SessionLocal()

    try:
        # 查询群聊的历史消息
        messages = db.query(Message)\
            .filter(Message.is_group == True)\
            .filter(Message.receiver_id == group_id)\
            .order_by(Message.timestamp.asc())\
            .all()

        # 格式化消息并返回
        result = []
        for m in messages:
            result.append(GroupChatMessageOut(
                message_id=m.id,
                sender_id=m.sender_id,
                sender_role=m.sender_role,
                group_id=m.receiver_id,  # 群聊id其实就是receiver_id
                content=m.content,
                timestamp=m.timestamp,
                is_location=m.is_location,
                latitude=m.latitude,
                longitude=m.longitude,
            ))

        return result
    finally:
        db.close()



# @router.post("/send-group-message", response_model=GroupChatMessageOut)
# def send_group_message(request: GroupChatMessageIn):
#     db: Session = SessionLocal()  # 手动创建数据库会话
#     try:
#         # 存储群聊消息
#         new_message = Message(
#             sender_id=request.sender_id,
#             sender_role=request.sender_role,
#             receiver_id=request.group_id,  # 群聊ID
#             receiver_role=0,  # 群聊没有接收者，receiver_role为0
#             content=request.content,
#             is_group=True,
#             is_read=False,
#             is_location=request.is_location,
#             latitude=request.latitude,
#             longitude=request.longitude,
#         )
#         db.add(new_message)
#         db.commit()
#
#         # 将消息返回
#         message_out = GroupChatMessageOut(
#             message_id=new_message.id,
#             sender_id=request.sender_id,
#             sender_role=request.sender_role,
#             group_id=request.group_id,
#             content=request.content,
#             timestamp=new_message.timestamp,
#             is_location=request.is_location,
#             latitude=request.latitude,
#             longitude=request.longitude,
#         )
#
#         # 广播消息给 WebSocket 连接中的成员
#         if request.group_id in group_connections:
#             for connection in group_connections[request.group_id]:
#                 # 通过 WebSocket 发送消息
#                 connection.send_text(message_out.json())
#
#         return message_out
#     except Exception as e:
#         print(f"发送群聊消息失败：{str(e)}")
#         raise HTTPException(status_code=500, detail="发送群聊消息失败")
#     finally:
#         db.close()  # 关闭数据库会话