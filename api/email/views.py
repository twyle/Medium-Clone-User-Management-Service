# -*- coding: utf-8 -*-
"""This module contains all the email sending routes."""
from flasgger import swag_from
from flask import Blueprint, request
from .controller import handle_send_confirm_email, handle_send_reset_password_email

mail = Blueprint("mail", __name__)


@mail.route("/send_confirm_email", methods=["POST"])
@swag_from("./docs/send.yml", endpoint="mail.send_confirm_mail", methods=["POST"])
def send_confirm_mail():
    """Send the confirm account email."""
    return handle_send_confirm_email(request.args.get("id"), request.args.get("id"), request.json)


@mail.route("/send_reset_password_email", methods=["POST"])
@swag_from(
    "./docs/password_reset.yml",
    endpoint="mail.send_reset_password_mail",
    methods=["POST"],
)
def send_reset_password_mail():
    """Send the reset password mail."""
    return handle_send_reset_password_email(request.args.get("id"), request.args.get("id"), request.json)
