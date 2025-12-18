import os
import random
import requests

from apps.actor_game import get_random_movie
# Below is the link to my chat with ChatGPT 
# https://chatgpt.com/c/6943047c-d430-8333-b54b-56ac6f578300

class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def test_get_random_movie_returns_title_and_5_actors(monkeypatch):
    os.environ["TMDB_API_KEY"] = "DUMMY"
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

    def fake_get(url, *args, **kwargs):
        if "discover/movie" in url:
            return FakeResponse(discover_payload)
        if "credits" in url:
            return FakeResponse(credits_payload)
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(requests, "get", fake_get)

    title, actors = get_random_movie()
    assert title == "Test Movie"
    assert len(actors) == 5
