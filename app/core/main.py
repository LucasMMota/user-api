"""Main module for the Flask app."""
from flask import Flask

from app.api.v1.routes.user import user_bp

from app.core.database.database import Database

"""Factory function that creates and configures a Flask app."""

# Database.recreate_db()  # TODO REMOVER
Database.initialize_db()  # TODO test after if will create without explicit import

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
