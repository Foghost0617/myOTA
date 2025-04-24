from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    tourist_id: int
    content: str

class ComplaintOut(BaseModel):
    id: int
    tourist_id: int
    content: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class ComplaintStatusUpdate(BaseModel):
    status: str  # 只能传 "已处理"
