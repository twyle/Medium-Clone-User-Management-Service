# -*- coding: utf-8 -*-
"""This module contains all helper methos used by the report package."""
from asyncio import exceptions
from functools import wraps
from flask import make_response, request, jsonify, current_app
import jwt
from ...author.model import Author
from ...auth.models import BlacklistToken

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            # decode the token to obtain user public_id
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            if data['role'] != 'author':
                return make_response(jsonify({'error': 'Only authors can report other authors!'}), 401)
            current_author = Author.query.filter_by(id=data['public_id']).first()
            if BlacklistToken.check_blacklist(token):
                return make_response(jsonify({"message": "Invalid token!"}), 401)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 401)
         # Return the user information attached to the token
        if current_author:
            return f(*args, **kwargs) 
        return make_response(jsonify({"message": "Invalid token!"}), 401)
    return decorator
