import os
from flask import Flask
from web_app.routes.home_routes import home_routes
from web_app.routes.auth_routes import auth_routes

from authlib.integrations.flask_client import OAuth

SECRET_KEY = os.getenv("SECRET_KEY")

def create_app():
    app = Flask(__name__)

    # for Flash
    #app.config["SECRET_KEY"] = SECRET_KEY
    
    app.register_blueprint(home_routes)
    app.register_blueprint(auth_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)