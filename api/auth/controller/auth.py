# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for authentication and authorization."""
from flask import  jsonify

from ..models import Author, author_schema
from ...extensions import db



def create_author(author_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    if not author_data:
        raise ValueError("The authors data must be provided!")
    if not isinstance(author_data, dict):
        raise ValueError("The author data must be a dictionary!")
    valid_keys = [
        "First Name",
        "Last Name",
        "Email Address",
        "Bio",
        "Nickname",
        "Password",
    ]
    for key in author_data.keys():
        if key not in valid_keys:
            raise ValueError(f"The only valid keys are {valid_keys}")
    if "First Name" not in author_data.keys():
        raise ValueError("The First Name must be provided")
    if "Last Name" not in author_data.keys():
        raise ValueError("The Last Name must be provided")
    if not author_data["First Name"]:
        raise ValueError("The First Name must be provided")
    if not author_data["Last Name"]:
        raise ValueError("The Last Name must be provided")
    if "Password" not in author_data.keys():
        raise ValueError("The password must be provided!")
    if not author_data["Password"]:
        raise ValueError("The password must be provided!")
    if "Email Address" not in author_data.keys():
        raise ValueError("The Emai address must be provide!")
    if not author_data["Email Address"]:
        raise ValueError("The Email address must be provide!")
    Author.validate_name(author_data['First Name'])
    Author.validate_name(author_data['Last Name'])
    Author.validate_email(author_data['Email Address'])
    Author.validate_password(author_data['Password'])
        
    if Author.user_with_email_exists(author_data["Email Address"]):
        raise ValueError(f'The user with email address {author_data["Email Address"]} exists')

    author = Author(
        first_name=author_data["First Name"],
        last_name=author_data["Last Name"],
        email_address=author_data["Email Address"],
        password=author_data["Password"],
    )

    if 'Bio' in author_data.keys():
        Author.validate_bio(author_data["Bio"])
        author.bio = author_data["Bio"]
        
    if 'Nickname' in author_data.keys():
        Author.validate_screen_name(author_data['Nickname'])
        author.screen_name = author_data["Nickname"]
        
    # db.session.add(author)
    # db.session.commit()

    return author_schema.dumps(author), 201


def handle_create_author(author_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    try:
        author = create_author(author_data, profile_pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return author
