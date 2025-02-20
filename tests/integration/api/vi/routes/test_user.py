import json

import pytest
from flask import Flask

from app.api.v1.routes.user import user_routes
from app.core.database.database import Database
from app.settings import settings


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    settings.DB_PATH = "test.db"
    Database.reinitializate_db()
    app = Flask(__name__)
    app.register_blueprint(user_routes, url_prefix=settings.API_V1_PREFIX)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_list_all_users_empty(client):
    """GET /users should return an empty list when no users exist."""
    response = client.get(f"{settings.API_V1_PREFIX}/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_create_get_update_delete_user(client):
    """Test the full user lifecycle: create, get, update, and delete."""
    new_user_payload = {"name": "Test User", "email": "test.user@example.com"}
    post_response = client.post(
        f"{settings.API_V1_PREFIX}/users",
        data=json.dumps(new_user_payload),
        content_type="application/json",
    )
    assert post_response.status_code == 201
    created_user = post_response.get_json()
    assert "id" in created_user
    user_id = created_user["id"]

    # Get the created user
    get_response = client.get(f"{settings.API_V1_PREFIX}/users/{user_id}")
    assert get_response.status_code == 200
    user_data = get_response.get_json()
    assert user_data.get("id") == user_id
    assert user_data.get("name") == new_user_payload["name"]
    assert user_data.get("email") == new_user_payload["email"]

    # Update the user
    updated_payload = {"name": "Updated User", "email": "updated.user@example.com"}
    put_response = client.put(
        f"{settings.API_V1_PREFIX}/users/{user_id}",
        data=json.dumps(updated_payload),
        content_type="application/json",
    )
    assert put_response.status_code == 200
    updated_user = put_response.get_json()
    assert updated_user.get("name") == updated_payload["name"]
    assert updated_user.get("email") == updated_payload["email"]

    # Delete the user
    delete_response = client.delete(f"{settings.API_V1_PREFIX}/users/{user_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.get_json()
    assert "message" in delete_data

    # Ensure the user no longer exists
    get_deleted_response = client.get(f"{settings.API_V1_PREFIX}/users/{user_id}")
    assert get_deleted_response.status_code == 404


def test_get_nonexistent_user(client):
    """GET /users/<id> should return a 404 for a non-existent user."""
    response = client.get(f"{settings.API_V1_PREFIX}/users/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_update_user_invalid_input(client):
    """PUT /users/<id> should return a 400 error if required fields are missing."""
    # Create a user first
    payload = {"name": "Test User", "email": "test.user@example.com"}
    post_response = client.post(
        f"{settings.API_V1_PREFIX}/users",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert post_response.status_code == 201
    user_id = post_response.get_json()["id"]

    # Try updating with missing name (only email provided)
    invalid_payload = {"email": "new.email@example.com"}
    put_response = client.put(
        f"{settings.API_V1_PREFIX}/users/{user_id}",
        data=json.dumps(invalid_payload),
        content_type="application/json",
    )
    assert put_response.status_code == 400
    data = put_response.get_json()
    assert "error" in data


def test_delete_nonexistent_user(client):
    """DELETE /users/<id> should return a 404 when deleting a non-existent user."""
    response = client.delete(f"{settings.API_V1_PREFIX}/users/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
