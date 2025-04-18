from fastapi import APIRouter, HTTPException, status,Depends, Query
from sqlalchemy.orm import Session
from backend.schemas.route_schema import RouteCreate, RouteOut, RouteSpotCreate,RouteSpotOut
from backend.services.route_service import RouteService
from backend.core.database import SessionLocal  # 直接导入SessionLocal
from typing import List
from backend.models.route_model import RouteSpot  # 导入 ORM 模型类

router = APIRouter(
    prefix="/routes",  # 路由前缀
    tags=["路线"]  # 为路由分配标签，便于文档管理
)

# 创建路线
@router.post("/info", response_model=RouteOut)
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


@router.get("/agency/{agency_id}", response_model=List[RouteOut])
def get_routes_by_agency(agency_id: int):
    db: Session = SessionLocal()
    try:
        route_service = RouteService(db)
        routes = route_service.get_routes_by_agency(agency_id)  # 获取所有路线
        if not routes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No routes found for agency {agency_id}"
            )
        return routes  # 返回一个包含多个 RouteOut 对象的列表
    finally:
        db.close()



@router.get("/spots/{route_id}", response_model=List[RouteSpotOut])
def get_route_spots(route_id: int):
    db: Session = SessionLocal()
    try:
        route_service = RouteService(db)
        route_spots = route_service.get_route_spots(route_id)
        if not route_spots:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No spots found for route {route_id}"
            )
        return route_spots
    finally:
        db.close()
