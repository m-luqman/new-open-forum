from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_login import UserMixin
from oauthlib.oauth2 import WebApplicationClient



app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

google_client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])


from App import routes, models, repository

if __name__ == "__main__":
    app.run(ssl_context="adhoc")