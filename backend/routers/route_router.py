from fastapi import APIRouter, HTTPException, status,Depends
from sqlalchemy.orm import Session
from backend.schemas.route_schema import RouteCreate, RouteOut, RouteSpotCreate
from backend.services.route_service import RouteService
from backend.core.database import SessionLocal  # 直接导入SessionLocal
from typing import List
from backend.models.route_model import RouteSpot  # 导入 ORM 模型类

router = APIRouter(
    prefix="/routes",  # 路由前缀
    tags=["路线"]  # 为路由分配标签，便于文档管理
)

# 创建路线
@router.post("/info/", response_model=RouteOut)
def create_route(route: RouteCreate):
    db: Session = SessionLocal()
    try:
        route_service = RouteService(db)
        db_route = route_service.create_route(route)
        print(db_route)
        if not db_route:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法创建路线"
            )
        return db_route
    finally:
        db.close()

# 创建景点（多个）
@router.post("/route_spots/")
def create_route_spots(spots: List[RouteSpotCreate]):
    db: Session = SessionLocal()
    try:
        route_spot_service = RouteService(db)
        db_spots = route_spot_service.create_route_spots(spots)
        if not db_spots:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法创建景点"
            )
        return db_spots
    finally:
        db.close()




# 获取单个路线
@router.get("/{route_id}", response_model=RouteOut)
def get_route(route_id: int):
    db: Session = SessionLocal()  # 直接使用 SessionLocal() 创建数据库会话
    route_service = RouteService(db)
    db_route = route_service.get_route(route_id)
    if not db_route:
        db.close()  # 关闭数据库会话
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="路线未找到"
        )
    db.close()  # 关闭数据库会话
    return db_route

# 删除路线
@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(route_id: int):
    db: Session = SessionLocal()  # 直接使用 SessionLocal() 创建数据库会话
    route_service = RouteService(db)
    route_service.delete_route(route_id)
    db.close()  # 关闭数据库会话
    return {"detail": "删除成功"}


