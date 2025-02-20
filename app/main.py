"""Main module for the Flask app."""
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from app.api.v1.routes.user import user_routes

from app.core.database.database import Database
from app.logger import logger
from app.settings import settings

Database.initialize_db()

logger.info("Application starting...")
app = Flask(__name__)
app.register_blueprint(user_routes, url_prefix=settings.API_PREFIX)


@app.errorhandler(Exception)
def handle_exception(error):
    """Global error handler for the application. Intercept all exceptions and log them."""
    # If it's an HTTPException, let Flask handle it normally.
    if isinstance(error, HTTPException):
        return error

    logger.error(
        f"m=handle_exception, Unhandled exception at path {request.path}: {error}"
    )
    response = jsonify({
        "detail": "Internal server error =/ Please contact the support team."
    })
    response.status_code = 500
    return response
