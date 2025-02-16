from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime
import enum

db = SQLAlchemy()

class Article(db.Model):
    __tablename__="articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="DO_NOTHING"), unique=True, nullable=False)
    image_url = db.Column(db.string(100), nullable=True)
    gif_url = db.Column(db.string(100), nullable=True)
    

    # auto fields
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

class Category(db.Model):
    __tablename__="categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    # auto fields
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class PracticeQuestion(db.Model):
    __tablename__="practice_questions"

    class DifficultyType(enum.Enum):
        HARD = "hard"
        MEDIUM = "medium"
        EASY = "easy"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    question_link = db.Column(db.String(), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="DO_NOTHING"), unique=True, nullable=False)
    difficulty = db.Column(Enum(DifficultyType), nullable=False)

    # auto fields
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
