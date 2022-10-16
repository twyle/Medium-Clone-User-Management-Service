# -*- coding: utf-8 -*-
"""This module contains all the routes used to suspend articles and suspends."""
from flasgger import swag_from
from flask import Blueprint, request
from .controller import handle_suspend_author, handle_get_suspended

suspend = Blueprint("suspend", __name__)


@swag_from(
    "./docs/suspend_author.yml", endpoint="suspend.suspend_author", methods=["POST"]
)
@suspend.route("/author", methods=["POST"])
def suspend_author():
    """Suspend Author with given id."""
    return handle_suspend_author(request.args.get('admin id'), request.args.get('author id'), request.json)


@swag_from(
    "./docs/get_suspended.yml", endpoint="suspend.get_suspended", methods=["GET"]
)
@suspend.route("/suspended", methods=["GET"])
def get_suspended():
    """Get suspended authors."""
    return handle_get_suspended(request.args.get('author id'))