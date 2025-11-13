import os
import httpx
import pytest
from scraper.fetcher import fetch_url, fetch_all, combine_paths, fetch_url as _fetch_url

# Asegura cache limpia por test
@pytest.fixture(autouse=True)
def _clear_cache():
    _fetch_url.cache_clear()

BASE = os.getenv("SCRAPER_BASE", "http://localhost:8000")


def _server_available():
    try:
        httpx.get(BASE, timeout=0.3)
        return True
    except Exception:
        return False


@pytest.mark.integration
def test_fetch_url_real_server_or_skip():
    if not _server_available():
        pytest.skip(f"Server not available at {BASE}")
    html = fetch_url(BASE)
    assert isinstance(html, str)
    assert len(html) > 0


@pytest.mark.integration
def test_fetch_all_real_server_or_skip():
    if not _server_available():
        pytest.skip(f"Server not available at {BASE}")

    paths = combine_paths(["", "about", "robots.txt"], ["no_existo"])
    res = fetch_all(BASE, paths)
    # Rutas normales deben devolver texto
    assert isinstance(res[""], str) and len(res[""]) > 0
    assert isinstance(res["about"], str) and len(res["about"]) > 0
    assert isinstance(res["robots.txt"], str) and "User-agent" in res["robots.txt"]
    # La inexistente debe ser None
    assert res["no_existo"] is None
