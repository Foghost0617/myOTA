# routers/route_guide.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.route_guide import RouteGuideCreate, RouteGuideOut
from backend.services.route_guide import RouteGuideService
from backend.core.database import SessionLocal  # 直接导入SessionLocal


router = APIRouter(
    prefix="/route_guide",  # 路由前缀
    tags=["分配路线"]  # 为路由分配标签，便于文档管理
)


# 创建导游指派
@router.post("/create", response_model=RouteGuideOut)
def assign_guide_to_route(route_guide: RouteGuideCreate):
    db: Session = SessionLocal()
    try:
        route_guide_service = RouteGuideService(db)
        db_route_guide = route_guide_service.create_route_guide(route_guide)

        # 如果没有创建成功，返回 400 错误
        if not db_route_guide:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法指派导游到此路线"
            )

        return db_route_guide
    finally:
        db.close()