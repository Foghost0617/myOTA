# backend/schemas/route_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional

# 景点的基表
class RouteSpotBase(BaseModel):
    route_id: int
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    sequence: int

# 前端给的数据
class RouteSpotCreate(RouteSpotBase):
    pass
# 后端给前端返回的
class RouteSpotOut(RouteSpotBase):
    id:int
    class Config:
        from_attributes = True


# 路线基础信息，名字和描述
class RouteBase(BaseModel):
    name: str
    description: Optional[str] = None
    agency_id: int

# 前端给的
class RouteCreate(RouteBase):
    pass

# 后端给前端的
class RouteOut(RouteBase):
    id: int
    class Config:
        from_attributes = True


