import os
from flask import Flask
from web_app.routes.home_routes import home_routes
from web_app.routes.auth_routes import auth_routes
from web_app.routes.search_routes import search_routes

from authlib.integrations.flask_client import OAuth

SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

def create_app():
    app = Flask(__name__)

    # for Flash
    app.config["SECRET_KEY"] = SECRET_KEY

    #
    # AUTH
    #

    oauth = OAuth(app)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        #authorize_params={"access_type": "offline"} # give us the refresh token! see: https://stackoverflow.com/questions/62293888/obtaining-and-storing-refresh-token-using-authlib-with-flask
    )
    app.config["OAUTH"] = oauth
    
    ## Routes

    app.register_blueprint(home_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(search_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)