# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for the admin."""
from ..model import Admin, admin_schema, admins_schema
from flask import jsonify
from ...extensions import db


def get_admin(admin_id: str) -> dict:
    """Get the user with the given id."""
    if not admin_id:
        raise ValueError("The admin_id has to be provided.")
    if not isinstance(admin_id, str):
        raise TypeError("The admin_id has to be a string.")
    if not Admin.user_with_id_exists(int(admin_id)):
        raise ValueError(f"The user with id {admin_id} does not exist.")

    return admin_schema.dump(Admin.get_user(int(admin_id))), 200   

    
def handle_get_admin(admin_id: str):
    """Get a single author."""
    try:
        author = get_admin(admin_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return author
    

def handle_list_admins():
    """List all admins."""
    return admins_schema.dump(Admin.all_users()), 200


def delete_admin(admin_id: str):
    """Delete an author."""
    if not admin_id:
        raise ValueError('The admin id has to be provided')
    if not isinstance(admin_id, str):
        raise TypeError('The author id has to be a string')
    if not Admin.user_with_id_exists(int(admin_id)):
        raise ValueError(f'Their is no author with id {admin_id}')
    return admin_schema.dump(Admin.delete_user(int(admin_id))), 200


def handle_delete_admin(admin_id: str):
    """List all authors."""
    try:
        deleted_admin = delete_admin(admin_id)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)})
    else:
        return deleted_admin
    

def update_admin(admin_id: str, admin_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    if not admin_id:
        raise ValueError("The admin_id has to be provided.")
    if not isinstance(admin_id, str):
        raise ValueError("The admin_id has to be a string.")
    if not Admin.user_with_id_exists(int(admin_id)):
        raise ValueError(f"The user with id {admin_id} does not exist.")
    if not admin_data:
        raise ValueError("The user data cannot be empty.")
    if not isinstance(admin_data, dict):
        raise TypeError("user_data must be a dict")
    valid_keys = [
        "First Name",
        "Last Name",
        "Email Address",
        "Nickname"
    ]
    for key in admin_data.keys():
        if key not in valid_keys:
            print(key)
            raise ValueError(f"The only valid keys are {valid_keys}")
    
    admin = Admin.get_user(int(admin_id))
    
    if "First Name" in admin_data.keys():
        Admin.validate_name(admin_data['First Name'])
        admin.first_name = admin_data['First Name']
    if "Last Name" in admin_data.keys():
        Admin.validate_name(admin_data['Last Name'])
        admin.last_name = admin_data['Last Name']
    if "Email Address" in admin_data.keys():
        Admin.validate_email(admin_data['Email Address'])
        if Admin.user_with_email_exists(admin_data["Email Address"]):
            raise ValueError(f'The user with email address {admin_data["Email Address"]} exists')
        admin.email_address = admin_data['Email Address']
    if "Nickname" in admin_data.keys():
        Admin.validate_screen_name(admin_data['Nickname'])
        admin.screen_name = admin_data['Nickname']
        
    db.session.add(admin)
    db.session.commit()

    return admin_schema.dumps(admin), 201


def handle_update_admin(admin_id: str, admin_data: dict, profile_pic):
    """Handle the post request to create a new author."""
    try:
        admin = update_admin(admin_id, admin_data, profile_pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return admin