# add ellection to get voterinos

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from datetime import datetime

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/election", response_model=schemas.ElectionOut)
def create_election(election: schemas.ElectionCreate, db: Session = Depends(get_db)):
    new_election = models.Election(
        title=election.title,
        description=election.description,
        start_time=election.start_time or datetime.utcnow(),
        end_time=election.end_time,
        is_active=True,
    )
    db.add(new_election)
    db.commit()
    db.refresh(new_election)
    return new_election

