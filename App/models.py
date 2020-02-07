
from App import app, login_manager, db
from flask_login import UserMixin, LoginManager
import datetime
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(id_):
    return User.query.filter_by(id_=id_).first()


class User(UserMixin, db.Model):
    id_=db.Column(db.Integer,primary_key=True)#goo
    username=db.Column(db.String(20), primary_key=True)#goo
    #password_hash=db.Column(db.String(128))
    email=db.Column(db.String(50), unique=True)#goo
    profile_pic=db.Column(db.String(100))#goo
    fullname=db.Column(db.String(50), nullable=True)#goo
    dob=db.Column(db.DateTime, default=datetime.datetime.now)
    #age=db.Column(db.Integer, nullable=True)
    gender=db.Column(db.String(2), nullable=True)
    country=db.Column(db.String(20))
    aboutMe=db.Column(db.String(100))#added
    joinedOnDate=db.Column(db.DateTime, default=datetime.datetime.now)#added
    lastSeen=db.Column(db.DateTime, default=datetime.datetime.now)#added
    
    primaryPostCount=db.Column(db.Integer, default=0)
    secondaryPostCount=db.Column(db.Integer, default=0)
    totalPoints=db.Column(db.Integer, default=0)

    @classmethod
    def calculate_points(cls,primaryPostCount,secondaryPostCount):
        PRIMARY_POST_POINTS=2
        SECONDARY_POST_POINTS=1
        return PRIMARY_POST_POINTS*int(primaryPostCount)+SECONDARY_POST_POINTS*int(secondaryPostCount)
    
    @classmethod
    def calculate_badge(cls,points):
        if int(points)<5:
            BADGE="contributer"
        elif int(points)<10:
            BADGE="regular contributer"
        elif int(points)<50:
            BADGE="great contributer"
        else:
            BADGE="ace contributer"
        return BADGE

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_id(self):
        return self.id_
    
    def __repr__(self):
        return "<User {}>".format(self.username)


class Topic(db.Model):
    topicID=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50), nullable=False)
    secondaryPostCount=db.Column(db.Integer, default=0) 
    posts = relationship("Post")

    def __repr__(self):
        return "<Topic {}>".format(self.title)



class Post(db.Model):
    postID=db.Column(db.Integer, primary_key=True)
    topicID=db.Column(db.Integer, db.ForeignKey(Topic.topicID))
    postingUser=db.Column(db.String(20), db.ForeignKey(User.username))
    description=db.Column(db.String(80), nullable=False)
    upvoteCount=db.Column(db.Integer, default=0)
    createdTime=db.Column(db.DateTime, default=datetime.datetime.now)
    postType=db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Post {}>".format(self.description)



class Reaction(db.Model):
    postID=db.Column(db.Integer, db.ForeignKey(Post.postID),primary_key=True)
    reactingUser=db.Column(db.String(20), db.ForeignKey(User.username), primary_key=True)
    reactionType=db.Column(db.String(10), default="upvote")


db.create_all()