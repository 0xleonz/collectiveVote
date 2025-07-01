# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
import os

# 1. URL de conexión (puedes parametrizar con env vars si quieres)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./collectivevote.db")

# 2. Motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# 3. Fabrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 4. Base para todos los modelos
Base = declarative_base()

def init_db() -> None:
    """
    Crea todas las tablas en la base de datos según los modelos que hereden de Base.
    Llamar en el evento 'startup' de FastAPI.
    """
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    """
    Dependency para FastAPI: abre una sesión de DB, la cede al endpoint, 
    y se asegura de cerrarla al terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
