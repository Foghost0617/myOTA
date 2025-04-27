from sqlalchemy.orm import Session
from backend.models.user import Guide , TravelAgency,Tourist
from backend.models.tourist_route_model import TouristRouteRelation
from backend.models.route_guide import RouteGuide
from backend.schemas.user import GuideUpdate,GuideOut
from typing import List

class GuideService:
    def __init__(self, db: Session):
        self.db = db

        # 更新导游信息

    def update_guide_info(self, guide_id: int, update_data: GuideUpdate):
        guide = self.db.query(Guide).filter(Guide.id == guide_id).first()  # 使用 guide_id 来查找导游
        if not guide:
            return None
        update_fields = update_data.dict(exclude_unset=True)
        for key, value in update_fields.items():
            setattr(guide, key, value)
        self.db.commit()
        self.db.refresh(guide)
        return guide

        # 获取所有旅行社
    def get_all_agencies(self):
        return self.db.query(TravelAgency).all()

    # 所有导游
    def get_guides(self, skip: int = 0, limit: int = 10) -> List[GuideOut]:
        return self.db.query(Guide).offset(skip).limit(limit).all()

    # 按旅社获取导游
    def get_agency_id_by_guide(self, guide_id: int):
        guide = self.db.query(Guide).filter(Guide.id == guide_id).first()
        return guide.agency_id if guide else None

    def get_tourists_by_guide_id(self, guide_id: int):
        # 1. 获取导游负责的路线 ID
        route_ids = self.db.query(RouteGuide.route_id).filter_by(guide_id=guide_id).all()
        route_ids = [r.route_id for r in route_ids]

        if not route_ids:
            return []
        tourist_ids = self.db.query(TouristRouteRelation.tourist_id)\
            .filter(TouristRouteRelation.route_id.in_(route_ids))\
            .distinct().all()

        tourist_ids = [t.tourist_id for t in tourist_ids]
        if not tourist_ids:
            return []


        tourists = self.db.query(Tourist).filter(Tourist.id.in_(tourist_ids)).all()
        return tourists