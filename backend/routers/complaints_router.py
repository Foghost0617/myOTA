from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List
from backend.core.database import SessionLocal
from backend.schemas.complaints_schemas import ComplaintCreate, ComplaintStatusUpdate,ComplaintOut
from backend.services.complaints_service import ComplaintService

router = APIRouter(prefix="/complaints", tags=["投诉"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 游客提交投诉
@router.post("/submit", response_model=ComplaintOut)
def create_complaint(complaint_data: ComplaintCreate, db: Session = Depends(get_db)):
    service = ComplaintService(db)
    return service.create_complaint(complaint_data)

# 文旅查看所有投诉
@router.get("/check", response_model=List[ComplaintOut])
def get_all_complaints(db: Session = Depends(get_db)):
    service = ComplaintService(db)
    return service.get_all_complaints()

# 文旅更新投诉状态为“已处理”
@router.put("/{complaint_id}", response_model=ComplaintOut)
def update_status(complaint_id: int, status_data: ComplaintStatusUpdate, db: Session = Depends(get_db)):
    service = ComplaintService(db)
    updated = service.update_complaint_status(complaint_id, status_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="投诉不存在")
    return updated
