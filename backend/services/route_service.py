from sqlalchemy.orm import Session
from typing import List
from backend.models.route_model import Route, RouteSpot
from backend.schemas.route_schema import RouteCreate, RouteOut, RouteSpotCreate


class RouteService:
    def __init__(self, db: Session):
        self.db = db

    # 创建路线
    def create_route(self, route: RouteCreate):
        # 创建路线
        db_route = Route(
            name=route.name,
            description=route.description,
            agency_id=route.agency_id
        )
        self.db.add(db_route)
        self.db.commit()
        self.db.refresh(db_route)

        return db_route
        # 创建多个景点

    def create_route_spots(self, spots: List[RouteSpotCreate]):
        # 批量添加景点
        db_spots = []
        for spot in spots:
            db_spot = RouteSpot(
                route_id=spot.route_id,  # 关联路线ID
                name=spot.name,
                description=spot.description,
                latitude=spot.latitude,
                longitude=spot.longitude,
                sequence=spot.sequence
            )
            db_spots.append(db_spot)

        self.db.add_all(db_spots)  # 批量添加景点
        self.db.commit()

        return db_spots  # 返回创建的景点列表



    # 获取所有路线
    def get_routes(self, skip: int = 0, limit: int = 100) -> List[RouteOut]:
        routes = self.db.query(Route).offset(skip).limit(limit).all()
        return routes

    # 获取单个路线
    def get_route(self, route_id: int) -> RouteOut:
        route = self.db.query(Route).filter(Route.id == route_id).first()
        return route

    # 删除路线
    def delete_route(self, route_id: int):
        db_route = self.db.query(Route).filter(Route.id == route_id).first()
        if db_route:
            self.db.delete(db_route)
            self.db.commit()
