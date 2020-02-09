
# openForum

A web application for an open forum platform. Users can create a new thread and add comments to it. Users will be rewarded with user badges and can see leaderboards. 


## Information

### ER Diagram

![ER Diagram](https://i.imgur.com/nb2eLD3.png)

### API Documentation

The API documentation can be found here [Postman Link](https://www.getpostman.com/collections/9d5517095fcec4866f22).

### Requirements

The requirements for the application:
* A user can login with a social media account let’s say Google or Facebook. User level information like Full Name, DOB, Demographic details should be captured.
* Users can create posts which can have images attached to it along with a description and a title which users can comment upon.
* An upvote system for both posts and comments.
* Each post and a comment will offer the users some points. Based on the User’s total score he will get badges.
* Badges can be like Level 1(Contributor), Level 2 (Regular Contributor), Level 3(Great Contributor), Level 4 (Ace Contributor).
* A leaderboard which shows trending posts and all time great users and posts.


## Usage

### Tools and Tech

1. Python 3
2. Flask
3. SQL-ALchemy
4. Sentry
5. ImgurPython API

### How To Run:
 
Its hosted on [https://openforum-project.herokuapp.com](https://openforum-project.herokuapp.com)

1. Clone the repo
 
     `git clone https://github.com/m-luqman/new-open-forum.git`  or  [Download zip](https://github.com/m-luqman/new-open-forum/archive/master.zip)
 
2. Move to the openForum project

     `$  cd openForum/`
     
     2a. Activate the virtualenv`
     
     `$  source venv/bin/activate`

3. Set the environment var FLASK_APP

     `$  export FLASK_APP=openforum.py`

4. Run the app from flask

     4a. Move to App folder
     
      `$ cd App/`

      `$ flask run --reload --cert=adhoc`

      *adhoc cert is for SSL certificate for authentication with Google*

