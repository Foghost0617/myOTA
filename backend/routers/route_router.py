from fastapi import APIRouter, HTTPException, status,Depends, Query
from sqlalchemy.orm import Session
from backend.schemas.route_schema import RouteCreate, RouteOut, RouteSpotCreate, RouteSpotOut, RouteEnrollmentCountOut
from backend.services.route_service import RouteService
from backend.core.database import SessionLocal  # 直接导入SessionLocal
from typing import List
from backend.models.route_model import RouteSpot  # 导入 ORM 模型类
from fastapi import UploadFile, File, APIRouter, HTTPException

import os
from uuid import uuid4
from sqlalchemy.orm import Session


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

# 创建景点（多个）
@router.post("/route_spots/")
def create_route_spots(spots: List[RouteSpotCreate]):
     db: Session = SessionLocal()
     try:
         route_spot_service = RouteService(db)
         db_spots = route_spot_service.create_route_spots(spots)
         if not db_spots:
             raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail="无法创建景点"
             )
         return db_spots
     finally:
         db.close()




# 找对应旅社
@router.get("/agency/{agency_id}", response_model=List[RouteOut])
def get_routes_by_agency(agency_id: int):
    db: Session = SessionLocal()
    try:
        # 初始化 RouteService 实例
        route_service = RouteService(db)
        # 调用 service 层的方法获取路线数据
        routes = route_service.get_routes_by_agency(agency_id)
        # 如果没有找到相关路线，返回 404 错误
        if not routes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No routes found for agency {agency_id}"
            )

        # 返回获取到的路线数据
        return routes
    finally:
        # 确保数据库会话被正确关闭
        db.close()
#应该和上面一样，但是不记得前端是否都调用了 暂时不删
@router.get("/assign/{agency_id}", response_model=List[RouteOut])
def get_routes_by_agency(agency_id: int):
    db: Session = SessionLocal()
    try:
        # 初始化 RouteService 实例
        route_service = RouteService(db)
        # 调用 service 层的方法获取路线数据
        routes = route_service.get_routes_by_agency(agency_id)
        # 如果没有找到相关路线，返回 404 错误
        if not routes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No routes found for agency {agency_id}"
            )

        # 返回获取到的路线数据
        return routes
    finally:
        # 确保数据库会话被正确关闭
        db.close()


@router.get("/all", response_model=List[RouteOut])
def get_routes():
    db: Session = SessionLocal()
    try:
        route_service = RouteService(db)

        # 获取所有路线数据，不做分页
        routes = route_service.get_all_routes()
        print(routes)

        # 如果没有找到相关路线，返回 404 错误
        if not routes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No routes found"
            )

        # 返回所有路线数据
        return routes

    finally:
        db.close()  # 确保会话被关闭


# @router.get("/all", response_model=List[RouteOut])
# def get_routes(skip: int = 0, limit: int = 3):
#     db: Session = SessionLocal()
#     try:
#         route_service = RouteService(db)
#         routes = route_service.get_all_routes(skip, limit)
#
#         if not routes:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="No routes found"
#             )
#
#         return routes
#
#     finally:
#         db.close()  # 确保会话被关闭


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

#
# @router.delete("/del/{route_id}")
# def delete_route(route_id: int):
#     db: Session = SessionLocal()
#     try:
#         print(f"Deleting route with ID: {route_id}")
#         route_service = RouteService(db)
#         result = route_service.delete_route(route_id)
#         if result:
#             return {"message": f"Route {route_id} deleted successfully"}
#         else:
#             print(f"Route {route_id} not found in the database")
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Route {route_id} not found"
#             )
#     finally:
#         db.close()

@router.delete("/del/{route_id}")
def delete_route(route_id: int):
    db: Session = SessionLocal()
    try:
        route_service = RouteService(db)
        success = route_service.delete_route(route_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Route with id {route_id} not found or could not be deleted"
            )
        return {"message": f"Route {route_id} deleted successfully"}
    finally:
        db.close()


@router.get("/enrollment-count/{route_id}", response_model=RouteEnrollmentCountOut)
def get_enrollment_count(route_id: int):
    db: Session = SessionLocal()
    try:
        route_service = RouteService(db)
        result = route_service.get_enrollment_count_info(route_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    finally:
        db.close()



# @router.post("/spot_images/{spot_id}")
# async def upload_spot_image(spot_id: int, file: UploadFile = File(...)):
#     db: Session = SessionLocal()
#     try:
#         # 创建保存目录
#         save_dir = "static/spot_images"
#         os.makedirs(save_dir, exist_ok=True)
#
#         # 获取文件扩展名
#         ext = os.path.splitext(file.filename)[-1]
#         # 防止重复名，生成唯一文件名
#         filename = f"{uuid4().hex}{ext}"
#         file_path = os.path.join(save_dir, filename)
#
#         # 保存文件
#         with open(file_path, "wb") as f:
#             content = await file.read()
#             f.write(content)
#
#         # 更新数据库中的 image_url 字段
#         image_url = f"/{file_path}"  # 可视路径，前端访问用
#
#
#         route_service = RouteService(db)
#         success = route_service.update_spot_image_url(spot_id, image_url)
#
#         if not success:
#             raise HTTPException(status_code=404, detail="景点不存在或更新失败")
#
#         return {"message": "上传成功", "image_url": image_url}
#
#     finally:
#         db.close()

@router.post("/spot_images/{spot_id}")
async def upload_spot_image(spot_id: int, file: UploadFile = File(...)):
    db: Session = SessionLocal()
    try:
        # 创建保存目录
        save_dir = "static/spot_images"
        os.makedirs(save_dir, exist_ok=True)

        # 获取文件扩展名
        ext = os.path.splitext(file.filename)[-1]
        # 防止重复名，生成唯一文件名
        filename = f"{uuid4().hex}{ext}"
        file_path = os.path.join(save_dir, filename)

        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 更新数据库中的 image_url 字段，确保返回路径格式正确
        image_url = f"/static/spot_images/{filename}"  # 修改为正确的可视路径

        # 更新数据库
        route_service = RouteService(db)
        success = route_service.update_spot_image_url(spot_id, image_url)

        if not success:
            raise HTTPException(status_code=404, detail="景点不存在或更新失败")

        return {"message": "上传成功", "image_url": image_url}

    finally:
        db.close()
