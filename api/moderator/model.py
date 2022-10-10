# -*- coding: utf-8 -*-
"""This module contains the Moderator user model."""
from ..models import User
from ..extensions import db, ma


class Moderator(User):
    """The Moderator Model."""

    __tablename__ = "moderators"
    
    id: int = db.Column(db.Integer, primary_key=True)
    bio: str = db.Column(db.Text, nullable=True)

class ModeratorSchema(ma.Schema):
    """Show all the moderator information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "first_name",
            "last_name",
            "screen_name",
            "email",
            "date_registered",
            "profile_pic",
            "bio",
        )

moderator_schema = ModeratorSchema()
moderators_schema = ModeratorSchema(many=True)