from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime
import enum
from content.models import Article, PracticeQuestion

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    class UserType(enum.Enum):
        USER = "user"
        ADMIN = "admin"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(100), nullable=False)
    email = db.Column(db.string(100), unique=True, nullable=False)
    password_hash = db.Column(db.string(255), nullable=False)
    role = db.Column(Enum(UserType), nullable=False, default=UserType.USER)

    # auto fields
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __str__(self):
        return f"{self.username}"
    
    def __repr__(self):
        return f"{self.username}: {self.email}"

class Profile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    petname = db.Column(db.string(100), nullable=True)
    bio = db.Column(db.string(200), nullable=True)
    profile_img = db.Column(db.string(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # auto fields
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    class ContentType(enum.Enum):
        QUESTION = "question"
        ARTICLE = "article"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    content_type = db.Column(Enum(ContentType), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)

    # auto fields
    completed_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    @property
    def content(self):
        if self.content_type == self.ContentType.QUESTION:
            return db.session.get(PracticeQuestion, self.content_id)
        elif self.content_type == self.ContentType.ARTICLE:
            return db.session.get(Article, self.content_id)