# services/route_guide.py

from sqlalchemy.orm import Session
from backend.models.route_guide import RouteGuide
from backend.schemas.route_guide import RouteGuideCreate

class RouteGuideService:
    def __init__(self, db: Session):
        self.db = db

    # 创建导游指派
    def create_route_guide(self, route_guide: RouteGuideCreate):
        # 创建新的导游指派记录
        db_route_guide = RouteGuide(
            route_id=route_guide.route_id,
            guide_id=route_guide.guide_id
        )
        self.db.add(db_route_guide)
        self.db.commit()
        self.db.refresh(db_route_guide)

        return db_route_guide
