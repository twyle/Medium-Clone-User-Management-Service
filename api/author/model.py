# -*- coding: utf-8 -*-
"""This module contains the Author user model."""
from sqlalchemy.dialects.postgresql import ARRAY
from ..models import User
from ..extensions import db, ma


class Author(User):
    """The Author Model."""

    __tablename__ = "authors"
    
    id: int = db.Column(db.Integer, primary_key=True)
    bio: str = db.Column(db.Text, nullable=True)
    interests: list = db.Column(ARRAY(db.String(100)), nullable=True)
    follows: list = db.Column(ARRAY(db.Integer), nullable=True)
    followers: list = db.Column(ARRAY(db.Integer), nullable=True)
    
    
    @staticmethod
    def validate_bio(bio: str):
        """Validate the given name."""
        pass
    
    @classmethod
    def get_followers(cls, author_id: int):
        """Get the authors followers."""
        return cls.query.filter_by(id=author_id).first().followers
    
    @classmethod
    def get_follows(cls, author_id: int):
        """Get the authors follows."""
        return cls.query.filter_by(id=author_id).first().follows
    

class AuthorSchema(ma.Schema):
    """Show all the author information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "first_name",
            "last_name",
            "screen_name",
            "email_address",
            "date_registered",
            "profile_picture",
            "bio",
        )

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)