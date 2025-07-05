import os
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import get_password_hash, verify_password, create_access_token
from deps import get_db, require_role, get_current_user
from schemas import UserCreate, Token, UserOut
from models import User, Base

router = APIRouter(prefix="/api", tags=["auth"])
# Inicializar BD
Base.metadata.create_all(bind=SessionLocal().bind)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed, role="user")
    db.add(db_user)
    try:
        db.commit(); db.refresh(db_user)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email in use")
    return {"id": db_user.id}

@router.post("/register-admin", status_code=status.HTTP_201_CREATED)
def register_admin(
    user: UserCreate,
    x_admin_secret: str = Header(None),
    db: Session = Depends(get_db)
):
    if x_admin_secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed, role="admin")
    db.add(db_user)
    try:
        db.commit(); db.refresh(db_user)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email in use")
    return {"id": db_user.id}

@router.post("/login", response_model=Token)
def login(credentials: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = create_access_token(user.id, user.role)
    return {"access_token": token}

@router.get("/me", response_model=UserOut)
def read_me(current_user=Depends(get_current_user)):
    return current_user

@router.get("/admin-only", dependencies=[Depends(require_role("admin"))])
async def admin_only():
    return {"msg": "Bienvenido, admin"}
