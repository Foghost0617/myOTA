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

# 前端发来
class GroupMessageIn(BaseModel):
    group_id: int
    sender_id: int
    sender_role: int
    content: str

class CreateChatGroup(BaseModel):
    name: str
    created_by_id: int
    created_by_role: int
    members: List[Dict[str, int]]  # 每个成员是 {"user_id": int, "user_role": int}
