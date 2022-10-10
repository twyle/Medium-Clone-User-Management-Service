# -*- coding: utf-8 -*-
"""This module contains the Admin user model."""
from ..models import User
from ..extensions import db, ma


class Admin(User):
    """The Admin Model."""

    __tablename__ = "admins"
    
    id: int = db.Column(db.Integer, primary_key=True)


class AdminSchema(ma.Schema):
    """Show all the admin information."""

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
        )
        
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)