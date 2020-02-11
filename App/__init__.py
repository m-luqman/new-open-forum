from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_login import UserMixin
from oauthlib.oauth2 import WebApplicationClient
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from imgurpython import ImgurClient
from simple_geoip import GeoIP

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

geoip_client = GeoIP(app.config['GEOIPIFY_API_KEY'])
imgur_client = ImgurClient(app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_ID'])
google_client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])
sentry_sdk.init(
    dsn=app.config['SENTRY_KEY'],
    integrations=[FlaskIntegration()]
)


from App import routes, models, repository

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
