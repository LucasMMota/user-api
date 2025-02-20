"""User routes module."""
from flask import Blueprint, request, jsonify

from app.core.services.user_service import UserService
from app.logger import logger

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users", methods=["GET"])
def list_all_users():
    """Returns all users from the database."""
    return jsonify(UserService().list_all()), 200


@user_routes.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """Returns a user by its ID."""
    user = UserService().get_user(user_id)
    if not user:
        logger.info(f"m=get_user, User {user_id} not found")
        return jsonify({"error": "User not found"}), 404

    logger.info(f"m=get_user, User found: {user.get('id')}")
    return jsonify(user), 200


@user_routes.route("/users", methods=["POST"])
def create_user():
    """Creates a new user."""
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    try:
        user = UserService().create_user(name, email)
        if not user:
            logger.error(
                f"m=create_user, Error creating new user. Verify input, name={name}, email={email}"
            )
            return jsonify({"error": "Error creating new user. Verify input."}), 409

        logger.info(f"m=create_user, User created: {user.get('id')}")
        return jsonify(user), 201
    except Exception as e:
        logger.error(f"m=create_user, Internal Server Error, error={str(e)}")
        return (
            jsonify({"error": "Internal Server Error"}),
            500,
        )  # todo check interceptors


@user_routes.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    """Updates a user by its ID."""
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        # assuming we want to update both fields updated at the same time
        logger.error(f"m=update_user, Ivalid input, name={name}, email={email}")
        return jsonify({"error": "Name and email are required"}), 400

    try:
        updated_user = UserService().update_user(user_id, name, email)
        if not updated_user:
            logger.error(f"m=update_user, User {user_id} not found")
            return jsonify({"error": "User not found"}), 404

        return jsonify(updated_user), 200
    except Exception as e:
        logger.error(f"m=update_user, Internal Server Error, error={str(e)}")
        return (
            jsonify({"error": "Internal Server Error"}),
            500,
        )  # todo check interceptors


@user_routes.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """Deletes a user by its ID."""
    if not UserService().delete_user(user_id):
        logger.error(f"m=delete_user, Error deleting user {user_id}")
        return jsonify({"error": "Error deleting user"}), 404

    return jsonify({"message": f"User {user_id} deleted successfully"}), 200
