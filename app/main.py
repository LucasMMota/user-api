"""Main module for the Flask app."""
from flask import Flask

from app.api.v1.routes.user import user_routes

from app.core.database.database import Database
from app.logger import logger
from app.settings import settings

Database.initialize_db()

logger.info("Application starting...")
app = Flask(__name__)
app.register_blueprint(user_routes, url_prefix=settings.API_PREFIX)

if __name__ == "__main__":
    app.run(debug=True)
