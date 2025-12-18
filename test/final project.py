import os
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class FakeResponse:
    """Minimal fake `requests` response object used in tests."""
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


@pytest.fixture
def set_tmdb_key(monkeypatch):
    """Ensure TMDB_API_KEY is set for any module that reads it."""
    monkeypatch.setenv("TMDB_API_KEY", "DUMMY")


@pytest.fixture
def mock_get(monkeypatch):
    """Return a function that mocks requests.get to return a chosen payload."""
    import requests

    def _mock(payload):
        monkeypatch.setattr(requests, "get", lambda *args, **kwargs: FakeResponse(payload))

    return _mock
