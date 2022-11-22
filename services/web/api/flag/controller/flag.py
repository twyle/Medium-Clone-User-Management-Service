# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for flagging authors and accounts."""
from ...author.model import Author
from ...moderator.model import Moderator
from ..models import Flag, flag_schema, flags_schema
from ...extensions import db
from flask import jsonify


def flag_author(moderator_id: str, author_id: str, reason: str):
    if not moderator_id:
        raise ValueError('The moderaotr id must be provided')
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
    if not isinstance(moderator_id, str):
        raise TypeError('The moderator id must be a string')
    if not isinstance(author_id, str):
        raise TypeError('The author id must be a string')
    if not Moderator.user_with_id_exists(int(moderator_id)):
        raise ValueError(f'The moderator with id {moderator_id} does not exist!')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'The author with id {author_id} does not exist!')
    
    flag = Flag(moderator_id=moderator_id, author_id=author_id, reason=reason['reason'])
    db.session.add(flag)
    db.session.commit()
    
    return flag_schema.dump(flag), 201

def handle_flag_author(moderator_id: str, author_id: str, reason: str):
    """Flag an author."""
    try:
        flag = flag_author(moderator_id, author_id, reason)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return flag

def get_flags(author_id: str):
    """Get flags"""
    if author_id:
        if not isinstance(author_id, str):
            raise TypeError('The author id has to be a string')
        if not Author.user_with_id_exists(int(author_id)):
            raise ValueError(f'There is not author with id {author_id}')
    if author_id:
        flags = Flag.query.filter_by(author_id=int(author_id)).all()
        return flags_schema.dump(flags), 200
    flags = Flag.query.all()
    return flags_schema.dump(flags), 200
        
    
def handle_get_flags(author_id: str):
    """Get reports"""
    try:
        flags = get_flags(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)})
    else:
        return flags
    