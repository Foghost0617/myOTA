from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, func

from pydantic import BaseModel
from datetime import datetime

class MessageOut(BaseModel):
    id: int
    sender_id: int
    sender_role: int
    receiver_id: int
    receiver_role: int
    content: str
    timestamp: datetime
    is_group: bool

    is_location: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # ✅ 新增字段
    location_owner_id: Optional[int] = None
    location_owner_role: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True  # 添加这一行

# 创建群聊

class CreateGroupChatRequest(BaseModel):
    name: str  # 群聊名称
    creator_id: int  # 创建者的用户ID
    creator_role: int  # 创建者的角色ID
    class Config:
        from_attributes = True  # 添加这一行


class CreateGroupChatResponse(BaseModel):
    group_id: int
    name: str
    creator_id: int
    creator_role: int
    member_ids: List[int]  # 群成员ID
    member_roles: List[int]  # 群成员角色

# 群聊信息体
class GroupChatMessageIn(BaseModel):
    sender_id: int  # 发送者ID
    sender_role: int  # 发送者角色
    group_id: int  # 群聊ID
    content: str  # 消息内容
    is_location: Optional[bool] = False  # 是否是位置消息
    latitude: Optional[float] = None  # 经度
    longitude: Optional[float] = None  # 纬度

    class Config:
        orm_mode = True


class GroupChatMessageOut(BaseModel):
    message_id: int
    sender_id: int
    sender_role: int
    group_id: int
    content: str
    timestamp: datetime
    is_location: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        orm_mode = True
