# add ellection to get voterinos
# Add token generation
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from datetime import datetime
import secrets
from typing import List

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


@router.post("/generate-tokens", response_model=List[schemas.VoterTokenOut])
def generate_tokens(
    request: schemas.TokenBatchRequest, db: Session = Depends(get_db)
):
    # Verificar que la elección exista
    election = db.query(models.Election).filter_by(id=request.election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    tokens = []
    for _ in range(request.count):
        token = secrets.token_urlsafe(16)
        voter = models.Voter(token=token, election_id=request.election_id)
        db.add(voter)
        tokens.append({"token": token})

    db.commit()
    return tokens
