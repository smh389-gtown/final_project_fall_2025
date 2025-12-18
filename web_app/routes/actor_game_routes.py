from flask import Blueprint, request, render_template, session
from apps.actor_game import get_random_movie 

actor_game_routes = Blueprint("actor_game_routes", __name__)

# Since some of this rendered front end, that part was also created with ChatGPT assistance
# https://chatgpt.com/c/6941f83a-2be8-832e-bac8-f3cfc6945287


@actor_game_routes.route("/actor/form")
def form():
    movie_title, actor_list = get_random_movie()
    session["movie_title"] = movie_title
    session["actor_list"] = actor_list

    return render_template("actor_form.html", actors=actor_list)


@actor_game_routes.route("/actor/results", methods=["POST"])
def results():
    user_guess = request.form.get("user_guess", "").strip()
    movie_title = session.get("movie_title")
    actor_list = session.get("actor_list")

    if not movie_title or not actor_list:
        return "Session expired. Please try again.", 400

    if user_guess.lower() == movie_title.lower():
        outcome = "Congratulations! You guessed correctly!"
    else:
        outcome = f"Sorry, the correct movie was: {movie_title}"

    return render_template(
        "actor_game_results.html",
        user_guess=user_guess,
        actors=actor_list,
        outcome=outcome
    )
