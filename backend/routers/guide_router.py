from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from backend.schemas.user import GuideUpdate, GuideOut,TravelAgencyOut
from backend.services.guide_service import GuideService
from backend.core.database import SessionLocal
from typing import List

router = APIRouter(
    prefix="/guides",
    tags=["导游"]
)

# 后端更新导游信息的接口
@router.put("/update_info", response_model=GuideOut)
def update_guide_info(guide_data: GuideUpdate):
    db: Session = SessionLocal()
    try:
        guide_service = GuideService(db)
        updated_guide = guide_service.update_guide_info(guide_data.guide_id, guide_data)
        if not updated_guide:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="导游信息不存在"
            )
        return updated_guide
    finally:
        db.close()



# 获取所有旅行社
@router.get("/allTA", response_model=List[TravelAgencyOut])
def get_all_agencies():
    db: Session = SessionLocal()
    try:
        travel_agency_service = GuideService(db)
        agencies = travel_agency_service.get_all_agencies()
        if not agencies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到旅行社"
            )
        return agencies
    finally:
        db.close()

