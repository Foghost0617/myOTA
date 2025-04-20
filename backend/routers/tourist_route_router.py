
from fastapi import APIRouter, HTTPException, status,Depends, Query
from sqlalchemy.orm import Session
from backend.schemas.tourist_route_schema import TouristRouteOut,TouristRouteCreate
from backend.services.tourist_route_service import TouristRouteService
from backend.core.database import SessionLocal  # 直接导入SessionLocal
from typing import List
from backend.models.route_model import RouteSpot  # 导入 ORM 模型类

router = APIRouter(
    prefix="/tourist_route",  # 路由前缀
    tags=["路线"]  # 为路由分配标签，便于文档管理
)
# 游客报名某条路线
@router.post("/signup", response_model=TouristRouteOut)
def signup_route_for_tourist(tourist_route: TouristRouteCreate):
    db: Session = SessionLocal()
    try:
        tourist_route_service = TouristRouteService(db)
        db_tourist_route = tourist_route_service.signup_route(tourist_route)
        if not db_tourist_route:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法完成报名"
            )
        return db_tourist_route
    finally:
        db.close()

# 获取某条路线的所有报名游客
@router.get("/route/{route_id}/tourists", response_model=List[TouristRouteOut])
def get_tourists_by_route(route_id: int):
    db: Session = SessionLocal()
    try:
        tourist_route_service = TouristRouteService(db)
        tourists = tourist_route_service.get_signed_up_tourists(route_id)
        if not tourists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="没有找到报名此路线的游客"
            )
        return tourists
    finally:
        db.close()

# 获取某个游客报名的所有路线
@router.get("/tourist/{tourist_id}/routes", response_model=List[TouristRouteOut])
def get_routes_by_tourist(tourist_id: int):
    db: Session = SessionLocal()
    try:
        tourist_route_service = TouristRouteService(db)
        routes = tourist_route_service.get_tourist_routes(tourist_id)
        if not routes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="没有找到该游客报名的路线"
            )
        return routes
    finally:
        db.close()
