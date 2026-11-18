
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import pytest
from app.app import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        tasks.clear()
        tasks.extend([
            {"id": 1, "title": "Learn DevOps", "completed": False},
            {"id": 2, "title": "Build CI/CD Pipeline", "completed": False}
        ])
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) == 2


def test_add_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Complete Assignment"}
    )
    assert response.status_code == 201
    assert response.json["title"] == "Complete Assignment"


def test_invalid_task(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
