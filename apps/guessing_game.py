import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE = "https://api.themoviedb.org/3"

TMDB_MOVIE_URL = "https://www.themoviedb.org/movie/"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/"
PLACEHOLDER_POSTER = None  # or "/static/placeholder.jpg" in Flask

def movie_page_url(movie):
    return f"{TMDB_MOVIE_URL}{movie['id']}"

def poster_url(movie, size="w500"):
    path = movie.get("poster_path")
    if not path:
        return PLACEHOLDER_POSTER
    return f"{TMDB_POSTER_BASE}{size}{path}"

def discover_movies_page(page: int, *, min_votes: int = 10_000):
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "include_adult": "false",
        "region": "US",

        "sort_by": "popularity.desc",
        "with_original_language": "en",
        "vote_count.gte": min_votes,
        "page": page,
    }
    r = requests.get(f"{BASE}/discover/movie", params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def get_two_movies_random_page(page_min=1, page_max=15, min_votes=10_000, max_tries=40):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY missing. Put it in your .env and call load_dotenv() before this runs.")

    for _ in range(max_tries):
        page = random.randint(page_min, page_max)
        data = discover_movies_page(page, min_votes=min_votes)

        total_pages = data.get("total_pages", page_max)
        if page > total_pages:
            continue

        movies = [
            m for m in data.get("results", [])
            if m.get("vote_count", 0) >= min_votes and m.get("original_language") == "en"
        ]

        if len(movies) >= 2:
            return random.sample(movies, 2), page

    raise RuntimeError("Couldn’t find a page with 2+ movies. Try lowering min_votes or expanding page range.")

(a, b), page = get_two_movies_random_page(page_min=1, page_max=15, min_votes=10_000)

movie_a = {
    "title": a["title"],
    "rating": a["vote_average"],
    "votes": a["vote_count"],
    "popularity": a["popularity"],
    "page_url": movie_page_url(a),
    "poster_url": poster_url(a),
}
movie_b = {
    "title": b["title"],
    "rating": b["vote_average"],
    "votes": b["vote_count"],
    "popularity": b["popularity"],
    "page_url": movie_page_url(b),
    "poster_url": poster_url(b),
}

