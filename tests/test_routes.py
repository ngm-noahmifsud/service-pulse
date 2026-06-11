import sys
from pathlib import Path
import os
import pytest
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL")

from models import db, Service, ServiceStatus
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Service" in response.data


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "healthy"}


def test_home_page_displays_services(client):
    with client.application.app_context():
        status = ServiceStatus(name="TEST")
        db.session.add(status)
        db.session.flush()

        service = Service(name="Test Service", status_id=status.id)
        db.session.add(service)
        db.session.commit()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Test Service" in response.data
    assert b"TEST" in response.data