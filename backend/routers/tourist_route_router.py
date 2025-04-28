
from fastapi import APIRouter, HTTPException, status,Depends, Query
from sqlalchemy.orm import Session

from backend.models.route_guide import RouteGuide
from backend.models.tourist_route_model import TouristRouteRelation
from backend.schemas.tourist_route_schema import TouristRouteOut,TouristRouteCreate,TouristRouteStatusUpdate
from backend.services.tourist_route_service import TouristRouteService
from backend.core.database import SessionLocal  # 直接导入SessionLocal
from typing import List
from fastapi import Body
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


# 获取某个旅行社所有报名记录
@router.get("/agency/{agency_id}/enrollments", response_model=List[TouristRouteOut])
def get_applications_by_agency(agency_id: int):
    db: Session = SessionLocal()
    try:
        tourist_route_service = TouristRouteService(db)
        applications = tourist_route_service.get_applications_by_agency(agency_id)
        if not applications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="没有找到任何报名记录"
            )
        return applications
    finally:
        db.close()

# 更新游客报名记录的状态
@router.put("/enrollment/{application_id}/status", response_model=TouristRouteOut)
def update_application_status(application_id: int, status_update: TouristRouteStatusUpdate):
    db: Session = SessionLocal()
    try:
        tourist_route_service = TouristRouteService(db)
        updated_application = tourist_route_service.update_application_status(
            application_id, status_update.status
        )
        if not updated_application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法更新报名记录状态"
            )
        return updated_application
    finally:
        db.close()




@router.get("/get_guides_by_tourist/{tourist_id}")
def get_confirmed_route_guides(tourist_id: int):
    # 创建数据库会话
    db: Session = SessionLocal()

    try:
        # 查询游客已确认的路线
        confirmed_routes = db.query(TouristRouteRelation) \
            .filter(TouristRouteRelation.tourist_id == tourist_id) \
            .filter(TouristRouteRelation.status == '已确认') \
            .all()

        if not confirmed_routes:
            raise HTTPException(status_code=404, detail="没有已确认的路线")

        # 获取这些已确认路线的导游ID
        route_ids = [route.route_id for route in confirmed_routes]
        guides = db.query(RouteGuide) \
            .filter(RouteGuide.route_id.in_(route_ids)) \
            .all()

        if not guides:
            raise HTTPException(status_code=404, detail="未找到导游")

        # 提取所有导游的 ID
        guide_ids = [guide.guide_id for guide in guides]

        return {"guide_ids": guide_ids}

    finally:
        # 确保数据库会话关闭
        db.close()