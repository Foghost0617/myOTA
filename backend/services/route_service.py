from sqlalchemy.orm import Session
from typing import List
from backend.models.route_model import Route, RouteSpot
from backend.schemas.route_schema import RouteCreate, RouteOut, RouteSpotCreate,RouteSpotOut


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

        # 获取某个旅社的所有路线（只包含名称和简介）

    def get_routes_by_agency(self, agency_id: int) -> List[RouteOut]:
        # 查询该 agency_id 下所有的路线
        routes = self.db.query(Route).filter(Route.agency_id == agency_id).all()

        # 打印查询结果，检查是否正确获取了多条记录
        print(f"查询到的路线: {routes}")

        return [RouteOut.from_orm(route) for route in routes] if routes else []

        # 获取某条路线的所有景点

    def get_route_spots(self, route_id: int) -> List[RouteSpotOut]:
        # 查询并按景点顺序获取某条路线的所有景点
        route_spots = self.db.query(RouteSpot).filter(RouteSpot.route_id == route_id).order_by(RouteSpot.sequence).all()
        return [RouteSpotOut.from_orm(spot) for spot in route_spots]


