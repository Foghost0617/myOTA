from typing import List, Dict
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

    class Config:
        orm_mode = True

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
