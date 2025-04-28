# routers/route_guide.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.models.route_guide import RouteGuide
from backend.schemas.route_guide import RouteGuideCreate, RouteGuideOut
from backend.schemas.user import GuideOut
from backend.services.route_guide import RouteGuideService
from backend.core.database import SessionLocal  # 直接导入SessionLocal


router = APIRouter(
    prefix="/route_guide",  # 路由前缀
    tags=["分配路线"]  # 为路由分配标签，便于文档管理
)


@router.get("/check/{route_id}")
def check_route_assignment(route_id: int):
    db: Session = SessionLocal()  # 创建数据库会话
    try:
        route_guide_service = RouteGuideService(db)
        is_assigned = route_guide_service.check_assigned(route_id)  # 调用服务层的检查方法
        return {"is_assigned": is_assigned}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"检查指派失败: {str(e)}"
        )
    finally:
        db.close()  # 关闭数据库会话


@router.post("/create", response_model=RouteGuideOut)
def assign_guide(route_guide_create: RouteGuideCreate):
    db: Session = SessionLocal()  # 获取数据库会话
    try:
        # 创建 service 实例并进行导游指派
        service = RouteGuideService(db)
        result = service.assign_guide(route_guide_create)

        # 返回创建的导游指派信息
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"导游指派失败: {str(e)}"
        )
    finally:
        db.close()


# 根据旅行社获取所有导游
@router.get("/get_guides_by_agency/{agency_id}", response_model=List[GuideOut])
def get_guides_by_agency(agency_id: int):
    db: Session = SessionLocal()
    try:
        guide_service = RouteGuideService(db)
        guides = guide_service.get_guides_by_agency(agency_id)

        # 如果没有找到导游，抛出 404 异常
        if not guides:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="没有找到该旅行社的导游"
            )

        # 将 SQLAlchemy 对象转换为 Pydantic 模型
        return guides  # FastAPI 会根据 response_model 自动转换为 GuideOut
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取导游列表失败: {str(e)}"
        )


# 根据旅社获取路线记录
@router.get("/{agency_id}/all")
async def get_route_guides_by_agency(agency_id: int):
    db: Session = SessionLocal()  # 直接创建数据库会话
    route_guide_service = RouteGuideService(db)
    route_guides = route_guide_service.get_route_guides_by_agency(agency_id)
    db.close()  # 使用完后关闭会话
    return route_guides

# 删除指定的指派记录
@router.delete("/del/{route_guide_id}")
async def delete_route_guide(route_guide_id: int):
    db: Session = SessionLocal()  # 直接创建数据库会话
    route_guide_service = RouteGuideService(db)
    success = route_guide_service.delete_route_guide(route_guide_id)
    db.close()  # 使用完后关闭会话
    if not success:
        raise HTTPException(status_code=404, detail="指派记录未找到")
    return {"message": "指派记录删除成功"}


# 获取导游的所有被指派记录
@router.get("/guide/{guide_id}")
async def get_route_guides_by_guide(guide_id: int):
    db: Session = SessionLocal()
    try:
        # 查询导游的所有指派记录
        route_guides = db.query(RouteGuide).filter(RouteGuide.guide_id == guide_id).all()

        if not route_guides:
            raise HTTPException(status_code=404, detail="没有找到该导游的指派记录")

        return route_guides

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指派记录失败: {str(e)}")


