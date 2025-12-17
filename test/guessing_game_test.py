import importlib
import random


def test_get_two_movies_random_page_returns_two_movies(set_tmdb_key, mock_get, monkeypatch):
    # deterministic
    monkeypatch.setattr(random, "randint", lambda a, b: a)
    monkeypatch.setattr(random, "sample", lambda seq, k: list(seq)[:k])

    payload = {
        "total_pages": 1,
        "results": [
            {"id": 1, "title": "A", "vote_count": 12000, "original_language": "en", "poster_path": "/a.jpg"},
            {"id": 2, "title": "B", "vote_count": 15000, "original_language": "en", "poster_path": "/b.jpg"},
            {"id": 3, "title": "C", "vote_count": 20000, "original_language": "en", "poster_path": "/c.jpg"},
        ],
    }
    mock_get(payload)

    import apps.guessing_game as gg
    gg = importlib.reload(gg)

    (m1, m2), page = gg.get_two_movies_random_page(page_min=1, page_max=1, min_votes=10000)

    assert page == 1
    assert m1["id"] != m2["id"]


def test_poster_url_returns_none_if_missing(set_tmdb_key, mock_get):
    mock_get({"total_pages": 1, "results": []})

    import apps.guessing_game as gg
    gg = importlib.reload(gg)

    assert gg.poster_url({"poster_path": None}) is None
