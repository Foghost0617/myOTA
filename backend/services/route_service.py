from http.client import HTTPException

from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from backend.models.route_model import Route, RouteSpot
from backend.models.tourist_route_model import TouristRouteRelation
from backend.schemas.route_schema import RouteCreate, RouteOut, RouteSpotCreate, RouteSpotOut, RouteEnrollmentCountOut


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
                sequence=spot.sequence,
                image_url = spot.image_url
            )
            db_spots.append(db_spot)

        self.db.add_all(db_spots)  # 批量添加景点
        self.db.commit()

        return db_spots  # 返回创建的景点列表

    # def get_routes_by_agency(self, agency_id: int) -> List[RouteOut]:
    #     # 查询该 agency_id 下所有的路线
    #     routes = self.db.query(Route).filter(Route.agency_id == agency_id).all()
    #
    #     # 打印查询结果，检查是否正确获取了多条记录
    #     print(f"查询到的路线: {routes}")
    #
    #     return [RouteOut.from_orm(route) for route in routes] if routes else []

    def get_routes_by_agency(self, agency_id: int) -> List[RouteOut]:
            return self.db.query(Route).filter(Route.agency_id == agency_id).all()

    # def get_routes_by_agency(self, agency_id: int, skip: int = 0, limit: int = 3) -> List[RouteOut]:
    #         return self.db.query(Route).filter(Route.agency_id == agency_id).offset(skip).limit(limit).all()

    def get_all_routes(self) -> List[Route]:
        routes = self.db.query(Route).all()
        print(f"返回的数据: {routes}")
        return routes



    def get_enrollment_count_info(self, route_id: int) -> RouteEnrollmentCountOut:
        # 查找路线
        route = self.db.query(Route).filter(Route.id == route_id).first()
        if not route:
            raise ValueError("路线不存在")

        # 统计报名人数
        count = self.db.query(func.count()).select_from(TouristRouteRelation).filter(
            TouristRouteRelation.route_id == route_id
        ).scalar()

        return RouteEnrollmentCountOut(
            route_id=route.id,
            route_name=route.name,
            count=count
        )



    def get_route_spots(self, route_id: int) -> List[RouteSpotOut]:
        # 查询并按景点顺序获取某条路线的所有景点
        route_spots = self.db.query(RouteSpot).filter(RouteSpot.route_id == route_id).order_by(RouteSpot.sequence).all()
        return [RouteSpotOut.from_orm(spot) for spot in route_spots]



    # def delete_route(self, route_id: int):
    #     route = self.db.query(Route).filter(Route.id == route_id).first()
    #     if route:
    #         self.db.delete(route)
    #         self.db.commit()
    #         return {"message": f"Route {route_id} deleted successfully"}
    #     else:
    #         return None  # 不存在时返回 None，让路由层处理

    def delete_route(self, route_id: int) -> bool:
        # 先删除关联的游客记录
        self.db.query(TouristRouteRelation).filter_by(route_id=route_id).delete(synchronize_session=False)

        # 删除所有景点
        self.db.query(RouteSpot).filter_by(route_id=route_id).delete(synchronize_session=False)

        # 删除路线本身
        route = self.db.query(Route).filter_by(id=route_id).first()
        if not route:
            return False

        self.db.delete(route)
        self.db.commit()
        return True




    # 上传图像
    def update_spot_image_url(self, spot_id: int, image_url: str) -> bool:
        spot = self.db.query(RouteSpot).filter(RouteSpot.id == spot_id).first()
        if not spot:
            return False
        spot.image_url = image_url
        self.db.commit()
        return True

