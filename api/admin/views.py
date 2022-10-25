# -*- coding: utf-8 -*-
"""This module contains all the admin routes."""
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from .controller import (
    handle_get_admin,
    handle_delete_admin,
    handle_list_admins,
    handle_update_admin
)

admin = Blueprint("admin", __name__)


@swag_from("./docs/get_admin.yml", endpoint="admin.get_admin", methods=["GET"])
@admin.route("/", methods=["GET"])
def get_admin():
    """Get a an admin by id."""
    return handle_get_admin(request.args.get('id'))


@swag_from("./docs/update_admin.yml", endpoint="admin.update_admin", methods=["PUT"])
@admin.route("/", methods=["PUT"])
def update_admin():
    """Update the admin with given id."""
    return handle_update_admin(request.args.get("id"), request.form, request.files)


@swag_from("./docs/delete_admin.yml", endpoint="admin.delete_admin", methods=["DELETE"])
@admin.route("/", methods=["DELETE"])
def delete_admin():
    """Delete the admin with given id."""
    return handle_delete_admin(request.args.get('id'))


@swag_from(
    "./docs/get_all_admins.yml", endpoint="admin.get_all_admins", methods=["GET"]
)
@admin.route("/admins", methods=["GET"])
def get_all_admins():
    """List all admins."""
    return handle_list_admins()
