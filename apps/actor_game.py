import random
import requests
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# A lot of base code was done by hand and then refactored using ChatGPT
# Below is the link to my VERY long chat with ChatGPT working on various things like debugging, refactoring, and generating front end interface
# https://chatgpt.com/c/6941f83a-2be8-832e-bac8-f3cfc6945287

load_dotenv()

def get_random_movie():
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")

    # The code below only searches out of the first 25 pages out of about 500 to get more well known movies
    page_number = random.randint(1, 25)
    movie_number = random.randint(0, 19)

    url = f"https://api.themoviedb.org/3/discover/movie?language=en-US&page={page_number}&sort_by=popularity.desc&vote_count.gte=3000&vote_average.gte=6.8&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    movies = response.json()["results"]

    movie = movies[movie_number]
    movie_id = movie["id"]
    movie_title = movie["title"]

    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US&api_key={TMDB_API_KEY}"
    credits_response = requests.get(credits_url)
    credits = credits_response.json()["cast"]

    # Once it find a movie and finds its credits, it pulls information from the first 5 actors
    actor_list = [
        {"name": actor["name"], "profile_path": actor["profile_path"]}
        for actor in credits
        if actor["known_for_department"] == "Acting"
    ][:5]

    return movie_title, actor_list

# Takes user input and says whether it is correct or not
def play_movie_guess_game(movie_title, actor_list):
    print("Guess the movie based on the actors!")

    for actor in reversed(actor_list):
        if actor.get("profile_path"):
            actor_url = f"https://image.tmdb.org/t/p/w500{actor['profile_path']}"
            response = requests.get(actor_url)
            img = Image.open(BytesIO(response.content))

            plt.imshow(img)
            plt.axis("off")
            plt.show()

        user_guess = input(f"Actor: {actor['name']}\nYour guess for the movie: ").strip()

        if user_guess.lower() == movie_title.lower():
            print("Congratulations! You guessed correctly!")
            return

    print(f"Out of guesses! The movie was: {movie_title}")


if __name__ == "__main__":
    movie_title, actor_list = get_random_movie()
    play_movie_guess_game(movie_title, actor_list)
