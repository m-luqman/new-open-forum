import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey-we-can-set'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    GOOGLE_CLIENT_ID = "530958200715-qau4bjsgpu9dfn3h4gtvokekr41fp950.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "OM46KDb7CqbdeTRsX7be_xg1"
    GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
