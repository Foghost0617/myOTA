from sqlalchemy.orm import Session

from backend.models.complaints_model import Complaint
from backend.schemas.complaints_schemas import ComplaintCreate, ComplaintStatusUpdate


class ComplaintService:
    def __init__(self, db: Session):
        self.db = db

    def create_complaint(self, complaint_data: ComplaintCreate) -> Complaint:
        complaint = Complaint(
            tourist_id=complaint_data.tourist_id,
            content=complaint_data.content
        )
        self.db.add(complaint)
        self.db.commit()
        self.db.refresh(complaint)
        return complaint

    def get_all_complaints(self):
        return self.db.query(Complaint).order_by(Complaint.created_at.desc()).all()

    def update_complaint_status(self, complaint_id: int, status_data: ComplaintStatusUpdate) -> Complaint:
        complaint = self.db.query(Complaint).filter(Complaint.id == complaint_id).first()
        if complaint:
            complaint.status = status_data.status
            self.db.commit()
            self.db.refresh(complaint)
        return complaint




