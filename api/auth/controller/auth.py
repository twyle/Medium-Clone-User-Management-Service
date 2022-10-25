# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for authentication and authorization."""
from flask import  jsonify, current_app
from ...admin import Admin, admin_schema
from ...author import Author, author_schema
from ...moderator import Moderator, moderator_schema
from ...extensions import db, url_serializer
from ...helpers.blueprint_helpers import validate_user_data
import json
import jwt
from ...models.models import user_schema
import datetime
from ..models import BlacklistToken
from ...suspend.models import Suspend
from itsdangerous import BadSignature, BadTimeSignature, SignatureExpired
    

def create_author(moderator_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    
    validate_user_data(moderator_data, profile_pic)
    
    Author.validate_name(moderator_data['First Name'])
    Author.validate_name(moderator_data['Last Name'])
    Author.validate_email(moderator_data['Email Address'])
    Author.validate_password(moderator_data['Password'])
        
    if Author.user_with_email_exists(moderator_data["Email Address"]):
        raise ValueError(f'The user with email address {moderator_data["Email Address"]} exists')
    
    author = Author(
        first_name=moderator_data["First Name"],
        last_name=moderator_data["Last Name"],
        email_address=moderator_data["Email Address"],
        password=moderator_data["Password"],
    )

    if 'Bio' in moderator_data.keys():
        Author.validate_bio(moderator_data["Bio"])
        author.bio = moderator_data["Bio"]
        
    if 'Nickname' in moderator_data.keys():
        Author.validate_screen_name(moderator_data['Nickname'])
        author.screen_name = moderator_data["Nickname"]
        
    db.session.add(author)
    db.session.commit()

    return author_schema.dumps(author), 201


def handle_create_author(moderator_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    try:
        author = create_author(moderator_data, profile_pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return author
    
def create_admin(admin_data: dict, profile_pic):
    """Handle the post request to create a new Admin."""
    
    validate_user_data(admin_data, profile_pic)
    
    Admin.validate_name(admin_data['First Name'])
    Admin.validate_name(admin_data['Last Name'])
    Admin.validate_email(admin_data['Email Address'])
    Admin.validate_password(admin_data['Password'])
        
    if Admin.user_with_email_exists(admin_data["Email Address"]):
        raise ValueError(f'The user with email address {admin_data["Email Address"]} exists')
    
    admin = Admin(
        first_name=admin_data["First Name"],
        last_name=admin_data["Last Name"],
        email_address=admin_data["Email Address"],
        password=admin_data["Password"],
    )

        
    if 'Nickname' in admin_data.keys():
        Admin.validate_screen_name(admin_data['Nickname'])
        admin.screen_name = admin_data["Nickname"]
        
    db.session.add(admin)
    db.session.commit()

    return admin_schema.dumps(admin), 201
    
def handle_create_admin(admin_data: dict, profile_pic):
    """Handle the post request to create a new Moderator."""
    try:
        admin = create_admin(admin_data, profile_pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return admin
    
    
def create_moderator(moderator_data: dict, profile_pic):
    """Handle the post request to create a new Moderator."""
    
    validate_user_data(moderator_data, profile_pic)
    
    Moderator.validate_name(moderator_data['First Name'])
    Moderator.validate_name(moderator_data['Last Name'])
    Moderator.validate_email(moderator_data['Email Address'])
    Moderator.validate_password(moderator_data['Password'])
        
    if Moderator.user_with_email_exists(moderator_data["Email Address"]):
        raise ValueError(f'The user with email address {moderator_data["Email Address"]} exists')
    
    moderator = Moderator(
        first_name=moderator_data["First Name"],
        last_name=moderator_data["Last Name"],
        email_address=moderator_data["Email Address"],
        password=moderator_data["Password"]
    )
        
    if 'Nickname' in moderator_data.keys():
        print('Got here!!1')
        Moderator.validate_screen_name(moderator_data['Nickname'])
        moderator.screen_name = moderator_data["Nickname"]
        
    if 'Bio' in moderator_data.keys():
        Moderator.validate_bio(moderator_data["Bio"])
        moderator.bio = moderator_data["Bio"]
        
    db.session.add(moderator)
    db.session.commit()

    return moderator_schema.dumps(moderator), 201


def create_access_token(user_id: int, role: str):
    """Create the access token"""
    print(datetime.datetime.now() + datetime.timedelta(seconds=30))
    access_token = jwt.encode(
        {'public_id': user_id, 'role': role}, 
        current_app.config['JWT_SECRET_KEY'], 
        'HS256', 
        {'exp': str(datetime.datetime.now() + datetime.timedelta(seconds=30))}
    )
    return access_token


def create_refresh_token(user_id: int, role: str):
    """Create the refresh token"""
    refresh_token = jwt.encode(
        {'public_id': user_id, 'role': role}, 
        current_app.config['JWT_SECRET_KEY'], 
        'HS256', 
        {'exp': str(datetime.datetime.now() + datetime.timedelta(seconds=60))}
    )
    return refresh_token

    
def handle_create_moderator(moderator_data: dict, profile_pic):
    """Handle the post request to create a new Moderator."""
    try:
        moderator = create_moderator(moderator_data, profile_pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return moderator
    
def log_in_user(user_id: str, role: str, user_data: dict):
    """Log in a registered user."""
    cls = None
    if not role:
        raise ValueError("The user role has to be provided!")
    if not isinstance(role, str):
        raise TypeError("The user role has to be a string")
    if not user_id:
        raise ValueError(f"The {role} id has to be provided!")
    if not isinstance(user_id, str):
        raise TypeError(f"The {role} id has to be a string")
    if role == 'author':
        cls = Author
    elif role == 'admin':
        cls = Admin
    else:
        cls = Moderator
    if not cls.user_with_id_exists(int(user_id)):
        raise ValueError(f"There is no {role} with id {user_id}")
    if role == 'author':
        if Suspend.is_suspended(int(user_id)):
            raise ValueError('You are currently suspended')
    if not user_data:
        raise ValueError(f"The {role} data cannot be empty.")

    if not isinstance(user_data, dict):
        raise TypeError("user_data must be a dict")

    if "email" not in user_data.keys():
        raise ValueError(f"The email is missing from the {role} data")

    if not user_data["email"]:
        raise ValueError(f"The email data for {role} is missing")

    if "password" not in user_data.keys():
        raise ValueError(f"The password is missing from the {role} data")

    if not user_data["password"]:
        raise ValueError("The password data is missing")

    if not cls.user_with_email_exists(user_data["email"]):
        raise ValueError(
            f'The {role} with email {user_data["email"]} does not exist!'
        )

    if not cls.validate_user(int(user_id), user_data["email"]):
        raise ValueError(
            f'The {role} with email {user_data["email"]} and id {user_id} does not exist!'
        )

    user = cls.query.filter_by(email_address=user_data["email"]).first()
    if user:
        if user.check_password(user_data["password"]):
            if not user.is_active:
                user_data = {
                    f"{role} profile": json.loads(user_schema.dumps(user)),
                    "access token": create_access_token(user.id, role),
                    "refresh token": create_refresh_token(user.id, role),
                }

                return user_data
            raise ValueError("This account has not been activate.")
        raise ValueError(f"The {role} password is invalid!")


def handle_log_in_user(user_id: str, role: str, user_data: dict) -> dict:
    """Handle a POST request to log in an admin."""
    try:
        data = log_in_user(user_id, role, user_data)
    except (
        ValueError,
        TypeError
    ) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return data, 200
    
    
def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return response_object, 200


def logout_user(user_id: str, role: str, token: str) -> dict:
    """Log out a user."""
    cls = None
    if not role:
        raise ValueError("The user role must be provided!")
    if not isinstance(role, str):
        raise TypeError("The user role must be a string")
    if not user_id:
        raise ValueError(f"The {role} id must be provided!")
    if not isinstance(user_id, str):
        raise TypeError(f"The {role} id must be a string")
    if role == 'author':
        cls = Author
    elif role == 'admin':
        cls = Admin
    else:
        cls = Moderator
    if not cls.user_with_id_exists(int(user_id)):
        raise ValueError(f"The {role} with id {user_id} does not exist1")
    return save_token(token)


def handle_logout_user(user_id: str, role: str, token: str) -> dict:
    """Log out a logged in user."""
    try:
        log_out_data = logout_user(user_id, role, token)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return log_out_data


def activate_account(email: str, cls):
    """Activate a user account."""
    user = cls.query.filter_by(email_address=email).first()
    user.is_active = True
    db.session.commit()
    return jsonify({"Email confirmed": email}), 200


def confirm_email(user_id: str, token: str, role: str) -> dict:
    """Confrim user account."""
    cls = None
    if not role:
        raise ValueError("The user role must be provided!")
    if not isinstance(role, str):
        raise TypeError("The user role must be a string")
    if role == 'author':
        cls = Author
    elif role == 'admin':
        cls = Admin
    else:
        cls = Moderator
    if not user_id:
        raise ValueError("The user id has to be provided!")
    if not isinstance(user_id, str):
        raise TypeError("The user id has to be a string!")
    if not token:
        raise ValueError("The token has to be provided!")
    if not isinstance(token, str):
        raise TypeError("The token has to be a string!")
    if not cls.user_with_id_exists(int(user_id)):
        raise ValueError(f"The {role} with id {user_id} does not exist1")
    email = url_serializer.loads(token, salt="somesalt", max_age=60)
    
    if not cls.validate_user(int(user_id), email):
        raise ValueError(
            f'The {role} with email {email} and id {user_id} does not exist!'
        )

    return activate_account(email)


def handle_email_confirm_request(user_id: str, token: str, role: str) -> dict:
    """Handle the GET request to /api/v1/mail/conrfim."""
    try:
        confirm_data = confirm_email(user_id, token, role)
    except SignatureExpired as e:
        return jsonify({"error": str(e)}), 400
    except BadTimeSignature as e:
        return jsonify({"error": str(e)}), 400
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return confirm_data