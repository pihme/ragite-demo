"""Unit tests for the download, cache-path and model-name checks in scripts/build-demo-db."""

import importlib.machinery
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_loader = importlib.machinery.SourceFileLoader("build_demo_db_checks", str(ROOT / "scripts" / "build-demo-db"))
_spec = importlib.util.spec_from_loader("build_demo_db_checks", _loader)
build = importlib.util.module_from_spec(_spec)
_loader.exec_module(build)


@pytest.mark.parametrize("url", [
    "https://github.com/pihme/ragite/releases/download/x/libragite.so",
    "https://raw.githubusercontent.com/pihme/ragite/abc/README.md",
    "https://sqlite.org/2026/sqlite-doc.zip",
    "https://de.wikipedia.org/w/api.php?action=parse",
])
def test_known_https_urls_pass(url):
    assert build.check_url(url) == url


@pytest.mark.parametrize("url", [
    "http://sqlite.org/x.zip",
    "file:///etc/passwd",
    "https://example.com/x",
    "https://evilsqlite.org/x",
    "https://evil.com/?.wikipedia.org",
])
def test_other_urls_are_refused(url):
    with pytest.raises(SystemExit):
        build.check_url(url)


def test_fetch_refuses_before_any_request():
    with pytest.raises(SystemExit):
        build.fetch("http://example.com/")


def test_inside_keeps_paths_in_the_cache(tmp_path):
    assert build.inside(tmp_path, "ragite", "abc", "docs/guide.md") == tmp_path / "ragite" / "abc" / "docs" / "guide.md"
    with pytest.raises(SystemExit):
        build.inside(tmp_path, "ragite", "abc", "../../../etc/passwd")
    with pytest.raises(SystemExit):
        build.inside(tmp_path, "/etc/passwd")


def test_model_name_check():
    name = "potion-retrieval-32M@6fc8051fab2a1e0ee76689cf08c853792ac285e7"
    assert build.check_model(name) == name
    for bad in ("x') ; DROP TABLE docs; --", "a b", ""):
        with pytest.raises(SystemExit):
            build.check_model(bad)
