#from model.entities import *
from App.models import *
from App.routes import *
from sqlalchemy.orm import contains_eager
from operator import itemgetter

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
#converts a sql row to dict

def flatten_primary_posts(tabularTopics):
    topics=[]
    for tabularTopic in tabularTopics:
        primaryPost=row2dict(tabularTopic.posts[0])
        topic=row2dict(tabularTopic)
        for key,value in primaryPost.items():
            topic[key]=value
        topics.append(topic)
    return topics

def get_chronological_topics(offset,limit):
    tabularTopics= db.session.query(Topic).\
        join(Topic.posts).\
        filter(Post.postType == 'PRIMARY').\
        order_by(Post.createdTime.desc()).\
        options(contains_eager(Topic.posts)).\
        all()

    return flatten_primary_posts(tabularTopics)


def get_reverse_chronological_posts(topicID,offset,limit):
    tabularPosts= db.session.query(Post).\
            filter_by(topicID=topicID).\
            order_by(Post.createdTime).\
            all()

    return [row2dict(post) for post in tabularPosts]

def get_great_topics(offset=0,limit=10):

    tabularTopics = db.session.query(Topic).\
        join(Topic.posts).\
        filter(Post.postType == 'PRIMARY').\
        order_by(Post.upvoteCount.desc(), Topic.secondaryPostCount.desc()).\
        options(contains_eager(Topic.posts)).\
        all()

    return flatten_primary_posts(tabularTopics)

def get_trending_topics(level,offset=0,limit=10):
    
    from datetime import date, timedelta
    today = date.today()
    level=level.lower().strip()
    
    if level == "day":
        otherday = today - timedelta(2)
    elif level == "week":
        otherday = today - timedelta(8)
    elif level == "month":
        otherday = today - timedelta(31)

    tabularTopics = db.session.query(Topic).\
        join(Topic.posts).\
        filter(Post.postType == 'PRIMARY').\
        filter(Post.createdTime.between(otherday, today)).\
        order_by(Post.upvoteCount.desc(), Topic.secondaryPostCount.desc()).\
        options(contains_eager(Topic.posts)).\
        all()
    
    return flatten_primary_posts(tabularTopics)
    
def get_great_users(offset=0,limit=10):
    
    users = User.query.all()
    
    _users=[]
    
    for user in [row2dict(user) for user in users]:
        user["totalPoints"]=User.calculate_points(user["primaryPostCount"],user["secondaryPostCount"])
        user["badge"]=User.calculate_badge(user["totalPoints"])
        _users.append(user)
    
    return sorted(_users, key=itemgetter('totalPoints'), reverse=True) 
 


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
    
    return row2dict(secondary_post)



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
    
    return row2dict(primary_post)



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
