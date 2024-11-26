import sys 
import os

#   Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pytest
import uuid
from src.db.database import get_session
from src.utils.dependencies import AccessTokenBearer, RoleChecker, RefreshTokenBearer
from src.models.models import Book
from src.app import app
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock

import warnings

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="jsonschema.exceptions.RefResolutionError is deprecated"
)


mock_session = Mock()
mock_user_service = Mock()
mock_book_service = Mock()


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(["admin"])

def get_mock_session():
    yield mock_session
    

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer] = Mock()
 

@pytest.fixture
def fake_session():
    return mock_session

@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def fake_book_service():
    return mock_book_service

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def test_book():
    return Book(
        uid=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        title="The Great Gatsby",
        description="A novel about the American Dream",
        page_count=384,
        language="English", 
        publish_date=datetime.now(),
        updated_at=datetime.now()
    )