from flask import Blueprint, render_template, request, redirect, url_for, session
from apps.guessing_game import get_two_movies_random_page, movie_page_url, poster_url

game_bp = Blueprint("game", __name__)

def build_movie(movie):
    return {
        "id": movie["id"],
        "title": movie["title"],
        "rating": movie["vote_average"],
        "votes": movie["vote_count"],
        "popularity": movie["popularity"],
        "page_url": movie_page_url(movie),
        "poster_url": poster_url(movie),
    }

@game_bp.route("/", methods=["GET"])
def game():
    (a, b), _ = get_two_movies_random_page()

    movie_a = build_movie(a)
    movie_b = build_movie(b)

    # store current round in session
    session["movie_a"] = movie_a
    session["movie_b"] = movie_b

    return render_template(
        "game.html",
        movie_a=movie_a,
        movie_b=movie_b,
        result=None
    )

@game_bp.route("/guess", methods=["POST"])
def guess():
    choice = request.form.get("choice")

    movie_a = session.get("movie_a")
    movie_b = session.get("movie_b")

    if not movie_a or not movie_b:
        return redirect(url_for("game.game"))

    # determine winner
    if movie_a["rating"] > movie_b["rating"]:
        correct = "A"
    elif movie_b["rating"] > movie_a["rating"]:
        correct = "B"
    else:
        correct = None  # extremely rare tie

    is_correct = (choice == correct)

    return render_template(
        "game.html",
        movie_a=movie_a,
        movie_b=movie_b,
        result={
            "choice": choice,
            "correct": correct,
            "is_correct": is_correct
        }
    )

@game_bp.route("/next", methods=["POST"])
def next_round():
    return redirect(url_for("game.game"))
