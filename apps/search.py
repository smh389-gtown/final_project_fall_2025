import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

def tmdb_like_search_movies(phrase, max_pages=50):
    """
    Search TMDB movies using SQL-like %phrase% matching
    and return rich movie metadata.
    """

    matches = []
    page = 1

    while True:
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            params={
                "api_key": TMDB_API_KEY,
                "page": page,
                "language": "en-US",
                "sort_by": "popularity.desc"
            }
        )

        if response.status_code != 200:
            break

        data = response.json()

        for movie in data.get("results", []):
            title = movie.get("title", "")

            if phrase.lower() in title.lower():
                matches.append({
                    "id": movie.get("id"),
                    "title": title,
                    "release_date": movie.get("release_date"),
                    "overview": movie.get("overview"),
                    "rating": movie.get("vote_average"),
                    "vote_count": movie.get("vote_count"),
                    "popularity": movie.get("popularity"),
                    "poster_url": (
                        f"{POSTER_BASE_URL}{movie['poster_path']}"
                        if movie.get("poster_path")
                        else None
                    ),
                    "backdrop_url": (
                        f"{POSTER_BASE_URL}{movie['backdrop_path']}"
                        if movie.get("backdrop_path")
                        else None
                    )
                })

        page += 1

        if page > data.get("total_pages", 1) or page > max_pages:
            break

    return matches
