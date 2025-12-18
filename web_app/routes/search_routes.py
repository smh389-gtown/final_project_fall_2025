from flask import Blueprint, render_template, request
from apps.search import tmdb_like_search_movies
from datetime import datetime

# The date formatting gave me some challeges where I needed help from AI plus implementing front end interface
# https://chatgpt.com/c/6942ecfb-21c8-832d-97ff-64cac38cbe5b

search_routes = Blueprint("search", __name__, template_folder="templates")

# Register datetime filter
@search_routes.app_template_filter('datetimeformat')
def jinja_datetimeformat(value, format="%b %d, %Y"):
    if not value:
        return "Unknown"
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime(format)
    except:
        return value

@search_routes.route("/search", methods=["GET"])
def movie_search():
    query = request.args.get("q")
    movies = None

    if query:
        movies = tmdb_like_search_movies(query, max_pages=25)

    return render_template(
        "search.html",
        movies=movies,
        query=query or "",
        active_page="game"
    )
