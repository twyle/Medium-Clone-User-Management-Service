# -*- coding: utf-8 -*-
"""This module contains all the author routes."""
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from .controller import (
    handle_list_authors,
    handle_delete_author,
    handle_get_author,
    handle_update_author,
    handle_get_author_followers,
    handle_get_author_follows,
    handle_follow_author,
    handle_unfollow_author,
    handle_subscribe_author,
    handle_unsubscribe_author,
    handle_get_author_subscribers,
    handle_get_author_subscribed_to
)

author = Blueprint("author", __name__)


@swag_from("./docs/get_author.yml", endpoint="author.get_author", methods=["GET"])
@author.route("/", methods=["GET"])
def get_author():
    """Get a an author by id."""
    return handle_get_author(request.args.get('id'))


@swag_from("./docs/update_author.yml", endpoint="author.update_author", methods=["PUT"])
@author.route("/", methods=["PUT"])
def update_author():
    """Update the author with given id."""
    return handle_update_author(request.args.get("id"), request.form, request.files)


@swag_from(
    "./docs/delete_author.yml", endpoint="author.delete_author", methods=["DELETE"]
)
@author.route("/", methods=["DELETE"])
def delete_author():
    """Delete the author with given id."""
    return handle_delete_author(request.args.get('id'))


@swag_from("./docs/follow_author.yml", endpoint="author.follow_author", methods=["GET"])
@author.route("/follow", methods=["GET"])
def follow_author():
    """Follow the author with given id."""
    return handle_follow_author(request.args.get('follower id'), request.args.get('follow id'))


@swag_from("./docs/unfollow_author.yml", endpoint="author.unfollow_author", methods=["GET"])
@author.route("/unfollow", methods=["GET"])
def unfollow_author():
    """Unfollow the author with given id."""
    return handle_unfollow_author(request.args.get('follower id'), request.args.get('follow id'))


@swag_from("./docs/author_followers.yml", endpoint="author.get_followers", methods=["GET"])
@author.route("/followers", methods=["GET"])
def get_followers():
    """Get author's followers."""
    return handle_get_author_followers(request.args.get('id'))


@swag_from("./docs/author_follows.yml", endpoint="author.get_follows", methods=["GET"])
@author.route("/follows", methods=["GET"])
def get_follows():
    """Get author follows."""
    return handle_get_author_follows(request.args.get('id'))


@swag_from(
    "./docs/get_all_authors.yml", endpoint="author.get_all_authors", methods=["GET"]
)
@author.route("/authors", methods=["GET"])
def get_all_authors():
    """List all authors."""
    return handle_list_authors()


@swag_from("./docs/subscribe.yml", endpoint="author.subscribe", methods=["GET"])
@author.route("/subscribe", methods=["GET"])
def subscribe():
    """Subscribe to the author with given id."""
    return handle_subscribe_author(request.args.get('subscriber id'), request.args.get('subscribe id'))


@swag_from("./docs/unsubscribe.yml", endpoint="author.unsubscribe", methods=["GET"])
@author.route("/unsubscribe", methods=["GET"])
def unsubscribe():
    """Unsubscribe from the author with given id."""
    return handle_unsubscribe_author(request.args.get('subscriber id'), request.args.get('subscribe id'))


@swag_from("./docs/author_subscribers.yml", endpoint="author.get_subscribers", methods=["GET"])
@author.route("/subscribers", methods=["GET"])
def get_subscribers():
    """Get author's subscribers."""
    return handle_get_author_subscribers(request.args.get('id'))


@swag_from("./docs/author_subscribed.yml", endpoint="author.get_subscribed_to", methods=["GET"])
@author.route("/subscribed_to", methods=["GET"])
def get_subscribed_to():
    """Get author subscribed_to."""
    return handle_get_author_subscribed_to(request.args.get('id'))

