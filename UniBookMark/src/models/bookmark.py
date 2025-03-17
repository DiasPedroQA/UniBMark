# pylint: disable=C

from flask_sqlalchemy import SQLAlchemy
from src import db

db = SQLAlchemy()


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Bookmark {self.title}>"
