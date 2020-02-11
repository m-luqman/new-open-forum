
from flask import render_template, redirect, url_for
from App.repository import *
from oauthlib.oauth2 import WebApplicationClient
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
import requests
import json
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from App import repository
from App import app, google_client, imgur_client,geoip_client, db, login_manager
from flask.json import jsonify
import base64

def get_google_provider_cfg():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()


@app.route("/")
def get_home_page(offset=0,limit=10):
    return render_template('index.html'
                           ,topics=get_chronological_topics(offset=offset,limit=limit)
                           ,isLoggedIn=current_user.is_authenticated)


@app.route("/thread/<string:topicID>")
def get_thread_page(topicID,offset=0,limit=10):
    
    return render_template('thread.html'
                           ,topic=get_topic(topicID)
                           ,posts=get_reverse_chronological_posts(topicID,offset=offset,limit=limit)
                           ,isLoggedIn=current_user.is_authenticated)

@app.route("/leaderboard")
def get_leaderboard_page():
    return render_template('leaderboard.html'
                           ,greatUsers=repository.get_great_users()
                           ,isLoggedIn=current_user.is_authenticated)

@app.route("/create/post")
@login_required
def get_new_post_page():
    return render_template('newPost.html'
                           ,isLoggedIn=current_user.is_authenticated)

@app.route("/greatTopics")
def get_great_topics():
    return jsonify(repository.get_great_topics())


@app.route("/trendingTopics/<string:level>")
def get_trending_topics(level):
    return jsonify(repository.get_trending_topics(level))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route("/upvote", methods=['GET', 'POST'])
@login_required
@use_args({"postID": fields.Int(validate=lambda id: not is_upvoted(username=current_user.username,post_id=id))})
def upvote(args):
    return insert_upvote(username=current_user.username,post_id=args['postID'])


@app.route("/save/comment", methods=['GET', 'POST'])
@login_required
@use_args({
    "description": fields.Str(validate=lambda val: bool(val.strip())),
    "topicID": fields.Int(required=True)
    })
def save_comment(args):
    return insert_secondary_post(
        topicID=args["topicID"]
       ,username=current_user.username
       ,description=args["description"])


@app.route("/save/post", methods=['GET', 'POST'])
@login_required
@use_args({
    "description": fields.Str(validate=lambda val: bool(val.strip())),
    "title": fields.Str(validate=lambda val: bool(val.strip()))
    })
def save_post(args):
    post=insert_primary_post(username=current_user.username,description=args["description"],title=args["title"])    
    return redirect(url_for('get_thread_page',topicID=post["topicID"],title=args["title"]))



@app.route('/login', methods=['GET', 'POST'])
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]


    token_url, headers, body = google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    google_client.parse_request_body_response(json.dumps(token_response.json()))


    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)


    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400


    # Create a user in your db with the information provided
    # by Google
    updatedUserName=users_email.split("@")[0]
    
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip=request.environ['REMOTE_ADDR']
    else:
        ip=request.environ['HTTP_X_FORWARDED_FOR']
    
    geoip_data = geoip_client.lookup(ip)
    print((geoip_data))
    user = User(
        id_=unique_id, country=geoip_data["location"]["country"],region=geoip_data["location"]["region"],username=updatedUserName, fullname=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)
    import time
    if not User.query.filter_by(id_=unique_id).first():
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        time.sleep(1)
        login_user(user)
        #first time logs in -> to update the profile
#        return redirect(url_for("editProfile"))

#     if user_exists(unique_id):
#         db.session.add(user)
#         db.session.commit()
#         login_user(user) #first time logs in -> to update the profile
#         return redirect(url_for("editProfile"))


    # Begin user session by logging the user in
    login_user(user)
#     next_page = request.args.get('next')#takes to next page after login
#     if not next_page or url_parse(next_page).netloc != '':
#         return redirect("/")

    # Send user back to homepage
    return redirect(url_for("get_home_page"))

@app.route("/upload/image", methods=['GET', 'POST'])
def upload_image():
    image_links=[]   
    if request.method == "POST":
        for image in request.files.values():
            b64 = base64.b64encode(image.read())
            data = {'image': b64, 'type': 'base64'}
            response=imgur_client.make_request('POST', 'upload', data, True)
            image_links.append(response["link"])
    
    return jsonify(image_links)    

    

if __name__ == '__main__':  # Script executed directly?
    app.run(ssl_context="adhoc")  # Launch built-in web server and run this Flask webapp
