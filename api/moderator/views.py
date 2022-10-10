# -*- coding: utf-8 -*-
"""This module contains all the content and moderator moderation routes."""
from flasgger import swag_from
from flask import Blueprint, jsonify

moderator = Blueprint("moderator", __name__)


@swag_from(
    "./docs/get_moderator.yml", endpoint="moderator.get_moderator", methods=["GET"]
)
@moderator.route("/", methods=["GET"])
def get_moderator():
    """Get a an moderator by id."""
    return jsonify({"moderator": "get"}), 200


@swag_from(
    "./docs/update_moderator.yml",
    endpoint="moderator.update_moderator",
    methods=["PUT"],
)
@moderator.route("/", methods=["PUT"])
def update_moderator():
    """Update the moderator with given id."""
    return jsonify({"moderator": "update"}), 200


@swag_from(
    "./docs/delete_moderator.yml",
    endpoint="moderator.delete_moderator",
    methods=["DELETE"],
)
@moderator.route("/", methods=["DELETE"])
def delete_moderator():
    """Delete the moderator with given id."""
    return jsonify({"moderator": "delete"}), 200


@swag_from(
    "./docs/get_all_moderators.yml",
    endpoint="moderator.get_all_moderators",
    methods=["GET"],
)
@moderator.route("/moderators", methods=["GET"])
def get_all_moderators():
    """List all moderators."""
    return jsonify({"moderator": "all"}), 200
