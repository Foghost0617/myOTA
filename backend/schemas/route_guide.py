# schemas/route_guide.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 创建导游指派的请求体
# class RouteGuideCreate(BaseModel):
#     route_id: int
#     guide_id: int
#
#     class Config:
#         orm_mode = True
#
#
# # 返回给客户端的导游指派信息
# class RouteGuideOut(BaseModel):
#     id: int
#     route_id: int
#     guide_id: int
#
#
#     class Config:
#         orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from datetime import date

class RouteGuideCreate(BaseModel):
    route_id: int
    guide_id: int
    trip_start_time: date  # 行程开始时间
    trip_end_time: date    # 行程结束时间

    class Config:
        orm_mode = True
        from_attributes = True  # 添加这一行

class RouteGuideOut(BaseModel):
    id: int
    route_id: int
    guide_id: int
    trip_start_time: date  # 行程开始时间
    trip_end_time: date    # 行程结束时间


    class Config:
        orm_mode = True
        from_attributes = True  # 添加这一行





