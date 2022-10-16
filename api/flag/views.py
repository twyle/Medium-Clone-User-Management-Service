# -*- coding: utf-8 -*-
"""This module contains all the routes for flagging articles and flags by moderators."""
from flasgger import swag_from
from flask import Blueprint, request
from .controller import handle_flag_author, handle_get_flags

flag = Blueprint("flag", __name__)


@swag_from("./docs/flag_author.yml", endpoint="flag.flag_author", methods=["POST"])
@flag.route("/author", methods=["POST"])
def flag_author():
    """Flag Author with given id."""
    return handle_flag_author(request.args.get('moderator id'), request.args.get('author id'), request.json)


@swag_from(
    "./docs/get_flagged.yml", endpoint="flag.get_flagged", methods=["GET"]
)
@flag.route("/flagged", methods=["GET"])
def get_flagged():
    """Get flagged authors."""
    return handle_get_flags(request.args.get('author id'))