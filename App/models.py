
from App import app, login_manager, db
from flask_login import UserMixin, LoginManager
import datetime
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy.orm import relationship
from sqlalchemy.databases import mysql
from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(id_):
    return User.query.filter_by(id_=id_).first()


class User(UserMixin, db.Model):
    id_=db.Column(db.String(30),primary_key=True)#goo
    username=db.Column(db.String(20), primary_key=True)#goo
    email=db.Column(db.String(50), unique=True)#goo
    joinedOnDate=db.Column(db.DateTime, default=datetime.datetime.now)#added    
    primaryPostCount=db.Column(db.Integer, default=0)
    secondaryPostCount=db.Column(db.Integer, default=0)

    profile_pic=db.Column(db.String(200))#goo
    fullname=db.Column(db.String(50), nullable=True)#goo
#     dob=db.Column(db.DateTime, default=datetime.datetime.now)
#     gender=db.Column(db.String(2), nullable=True)
#     country=db.Column(db.String(20))

#     def avatar(self, size):
#         digest = md5(self.email.lower().encode('utf-8')).hexdigest()
#         return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    @hybrid_property
    def total_points(self):
        PRIMARY_POST_POINTS=2
        SECONDARY_POST_POINTS=1
        
        primaryPostCount=0
        secondaryPostCount=0
        
        if self.primaryPostCount: primaryPostCount=self.primaryPostCount
        if self.secondaryPostCount: secondaryPostCount=self.secondaryPostCount
        
        return PRIMARY_POST_POINTS*primaryPostCount+SECONDARY_POST_POINTS*secondaryPostCount
    
    @hybrid_property
    def badge(self):
        points=self.total_points
        if points<5:
            BADGE="Contributor"
        elif points<10:
            BADGE="Regular Contributor"
        elif points<50:
            BADGE="Great Contributor"
        else:
            BADGE="Ace Contributor"
        return BADGE

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'username'   : self.username,
           'email'      : self.email,
           'totalPoints': self.total_points,
           'badge'      : self.badge
        }

    def get_id(self):
        return self.id_

    def __repr__(self):
        return "<User {}>".format(self.username)


class Topic(db.Model):
    topicID=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(35), nullable=False)
    secondaryPostCount=db.Column(db.Integer, default=0) 
    posts = relationship("Post")

    @property
    def serialize_with_one_post(self):
       """Return object data in easily serializable format"""
       return{**self.serialize,**self.posts[0].serialize}

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return{
           'topicID': self.topicID, 
           'title': self.title, 
           'secondaryPostCount': self.secondaryPostCount
        }
    
    def __repr__(self):
        return "<Topic {}>".format(self.title)



class Post(db.Model):
    postID=db.Column(db.Integer, primary_key=True)
    topicID=db.Column(db.Integer, db.ForeignKey(Topic.topicID))
    postingUser=db.Column(db.String(20), db.ForeignKey(User.username))
    description=db.Column(db.String(800), nullable=False)
    upvoteCount=db.Column(db.Integer, default=0)
    createdTime=db.Column(db.DateTime, default=datetime.datetime.now)
    postType=db.Column(db.String(10), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'postID'   : self.postID,
           'topicID'      : self.topicID,
           'postingUser': self.postingUser,
           'description': self.description,
           'upvoteCount': self.upvoteCount,
           'createdTime': self.createdTime,
           'timeAgo': self.time_ago,
        }

    @property
    def time_ago(self):
        import timeago, datetime
        now = datetime.datetime.now()
        if self.createdTime:
            return timeago.format(self.createdTime,now) 

    def __repr__(self):
        return "<Post {}>".format(self.description)



class Reaction(db.Model):
    postID=db.Column(db.Integer, db.ForeignKey(Post.postID),primary_key=True)
    reactingUser=db.Column(db.String(20), db.ForeignKey(User.username), primary_key=True)
    reactionType=db.Column(db.String(10), default="upvote")

db.create_all()
