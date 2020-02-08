#from model.entities import *
from App.models import *
from App.routes import *
from sqlalchemy.orm import contains_eager
from operator import itemgetter


def get_chronological_topics(offset,limit):
    topics= db.session.query(Topic).\
        join(Topic.posts).\
        filter(Post.postType == 'PRIMARY').\
        order_by(Post.createdTime.desc()).\
        options(contains_eager(Topic.posts)).\
        all()

    return [topic.serialize_with_one_post for topic in topics]


def get_reverse_chronological_posts(topicID,offset,limit):
    posts= db.session.query(Post).\
            filter_by(topicID=topicID).\
            order_by(Post.createdTime).\
            all()

    return [post.serialize for post in posts]

def get_great_topics(offset=0,limit=10):

    topics = db.session.query(Topic).\
        join(Topic.posts).\
        filter(Post.postType == 'PRIMARY').\
        order_by(Post.upvoteCount.desc(), Topic.secondaryPostCount.desc()).\
        options(contains_eager(Topic.posts)).\
        all()

    return [topic.serialize_with_one_post for topic in topics]

def get_trending_topics(level,offset=0,limit=10):
    
    from datetime import datetime, timedelta
    today = datetime.today()
    level=level.lower().strip()
    
    if level == "day":
        otherday = today - timedelta(2)
    elif level == "week":
        otherday = today - timedelta(8)
    elif level == "month":
        otherday = today - timedelta(31)

    topics = db.session.query(Topic).\
        join(Topic.posts).\
        filter(Post.postType == 'PRIMARY').\
        filter(Post.createdTime.between(otherday, today)).\
        order_by(Post.upvoteCount.desc(), Topic.secondaryPostCount.desc()).\
        options(contains_eager(Topic.posts)).\
        all()
            
    return [topic.serialize_with_one_post for topic in topics]
    
def get_great_users(offset=0,limit=10):
    
    users= db.session.query(User).\
            order_by(User.total_points.desc()).\
            all()
    
    return [user.serialize for user in users]

def insert_secondary_post(topicID,username,description):
    
    secondary_post=Post(topicID=topicID,description=description,postingUser=username,postType="SECONDARY")
    db.session.add(secondary_post)
    db.session.flush()
    db.session.commit()

    topic = Topic.query.get(int(topicID))
    topic.secondaryPostCount+=1
    db.session.add(topic)
    db.session.commit()

    user=User.query.filter_by(username=username).first()
    user.secondaryPostCount+=1
    db.session.add(user)
    db.session.commit()
    
    return secondary_post.serialize



def insert_primary_post(username,description,title):

    topic=Topic(title=title)
    db.session.add(topic)
    db.session.commit()
    
    primary_post=Post(topicID=topic.topicID,description=description,postingUser=username,postType="PRIMARY")
    db.session.add(primary_post)
    db.session.flush()
    db.session.commit()

    user=User.query.filter_by(username=username).first()
    user.primaryPostCount+=1
    db.session.add(user)
    db.session.commit()
    
    return primary_post.serialize



def insert_upvote(username,post_id):

    post=Post.query.get(post_id)
    post.upvoteCount+=1
    db.session.add(post)
    db.session.commit()

    reaction=Reaction(postID=post_id,reactingUser=username)
    db.session.add(reaction)
    db.session.flush()
    db.session.commit()

    return str(post.upvoteCount)
  

def is_upvoted(username,post_id):
    return bool(Reaction.query.filter_by(postID=post_id,reactingUser=username).first())
