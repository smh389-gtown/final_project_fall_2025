import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import time

# Based code off of what I know about searching in sql with help of ChatGPT
# not at all a complex search algorthm
# below is link of my conversation with ChatGPT working on creating this algorithm and debugging along with front end changes
# https://chatgpt.com/c/6942ecfb-21c8-832d-97ff-64cac38cbe5b

def datetimeformat(value):
    """Convert 'YYYY-MM-DD' to 'Jan 01, 2020' style."""
    if not value:
        return "Unknown"
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%b %d, %Y")
    except:
        return value

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3/discover/movie"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"


def tmdb_like_search_movies(phrase, max_pages=50):
    matches = []
    seen_ids = set()
    page = 1

    while True:
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "vote_count.gte": 3000,
            "vote_average.gte": 6.8,
            "page": page
        }

        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print("TMDB API error:", response.status_code)
            break

        data = response.json()
        results = data.get("results", [])

        for movie in results:
            title = movie.get("title", "")
            if phrase.lower() in title.lower():
                movie_id = movie.get("id")
                if movie_id not in seen_ids:
                    seen_ids.add(movie_id)
                    matches.append({
                        "id": movie_id,
                        "title": title,
                        "release_date": datetimeformat(movie.get("release_date")),
                        "overview": movie.get("overview"),
                        "rating": movie.get("vote_average"),
                        "vote_count": movie.get("vote_count"),
                        "popularity": movie.get("popularity"),
                        "poster_url": f"{POSTER_BASE_URL}{movie.get('poster_path')}" if movie.get("poster_path") else None
                    })

        page += 1
        if page > data.get("total_pages", 1) or page > max_pages:
            break

        time.sleep(0.25)

    return matches
