from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from backend.schemas.user import GuideUpdate, GuideOut,TravelAgencyOut,AgencyIdOut
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

# 获取所有导游
@router.get("/allguides", response_model=List[GuideOut])
def get_guides(skip: int = 0, limit: int = 10):
    db: Session = SessionLocal()
    try:
        guide_service = GuideService(db)
        guides = guide_service.get_guides(skip, limit)
        if not guides:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="没有找到导游"
            )
        return guides
    finally:
        db.close()

@router.get("/agency/{guide_id}", response_model=AgencyIdOut)
def get_agency_id(guide_id: int):
    db: Session = SessionLocal()
    try:
        guide_service = GuideService(db)
        agency_id = guide_service.get_agency_id_by_guide(guide_id)

        if agency_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Guide with ID {guide_id} not found or no agency assigned"
            )

        return {"agency_id": agency_id}
    finally:
        db.close()
