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
