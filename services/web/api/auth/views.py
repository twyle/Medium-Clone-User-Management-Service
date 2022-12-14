# -*- coding: utf-8 -*-
"""This module contains all the authentication, authorization and registration routes."""
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from .controller import (
    handle_create_admin,
    handle_create_author,
    handle_create_moderator,
    handle_log_in_user, 
    handle_logout_user,
    handle_email_confirm_request,
    handle_get,
    handle_post
)

auth = Blueprint("auth", __name__)


@swag_from(
    "./docs/register_admin.yml", endpoint="auth.register_admin", methods=["POST"]
)
@auth.route("/register/admin", methods=["POST"])
def register_admin():
    """Register an admin."""
    return handle_create_admin(request.form, request.files)


@swag_from(
    "./docs/register_author.yml", endpoint="auth.register_author", methods=["POST"]
)
@auth.route("/register/author", methods=["POST"])
def register_author():
    """Register an author."""
    return handle_create_author(request.form, request.files)


@swag_from(
    "./docs/register_moderator.yml",
    endpoint="auth.register_moderator",
    methods=["POST"],
)
@auth.route("/register/moderator", methods=["POST"])
def register_moderator():
    """Register a moderator."""
    return handle_create_moderator(request.form, request.files)


@auth.route("/reset_password", methods=["POST", "GET"])
@swag_from(
    "./docs/password_reset.yml", endpoint="auth.reset_password", methods=["POST", "GET"]
)
def reset_password():
    """Reset admin password."""
    if request.method == "GET":
        return handle_get(request.args.get('id'), request.args.get('token'), request.args.get('role'))
    elif request.method == "POST":
        return handle_post(request.args.get('id'), request.args.get('token'), request.args.get('role'), request.json)


@auth.route("/login", methods=["POST"])
@swag_from("./docs/login_user.yml", endpoint="auth.login", methods=["POST"])
def login():
    return handle_log_in_user(request.args.get("id"), request.args.get("role"), request.json) 


@auth.route("/logout", methods=["POST"])
@swag_from("./docs/logout_user.yml", endpoint="auth.logout", methods=["POST"])
def logout():
    token = request.headers.get('Authorization').split()[1]
    return handle_logout_user(request.args.get("id"), request.args.get("role"), token)


@auth.route("/confirm_email", methods=["GET"])
@swag_from("./docs/confirm.yml", endpoint="auth.confirm_email", methods=["GET"])
def confirm_email():
    """Handle email confirmation."""
    return handle_email_confirm_request(
        request.args.get("id"), request.args.get("token"), request.args.get("role") 
    )
