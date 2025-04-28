# services/route_guide.py
from datetime import datetime, date

from sqlalchemy.orm import Session
from backend.models.route_guide import RouteGuide
from backend.models.route_model import Route
from backend.models.user import Guide
from backend.schemas.route_guide import RouteGuideCreate, RouteGuideOut


class RouteGuideService:
    def __init__(self, db: Session):
        self.db = db



    def check_assigned(self, route_id: int) -> bool:
        # 查询是否有导游指派
        assignment = self.db.query(RouteGuide).filter(RouteGuide.route_id == route_id).first()
        return bool(assignment)

    def assign_guide(self, route_guide_create: RouteGuideCreate) -> RouteGuide:
        # 创建 RouteGuide 实例
        route_guide = RouteGuide(
            route_id=route_guide_create.route_id,
            guide_id=route_guide_create.guide_id,
            trip_start_time=route_guide_create.trip_start_time,
            trip_end_time=route_guide_create.trip_end_time
        )

        # 将记录添加到数据库
        self.db.add(route_guide)
        self.db.commit()
        self.db.refresh(route_guide)  # 刷新，确保拿到数据库中保存的记录

        return route_guide



    # 根据旅行社获取所有导游
    def get_guides_by_agency(self, agency_id: int):
        guides = self.db.query(Guide).filter(Guide.agency_id == agency_id).all()
        return guides


    # 获取旅社所有路线的指派记录
    def get_route_guides_by_agency(self, agency_id: int):
        # 查找旅社所有的路线
        routes = self.db.query(Route).filter(Route.agency_id == agency_id).all()
        # 获取所有这些路线的指派记录
        route_guides = []
        for route in routes:
            route_guides.extend(self.db.query(RouteGuide).filter(RouteGuide.route_id == route.id).all())

        return route_guides

    # 删除指派记录
    def delete_route_guide(self, route_guide_id: int):
        route_guide = self.db.query(RouteGuide).filter(RouteGuide.id == route_guide_id).first()
        if route_guide:
            self.db.delete(route_guide)
            self.db.commit()
            return True
        return False