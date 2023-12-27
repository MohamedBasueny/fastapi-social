from fastapi.testclient import TestClient 
from app.main import app 
from app.schemas import UserOut
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db , Base
import pytest 

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0716103235@localhost/fastapi_test"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#use this to create tables based on the models .... must import Base from database.py

@pytest.fixture(scope="function")
def session():
    #returns a database session and do the cleaning  
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client (session): #returns a test client that overrides the dev database with a test one 
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) 
