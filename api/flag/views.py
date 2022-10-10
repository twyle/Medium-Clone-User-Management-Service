# -*- coding: utf-8 -*-
"""This module contains all the routes for flagging articles and flags by moderators."""
from flasgger import swag_from
from flask import Blueprint, jsonify

flag = Blueprint("flag", __name__)


@swag_from("./docs/flag_author.yml", endpoint="flag.flag_author", methods=["POST"])
@flag.route("/author", methods=["POST"])
def flag_author():
    """Flag Author with given id."""
    return jsonify({"flag": "author"}), 200

