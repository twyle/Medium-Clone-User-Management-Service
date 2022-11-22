# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic suspending authors and articles."""
from ...author.model import Author
from ...admin.model import Admin
from ..models import Suspend, suspend_schema, suspends_schema
from ...extensions import db
from flask import jsonify


def suspend_author(admin_id: str, author_id: str, reason: str):
    if not admin_id:
        raise ValueError('The admin id must be provided')
    if not author_id:
        raise ValueError('The author id must be provided')
    if not reason:
        raise ValueError('The reason must be provided')
    if not isinstance(reason, dict):
        raise TypeError('The reason must be a dictionary!')
    if not reason['reason']:
        raise ValueError('The reason must be provided')
    if not isinstance(reason['reason'], str):
        raise TypeError('The reason must be a string')
    if not isinstance(admin_id, str):
        raise TypeError('The moderator id must be a string')
    if not isinstance(author_id, str):
        raise TypeError('The author id must be a string')
    if not Admin.user_with_id_exists(int(admin_id)):
        raise ValueError(f'The admin with id {admin_id} does not exist!')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'The author with id {author_id} does not exist!')
    
    suspend = Suspend(admin_id=admin_id, author_id=author_id, reason=reason['reason'])
    db.session.add(suspend)
    db.session.commit()
    
    return suspend_schema.dump(suspend), 201

def handle_suspend_author(admin_id: str, author_id: str, reason: str):
    """Suspend an author."""
    try:
        suspend = suspend_author(admin_id, author_id, reason)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return suspend

def get_suspended(author_id: str):
    """Get suspended authors"""
    if author_id:
        if not isinstance(author_id, str):
            raise TypeError('The author id has to be a string')
        if not Author.user_with_id_exists(int(author_id)):
            raise ValueError(f'There is not author with id {author_id}')
    if author_id:
        suspended = Suspend.query.filter_by(author_id=int(author_id)).all()
        return suspends_schema.dump(flags), 200
    flags = Suspend.query.all()
    return suspends_schema.dump(flags), 200
        
    
def handle_get_suspended(author_id: str):
    """Get suspended"""
    try:
        suspended = get_suspended(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)})
    else:
        return suspended