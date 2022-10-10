from email.policy import default
from ..extensions import db, ma, bcrypt
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from .helpers import (
    is_email_address_format_valid,
    is_user_name_valid,
    is_user_password_valid,
    check_if_email_id_match
)

class User(db.Model):
    """The User Model."""

    __abstract__ = True
    first_name: str = db.Column(db.String(100), nullable=False)
    last_name: str = db.Column(db.String(100), nullable=False)
    email_address: str = db.Column(db.Text, nullable=False, unique=True)
    profile_picture: str = db.Column(db.String(100), nullable=True)
    password_hash: str = db.Column(db.String(100), nullable=False)
    registered_on: datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    is_active: bool = db.Column(db.Boolean(), default=False)
    is_authenticated: bool = db.Column(db.Boolean(), default=False)
    nick_name: str = db.Column(db.String(100), nullable=True)
    
    @property
    def password(self):
        """Raise an exception when password is accessed."""
        raise AttributeError("Password is a write-only field!")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """Check if password hash is correct."""
        return bcrypt.check_password_hash(self.password_hash, password)     
    
    @classmethod
    def user_with_id_exists(cls, user_id):
        """Check if user with given id exists."""
        if cls.query.filter_by(id=user_id).first():
            return True
        return False
    
    @classmethod
    def user_with_email_exists(cls, user_email):
        """Check if user with given email exists."""
        if cls.query.filter_by(email_address=user_email).first():
            return True
        return False
    
    @staticmethod
    def validate_name(name):
        """Validate the given name."""
        is_user_name_valid(name)
    
    @staticmethod
    def validate_password(password):
        """Validate the given name."""
        is_user_password_valid(password)
    
    @staticmethod
    def validate_email(email):
        """Validate the given name."""
        is_email_address_format_valid(email)
    
    @staticmethod
    def validate_screen_name(screen_name):
        """Validate the given name."""
        if not isinstance(screen_name, str):
            raise TypeError('The Screen name has to be a string')
        if len(screen_name) < 3:
            raise ValueError('The screen name has to be longer than three.')
    
    
    @classmethod    
    def validate_user(cls, user_id, email):
        """Check if user id and email belong to the same person."""
        check_if_email_id_match(cls, user_id, email)
        

class Author(User):
    """The Author Model."""

    __tablename__ = "authors"
    
    id: int = db.Column(db.Integer, primary_key=True)
    bio: str = db.Column(db.Text, nullable=True)
    interests: list = db.Column(ARRAY(db.String(100)), nullable=True)
    follows: list = db.Column(ARRAY(db.Integer), nullable=True)
    followers: list = db.Column(ARRAY(db.Integer), nullable=True)
    
    
    @staticmethod
    def validate_bio(name):
        """Validate the given name."""
        pass


class Admin(User):
    """The Admin Model."""

    __tablename__ = "admins"
    
    id: int = db.Column(db.Integer, primary_key=True)

    
class Moderator(User):
    """The Moderator Model."""

    __tablename__ = "moderators"
    
    id: int = db.Column(db.Integer, primary_key=True)
    bio: str = db.Column(db.Text, nullable=True)


class AuthorSchema(ma.Schema):
    """Show all the author information."""

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


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

moderator_schema = ModeratorSchema()
moderators_schema = ModeratorSchema(many=True)
