# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for authentication and authorization."""
from flask import  jsonify
from ...admin import Admin, admin_schema
from ...author import Author, author_schema
from ...moderator import Moderator, moderator_schema
from ...extensions import db


def validate_user_data(user_data: dict, profile_pic):
    """Validate user data."""
    if not user_data:
        raise ValueError("The authors data must be provided!")
    if not isinstance(user_data, dict):
        raise ValueError("The author data must be a dictionary!")
    valid_keys = [
        "First Name",
        "Last Name",
        "Email Address",
        "Nickname",
        "Password",
    ]
    for key in user_data.keys():
        if key not in valid_keys:
            raise ValueError(f"The only valid keys are {valid_keys}")
    if "First Name" not in user_data.keys():
        raise ValueError("The First Name must be provided")
    if "Last Name" not in user_data.keys():
        raise ValueError("The Last Name must be provided")
    if not user_data["First Name"]:
        raise ValueError("The First Name must be provided")
    if not user_data["Last Name"]:
        raise ValueError("The Last Name must be provided")
    if "Password" not in user_data.keys():
        raise ValueError("The password must be provided!")
    if not user_data["Password"]:
        raise ValueError("The password must be provided!")
    if "Email Address" not in user_data.keys():
        raise ValueError("The Emai address must be provide!")
    if not user_data["Email Address"]:
        raise ValueError("The Email address must be provide!")
    

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
        
    # db.session.add(Admin)
    # db.session.commit()

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
        
    # db.session.add(moderator)
    # db.session.commit()

    return moderator_schema.dumps(moderator), 201

    
def handle_create_moderator(moderator_data: dict, profile_pic):
    """Handle the post request to create a new Moderator."""
    try:
        moderator = create_moderator(moderator_data, profile_pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return moderator
