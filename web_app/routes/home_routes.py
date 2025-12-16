# this is the "web_app/routes/home_routes.py" file...

from flask import Blueprint, request, render_template
from apps.new_movies_out import get_now_playing

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
@home_routes.route("/home")
def index():
    movies = get_now_playing(limit=8)
    return render_template("home.html", movies=movies)
    