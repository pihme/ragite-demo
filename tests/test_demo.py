"""Smoke tests for the built demo.db served through Datasette's test client.

Needs a built app/demo.db (scripts/build-demo-db) and libragite.so. RAGITE_LIB points at
the library (default: ./libragite.so, where build-demo-db puts the release).
"""

import json
import os
import sqlite3
from pathlib import Path

import pytest
import yaml
from datasette.app import Datasette

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"
SOURCES = json.loads((ROOT / "data" / "sources.json").read_text())
LIB = os.environ.get("RAGITE_LIB") or str(ROOT / "libragite.so")
LIB_ARG = LIB[: -len(".so")] if LIB.endswith(".so") else LIB


@pytest.fixture(scope="module")
def ds():
    assert (APP / "demo.db").exists(), "build app/demo.db first: scripts/build-demo-db"
    return Datasette(
        [str(APP / "demo.db")],
        metadata=yaml.safe_load((APP / "metadata.yml").read_text()),
        settings=json.loads((APP / "settings.json").read_text()),
        template_dir=str(APP / "templates"),
        static_mounts=[("static", str(APP / "static"))],
        sqlite_extensions=[LIB_ARG],
    )


async def rows(ds, query, **params):
    params.setdefault("collection", "")
    resp = await ds.client.get(f"/demo/{query}.json", params={**params, "_shape": "objects"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data.get("ok", True), data
    return data["rows"]


def test_every_source_is_indexed():
    con = sqlite3.connect(APP / "demo.db")
    counts = dict(con.execute("SELECT collection, count(*) FROM doc_info GROUP BY collection"))
    assert counts["sqlite-docs"] == len(SOURCES["sqlite_docs"]["pages"])
    assert counts["wikipedia"] == len(SOURCES["wikipedia"]["articles"])
    assert counts["ragite-docs"] == len(SOURCES["ragite_docs"]["files"])
    revisions = {r for (r,) in con.execute("SELECT revision FROM doc_info WHERE collection = 'wikipedia'")}
    assert revisions == {str(a["revid"]) for a in SOURCES["wikipedia"]["articles"]}
    assert dict(con.execute("SELECT key, value FROM build_info"))["model"] == SOURCES["ragite"]["model"]


@pytest.mark.asyncio
async def test_hybrid_search_finds_the_backup_api(ds):
    found = await rows(ds, "search", q="How do I copy a database while it is in use?")
    assert found and len(found) <= 20
    assert "sqlite.org/backup.html" in found[0]["url"]
    scores = [r["score"] for r in found]
    assert scores == sorted(scores, reverse=True)
    assert {"title", "url", "collection", "heading_path", "chunk", "score"} <= set(found[0])


@pytest.mark.asyncio
async def test_collection_filter(ds):
    found = await rows(ds, "search", q="What is a B-tree?", collection="wikipedia")
    assert found and all(r["collection"] == "wikipedia" for r in found)
    assert any("B-tree" in r["title"] for r in found)


@pytest.mark.asyncio
async def test_vector_search(ds):
    found = await rows(ds, "vector_search", q="What is write-ahead logging?")
    assert found and "wal.html" in found[0]["url"]
    assert all(-1.0 <= r["score"] <= 1.0 for r in found)


@pytest.mark.asyncio
async def test_fulltext_search(ds):
    found = await rows(ds, "fulltext_search", q='"vacuum" "into"')
    assert found and all("vacuum" in r["chunk"].lower() for r in found)


@pytest.mark.asyncio
async def test_document_search(ds):
    found = await rows(ds, "search_documents", q="command line shell output modes")
    assert any("cli.html" in r["url"] for r in found[:3])


@pytest.mark.asyncio
async def test_empty_query_returns_nothing(ds):
    for query in ("search", "vector_search"):
        assert await rows(ds, query, q="") == []


@pytest.mark.asyncio
async def test_search_page_and_assets(ds):
    page = await ds.client.get("/search")
    assert page.status_code == 200
    assert 'id="rs-q"' in page.text and "/static/search.js" in page.text
    for asset in ("search.js", "search.css"):
        assert (await ds.client.get(f"/static/{asset}")).status_code == 200
