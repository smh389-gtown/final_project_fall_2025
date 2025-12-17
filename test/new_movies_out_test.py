from apps.new_movies_out import get_now_playing


def test_get_now_playing_returns_movies_with_expected_keys(set_tmdb_key, mock_get):
    payload = {
        "results": [
            {"id": 1, "title": "Alpha", "overview": "Hello", "poster_path": "/p1.jpg"},
            {"id": 2, "title": "Beta", "overview": "", "poster_path": None},
        ]
    }
    mock_get(payload)

    movies = get_now_playing(limit=8)

    assert isinstance(movies, list)
    assert len(movies) == 2

    m = movies[0]
    assert "title" in m
    assert "overview" in m
    assert "poster_url" in m
    assert "tmdb_url" in m
