import random

from apps.actor_game import get_random_movie


def test_get_random_movie_returns_title_and_5_actors(set_tmdb_key, mock_get, monkeypatch):
    # deterministic random choices
    monkeypatch.setattr(random, "randint", lambda a, b: a)

    discover_payload = {
        "results": [{"id": 123, "title": "Test Movie"}] + [{"id": i, "title": f"Movie {i}"} for i in range(200, 230)]
    }
    credits_payload = {
        "cast": [
            {"name": "Actor 1", "profile_path": "/a1.jpg", "known_for_department": "Acting"},
            {"name": "Actor 2", "profile_path": "/a2.jpg", "known_for_department": "Acting"},
            {"name": "Actor 3", "profile_path": "/a3.jpg", "known_for_department": "Acting"},
            {"name": "Actor 4", "profile_path": "/a4.jpg", "known_for_department": "Acting"},
            {"name": "Actor 5", "profile_path": "/a5.jpg", "known_for_department": "Acting"},
            {"name": "Actor 6", "profile_path": "/a6.jpg", "known_for_department": "Acting"},
        ]
    }

    # We need different payloads based on the URL
    import requests

    def fake_get(url, *args, **kwargs):
        from test.conftest import FakeResponse
        if "discover/movie" in url:
            return FakeResponse(discover_payload)
        if "credits" in url:
            return FakeResponse(credits_payload)
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(requests, "get", fake_get)

    title, actors = get_random_movie()

    assert title == "Test Movie"
    assert len(actors) == 5
    assert all("name" in a for a in actors)
