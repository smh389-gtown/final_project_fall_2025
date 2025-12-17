import os
from dotenv import load_dotenv
from flask import Flask

from web_app.routes.game_routes import game_bp
from web_app.routes.home_routes import home_routes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    # register blueprints
    app.register_blueprint(home_routes)
    app.register_blueprint(game_bp, url_prefix="/game")


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
