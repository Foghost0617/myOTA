from sqlalchemy.orm import Session
from backend.models.tourist_route_model import TouristRouteRelation
from backend.models.route_model import Route
from backend.schemas.tourist_route_schema import TouristRouteCreate

class TouristRouteService:
    def __init__(self, db: Session):
        self.db = db

    # 游客报名路线
    def signup_route(self, tourist_route: TouristRouteCreate):
        db_tourist_route = TouristRouteRelation(
            tourist_id=tourist_route.tourist_id,
            route_id=tourist_route.route_id,
            status=tourist_route.status
        )
        self.db.add(db_tourist_route)
        self.db.commit()
        self.db.refresh(db_tourist_route)
        return db_tourist_route

    # 获取某条路线的所有报名游客
    def get_signed_up_tourists(self, route_id: int):
        return self.db.query(TouristRouteRelation).filter(TouristRouteRelation.route_id == route_id).all()

    # 获取游客报名的所有路线
    def get_tourist_routes(self, tourist_id: int):
        return self.db.query(TouristRouteRelation).filter(TouristRouteRelation.tourist_id == tourist_id).all()

    # 获取某个 agency 下所有路线的报名记录
    def get_applications_by_agency(self, agency_id: int):
        return (
            self.db.query(TouristRouteRelation)
            .join(Route, TouristRouteRelation.route_id == Route.id)
            .filter(Route.agency_id == agency_id)
            .all()
        )

    # 更新游客报名记录的状态
    def update_application_status(self, application_id: int, status: str):
        app = self.db.query(TouristRouteRelation).filter(TouristRouteRelation.id == application_id).first()
        if app:
            app.status = status
            self.db.commit()
            self.db.refresh(app)
        return app
