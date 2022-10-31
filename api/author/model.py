# -*- coding: utf-8 -*-
"""This module contains the Author user model."""
from sqlalchemy.dialects.postgresql import ARRAY
from ..models import User
from ..extensions import db, ma
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'follows'
    
    follower_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
    primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
    primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

class Subscribe(db.Model):
    __tablename__ = 'subscribers'
    
    subscriber_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
    primary_key=True)
    subscribed_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
    primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

class Author(User):
    """The Author Model."""

    __tablename__ = "authors"
    
    id: int = db.Column(db.Integer, primary_key=True)
    bio: str = db.Column(db.Text, nullable=True)
    interests: list = db.Column(ARRAY(db.String(100)), nullable=True)
    
    followed = db.relationship('Follow',
        foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')    
    
    followers = db.relationship('Follow',
        foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    
    subscribed = db.relationship('Subscribe',
        foreign_keys=[Subscribe.subscriber_id],
        backref=db.backref('subscriber', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    
    subscribers = db.relationship('Subscribe',
        foreign_keys=[Subscribe.subscribed_id],
        backref=db.backref('subscribed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'Author(first_name="{self.first_name}", email_address="{self.email_address}")'
    
    @staticmethod
    def validate_bio(bio: str):
        """Validate the given name."""
        pass
    
    @staticmethod
    def follow(follow_id, to_be_followed_id):
        follow_author = Author.query.filter_by(id=follow_id).first()
        to_be_followed_author = Author.query.filter_by(id=to_be_followed_id).first()
        if not follow_author.is_following(follow_author, to_be_followed_author):
            f = Follow(follower=follow_author, followed=to_be_followed_author)
            db.session.add(f)
            db.session.commit()
            return {'success': f'{follow_author.email_address} is following {to_be_followed_author.email_address}'}
        return {'success': f'{follow_author.email_address} is already following {to_be_followed_author.email_address}'}   
    
    
    @staticmethod
    def subscribe(subscriber_id, to_subscribe_to_id):
        subscribe_author = Author.query.filter_by(id=subscriber_id).first()
        to_subscribe_to_author = Author.query.filter_by(id=to_subscribe_to_id).first()
        if not subscribe_author.is_subscribed(subscribe_author, to_subscribe_to_author):
            s = Subscribe(subscriber=subscribe_author, subscribed=to_subscribe_to_author)
            db.session.add(s)
            db.session.commit()
            return {'success': f'{subscribe_author.email_address} is subscribed to {to_subscribe_to_author.email_address}'}
        return {'success': f'{subscribe_author.email_address} is already subscribed {to_subscribe_to_author.email_address}'}   
    
    @staticmethod        
    def unfollow(follow_id, unfollow_id):
        author = Author.query.filter_by(id=follow_id).first()
        unfollow_author = Author.query.filter_by(id=unfollow_id).first()
        f = author.followed.filter_by(followed_id=unfollow_author.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()
            return {'success': f'{author.email_address} is unfollowed {unfollow_author.email_address}'}
        return {'success': f'{author.email_address} is not following {unfollow_author.email_address}'}
    
    
    @staticmethod        
    def unsubscribe(subscriber_id, unsubscribe_to_id):
        author = Author.query.filter_by(id=subscriber_id).first()
        unsubscribe_to_author = Author.query.filter_by(id=unsubscribe_to_id).first()
        s = author.subscribed.filter_by(subscribed_id=unsubscribe_to_author.id).first()
        if s:
            db.session.delete(s)
            db.session.commit()
            return {'success': f'{author.email_address} has unsubscribed from {unsubscribe_to_author.email_address}'}
        return {'success': f'{author.email_address} is not subscribed to {unsubscribe_to_author.email_address}'}   
    
    
    def is_following(self, author, to_be_followed_author):
        return author.followed.filter_by(
            followed_id=to_be_followed_author.id).first() is not None
        
        
    def is_subscribed(self, author, to_subscribe_to_author):
        return author.subscribed.filter_by(
            subscribed_id=to_subscribe_to_author.id).first() is not None
        
    def is_followed_by(self, author):
        return self.followers.filter_by(
            follower_id=author.id).first() is not None
    
    @staticmethod
    def get_followers(author_id: int):
        """Get the authors followers."""
        followers = [follow.follower for follow in Author.query.filter_by(id=author_id).first().followers.all()]
        return followers
    
    @staticmethod
    def get_subscriberss(author_id: int):
        """Get the authors subscribers."""
        subscribers = [subscribe.subscriber for subscribe in Author.query.filter_by(id=author_id).first().subscribers.all()]
        return subscribers
    
    @staticmethod
    def get_follows(author_id: int):
        """Get the authors follows."""
        followed = [followed.followed for followed in Author.query.filter_by(id=author_id).first().followed.all()]
        return followed
    
    @staticmethod
    def get_subscribed_to(author_id: int):
        """Get the authors subscribed to."""
        subscribed_to = [subscribed.subscribed for subscribed in Author.query.filter_by(id=author_id).first().subscribed.all()]
        return subscribed_to
    

class AuthorSchema(ma.Schema):
    """Show all the author information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "first_name",
            "last_name",
            "screen_name",
            "email_address",
            "date_registered",
            "profile_picture",
            "bio",
        )

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)