import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, engine, SessionLocal
from app.routes.vote import get_db

# 1) Creamos un engine SQLite en memoria.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 2) Fixture para inicializar esquemas antes de cada sesión de pruebas.
@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 3) Override de la dependencia get_db para usar la sesión de pruebas.
@pytest.fixture(scope="function")
def db_session(monkeypatch):
    def _get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    monkeypatch.setattr("app.routes.vote.get_db", _get_test_db)
    return TestingSessionLocal()

# 4) Cliente de test FastAPI
@pytest.fixture(scope="function")
def client(db_session):
    return TestClient(app)
