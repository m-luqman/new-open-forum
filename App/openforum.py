from App import app, db, login_manager
from App.models import *
from App.repository import *
from App.routes import *

if __name__ == '__main__':  # Script executed directly?
    app.run(ssl_context="adhoc")  # Launch built-in web server and run this Flask webapp
