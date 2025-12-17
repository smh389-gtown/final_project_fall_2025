import os
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_NOW_PLAYING_URL = "https://api.themoviedb.org/3/movie/now_playing"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w500"

def get_now_playing(limit: int = 8):
    params = {
        "api_key": TMDB_API_KEY,
        "page": 1,
        "language": "en-US",   # translate title/overview to English when available
        "region": "US",
    }

    resp = requests.get(TMDB_NOW_PLAYING_URL, params=params, timeout=20)
    resp.raise_for_status()

    results = resp.json().get("results", [])

    movies = []
    for m in results[:limit]:
        poster_path = m.get("poster_path")
        poster_url = f"{TMDB_POSTER_BASE}{poster_path}" if poster_path else None

        movies.append({
            "title": m.get("title") or m.get("name") or "Untitled",
            "overview": (m.get("overview") or "No overview available.").strip(),
            "poster_url": poster_url or "https://via.placeholder.com/500x750?text=No+Poster",
            "tmdb_url": f"https://www.themoviedb.org/movie/{m.get('id')}",
        })

    return movies
