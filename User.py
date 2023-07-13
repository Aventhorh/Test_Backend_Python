from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username: str, email: str):
        """
        Initialize a User object.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
        """
        self.username = username
        self.email = email
