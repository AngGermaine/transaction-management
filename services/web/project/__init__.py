from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.routes import app_routes

import os

# Initialize the Flask app
app = Flask(__name__)

app.secret_key = os.urandom(24)


# Load the configuration
app.config.from_object("project.config.Config")

# Initialize SQLAlchemy
db = SQLAlchemy(app)
app.register_blueprint(app_routes)


# Define the Game model based on your table schema
class Game(db.Model):
    __tablename__ = "games"  # Ensure the table name matches the one in your database
    
    # Define columns based on your schema
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing ID
    game_name = db.Column(db.String(255), nullable=False)  # Game name (up to 255 characters)
    release_year = db.Column(db.Integer, nullable=False)  # Year of release
    release_month = db.Column(db.Integer, nullable=False)  # Month of release (1-12)
    release_day = db.Column(db.Integer, nullable=False)  # Day of release (1-31)

    def __init__(self, game_name, release_year, release_month, release_day):
        self.game_name = game_name
        self.release_year = release_year
        self.release_month = release_month
        self.release_day = release_day


if __name__ == "__main__":
    app.run(debug=True)