from flask import Blueprint, request, jsonify

from app.core.services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)


@user_bp.route("/users", methods=["GET"])
def list_all_users():
    """Returns all users from the database."""  # todo pagination?
    users = UserService().list_all()
    return jsonify(users), 200


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = UserService().get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200


@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    # todo check if already exists

    try:
        user = UserService().create_user(name, email)
        if not user:
            return jsonify({"error": "Error creating new user"}), 409

        return jsonify(user), 201 # change to object response
    except Exception as e:
        # todo log
        return jsonify({"error": "Internal Server Error"}), 500 # todo check interceptors


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        # assuming we want to update both fields at the same time
        return jsonify({"error": "Name and email are required"}), 400

    try:
        updated_user = UserService().update_user(user_id, name, email)
        if not updated_user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(updated_user), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500  # todo check interceptors


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    if not UserService().delete_user(user_id):
        return jsonify({"error": "Error deleting user"}), 404

    return jsonify({"message": f"User {user_id} deleted successfully"}), 200
