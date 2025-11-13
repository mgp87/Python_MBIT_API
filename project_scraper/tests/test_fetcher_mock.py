import httpx
import pytest
from scraper.fetcher import fetch_url, FetchError, combine_paths
import scraper.fetcher as fetcher
import logging


@pytest.fixture(autouse=True)
def _clear_cache():
    # Asegura que lru_cache no contamine entre tests
    fetch_url.cache_clear()


def test_combine_paths():
    a = ["", "about"]
    b = ["login", "register"]
    c = ["robots.txt"]
    assert combine_paths(a, b, c) == ["", "about", "login", "register", "robots.txt"]



def test_fetch_url_success(monkeypatch, caplog):
    class FakeResp:
        def __init__(self, text="OK"):
            self.text = text
        def raise_for_status(self):  # no lanza
            return None

    def fake_get(url, timeout=10.0):
        return FakeResp("HTML CONTENT")

    monkeypatch.setattr(httpx, "get", fake_get)

    # 👇 Asegura que capturamos logs INFO del logger "scraper.fetcher"
    caplog.set_level(logging.INFO, logger="scraper.fetcher")

    res = fetch_url("http://example.com/")
    assert res == "HTML CONTENT"
    assert any("Successfully fetched" in rec.message for rec in caplog.records)


def test_fetch_url_network_error(monkeypatch):
    def fake_get(url, timeout=10.0):
        raise httpx.RequestError("boom", request=httpx.Request("GET", url))

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(FetchError) as exc:
        fetch_url("http://bad-host/")
    assert "Network error" in str(exc.value)


def test_fetch_url_status_error(monkeypatch):
    def fake_get(url, timeout=10.0):
        request = httpx.Request("GET", url)
        resp = httpx.Response(status_code=404, request=request)
        # Simula .raise_for_status que lanza HTTPStatusError
        def raise_for_status():
            raise httpx.HTTPStatusError("404", request=request, response=resp)
        resp.raise_for_status = raise_for_status
        return resp

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(FetchError) as exc:
        fetch_url("http://example.com/not-found")
    assert "Bad status: 404" in str(exc.value)


def test_fetch_url_uses_cache(monkeypatch):
    calls = {"n": 0}

    class FakeResp:
        def __init__(self, text="OK"):
            self.text = text
        def raise_for_status(self):
            return None

    def fake_get(url, timeout=10.0):
        calls["n"] += 1
        return FakeResp(f"content for {url}")

    monkeypatch.setattr(httpx, "get", fake_get)

    url = "http://example.com/cache"
    r1 = fetch_url(url)
    r2 = fetch_url(url)  # Debe venir de la cache
    assert r1 == r2 == "content for http://example.com/cache"
    assert calls["n"] == 1  # solo se llamó una vez a httpx.get

    # Si cambiamos la URL, debe llamar otra vez
    r3 = fetch_url(url + "/other")
    assert calls["n"] == 2
    assert r3.startswith("content for")


def test_fetch_all_mixed(monkeypatch):
    # Mockeamos fetch_url directamente para controlar éxito/fallo por path
    def fake_fetch(url, timeout=10.0):
        if url.endswith("/ok"):
            return "<html>ok</html>"
        else:
            raise fetcher.FetchError("forced fail")

    monkeypatch.setattr(fetcher, "fetch_url", fake_fetch)

    base = "http://localhost:8000"
    paths = ["ok", "fail", "also-fail"]
    res = fetcher.fetch_all(base, paths)
    assert res["ok"] == "<html>ok</html>"
    assert res["fail"] is None
    assert res["also-fail"] is None
