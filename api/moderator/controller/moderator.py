# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for moderating authors and content."""
# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for the admin."""
from ..model import Moderator, moderator_schema, moderators_schema
from flask import jsonify
from ...extensions import db


def get_moderator(moderator_id: str) -> dict:
    """Get the user with the given id."""
    if not moderator_id:
        raise ValueError("The moderator_id has to be provided.")
    if not isinstance(moderator_id, str):
        raise TypeError("The moderator_id has to be a string.")
    if not Moderator.user_with_id_exists(int(moderator_id)):
        raise ValueError(f"The user with id {moderator_id} does not exist.")

    return moderator_schema.dump(Moderator.get_user(int(moderator_id))), 200   

    
def handle_get_moderator(moderator_id: str):
    """Get a single author."""
    try:
        moderator = get_moderator(moderator_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return moderator
    

def handle_list_moderators():
    """List all admins."""
    return moderators_schema.dump(Moderator.all_users()), 200


def delete_moderator(moderator_id: str):
    """Delete an author."""
    if not moderator_id:
        raise ValueError('The admin id has to be provided')
    if not isinstance(moderator_id, str):
        raise TypeError('The author id has to be a string')
    if not Moderator.user_with_id_exists(int(moderator_id)):
        raise ValueError(f'Their is no author with id {moderator_id}')
    return moderator_schema.dump(Moderator.delete_user(int(moderator_id))), 200


def handle_delete_moderator(moderator_id: str):
    """List all authors."""
    try:
        deleted_moderator = delete_moderator(moderator_id)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)})
    else:
        return deleted_moderator
    

def update_moderator(moderator_id: str, moderator_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    if not moderator_id:
        raise ValueError("The moderator_id has to be provided.")
    if not isinstance(moderator_id, str):
        raise ValueError("The moderator_id has to be a string.")
    if not Moderator.user_with_id_exists(int(moderator_id)):
        raise ValueError(f"The user with id {moderator_id} does not exist.")
    if not moderator_data:
        raise ValueError("The user data cannot be empty.")
    if not isinstance(moderator_data, dict):
        raise TypeError("user_data must be a dict")
    valid_keys = [
        "First Name",
        "Last Name",
        "Email Address",
        "Nickname",
        "Bio"
    ]
    for key in moderator_data.keys():
        if key not in valid_keys:
            print(key)
            raise ValueError(f"The only valid keys are {valid_keys}")
    
    moderator = Moderator.get_user(int(moderator_id))
    
    if "First Name" in moderator_data.keys():
        Moderator.validate_name(moderator_data['First Name'])
        moderator.first_name = moderator_data['First Name']
    if "Last Name" in moderator_data.keys():
        Moderator.validate_name(moderator_data['Last Name'])
        moderator.last_name = moderator_data['Last Name']
    if "Email Address" in moderator_data.keys():
        Moderator.validate_email(moderator_data['Email Address'])
        if Moderator.user_with_email_exists(moderator_data["Email Address"]):
            raise ValueError(f'The user with email address {moderator_data["Email Address"]} exists')
        moderator.email_address = moderator_data['Email Address']
    if "Nickname" in moderator_data.keys():
        Moderator.validate_screen_name(moderator_data['Nickname'])
        moderator.screen_name = moderator_data['Nickname']
    if "Bio" in moderator_data.keys():
        Moderator.validate_bio(moderator_data['Bio'])
        moderator.bio = moderator_data['Bio']
        
    db.session.add(moderator)
    db.session.commit()

    return moderator_schema.dumps(moderator), 201


def handle_update_moderator(moderator_id: str, moderator_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    try:
        moderator = update_moderator(moderator_id, moderator_data, profile_pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return moderator