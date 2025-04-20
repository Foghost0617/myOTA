# schemas/route_guide.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 创建导游指派的请求体
class RouteGuideCreate(BaseModel):
    route_id: int
    guide_id: int

    class Config:
        orm_mode = True


# 返回给客户端的导游指派信息
class RouteGuideOut(BaseModel):
    id: int
    route_id: int
    guide_id: int


    class Config:
        orm_mode = True
