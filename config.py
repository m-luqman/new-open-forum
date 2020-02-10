import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    GOOGLE_CLIENT_SECRET=os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID")
    IMGUR_CLIENT_SECRET=os.environ.get("IMGUR_CLIENT_SECRET")
    IMGUR_CLIENT_ID=os.environ.get("IMGUR_CLIENT_ID")
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    SENTRY_KEY = os.environ.get("SENTRY_KEY")
    GEOIPIFY_API_KEY=os.environ.get("GEOIPIFY_API_KEY")
