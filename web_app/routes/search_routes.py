from flask import Blueprint, render_template, request, flash
from app.services.tmdb_service import tmdb_like_search_movies

search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/search", methods=["GET"])
def movie_search():
    query = request.args.get("q", "").strip()
    movies = []

    if query:
        try:
            movies = tmdb_like_search_movies(query, max_pages=50)

            if not movies:
                flash(f"No movies found matching '{query}'.", "warning")

        except Exception as e:
            flash("Error retrieving movies. Please try again later.", "danger")
            print("TMDB ERROR:", e)

    else:
        flash("Please enter a search term.", "info")

    return render_template(
        "movie_search_results.html",
        movies=movies,
        active_page="game"
    )