"""Smoke tests for the built demo.db served through Datasette's test client.

Needs a built app/demo.db (scripts/build-demo-db) and libragite.so. RAGITE_LIB points at
the library (default: ./libragite.so, where build-demo-db puts the release).
"""

import json
import os
import re
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
async def test_document_search(ds):
    found = await rows(ds, "search_documents", q="command line shell output modes")
    assert any("cli.html" in r["url"] for r in found[:3])
    assert len({r["url"] for r in found}) == len(found)
    wiki = await rows(ds, "search_documents", q="What is a B-tree?", collection="wikipedia")
    assert wiki and all(r["collection"] == "wikipedia" for r in wiki)


@pytest.mark.asyncio
async def test_empty_query_returns_nothing(ds):
    for query in ("search", "search_documents"):
        assert await rows(ds, query, q="") == []


@pytest.mark.asyncio
async def test_only_hybrid_queries_are_offered(ds):
    # The demo uses ragite's public interface only: docs, docs_chunks and the ragite_* functions.
    queries = (await ds.client.get("/demo.json")).json()["queries"]
    assert sorted(q["name"] for q in queries) == [
        "chunks_with_document", "document_chunks", "embed", "model", "search", "search_documents"]
    for q in queries:
        for storage in ("docs_vec", "docs_fts", "docs_chunk_rows", "docs_documents", "docs_model"):
            assert storage not in q["sql"], (q["name"], storage)


@pytest.mark.asyncio
async def test_search_page_and_assets(ds):
    page = await ds.client.get("/search")
    assert page.status_code == 200
    assert 'id="rs-q"' in page.text and "/static/search.js" in page.text
    assert 'name="mode"' not in page.text
    assert 'id="rs-filter-hint"' in page.text
    for asset in ("search.js", "search.css"):
        assert (await ds.client.get(f"/static/{asset}")).status_code == 200
    # The source filter is a set of radio chips with the same parameter name and values (SPEC D10).
    for value in ("", "sqlite-docs", "wikipedia", "ragite-docs"):
        assert f'name="collection" value="{value}"' in page.text, value


@pytest.mark.asyncio
async def test_global_style_and_fonts_are_local(ds):
    # SPEC D11: Datasette's pages load one global stylesheet and script; fonts are served from static/.
    home = await ds.client.get("/")
    assert "/static/ragite-demo.css" in home.text and "/static/ragite-demo.js" in home.text
    assert "Powered by" in home.text and "datasette.io" in home.text
    css = (await ds.client.get("/static/ragite-demo.css")).text
    fonts = re.findall(r"url\(([^)]+)\)", css)
    assert fonts and all(f.startswith("/static/fonts/") for f in fonts), fonts
    for f in fonts:
        resp = await ds.client.get(f)
        assert resp.status_code == 200 and len(resp.content) > 1000, f
    for asset in ("ragite-demo.js", "fonts/OFL-geist.txt", "fonts/OFL-geist-mono.txt", "fonts/OFL-space-grotesk.txt"):
        assert (await ds.client.get(f"/static/{asset}")).status_code == 200, asset


@pytest.mark.asyncio
async def test_search_rows_point_at_their_chunk(ds):
    # The search page links every card to /demo/docs_chunks/{chunk_id}; that row must be the hit.
    found = await rows(ds, "search", q="What is write-ahead logging?")
    assert found
    for r in found:
        resp = await ds.client.get(f"/demo/docs_chunks/{r['chunk_id']}.json", params={"_shape": "objects"})
        assert resp.status_code == 200, resp.text
        (chunk,) = resp.json()["rows"]
        assert (chunk["doc_id"], chunk["start"], chunk["chunk"]) == (r["doc_id"], r["start"], r["chunk"])


@pytest.mark.asyncio
async def test_chunks_with_document(ds):
    found = await rows(ds, "chunks_with_document", q="What is a B-tree?")
    assert found and len(found) <= 10
    assert {"title", "license", "revision", "format", "start", "end", "chunk"} <= set(found[0])
    assert all(0 <= r["start"] <= r["end"] <= r["document_length"] for r in found)


@pytest.mark.asyncio
async def test_document_chunks(ds):
    found = await rows(ds, "document_chunks", doc_id="1")
    assert found and all(r["doc_id"] == 1 for r in found)
    assert [r["chunk_id"] for r in found] == sorted(r["chunk_id"] for r in found)


@pytest.mark.asyncio
async def test_model_and_embed(ds):
    (model,) = await rows(ds, "model")
    assert model["technical_id"] == model["table_model"] == SOURCES["ragite"]["model"]
    (emb,) = await rows(ds, "embed", text="write-ahead logging", role="query")
    assert emb["dimensions"] == 512 and len(emb["first_16_bytes"]) == 32
    assert await rows(ds, "embed", text="", role="query") == []


@pytest.mark.asyncio
async def test_few_near_empty_chunks(ds):
    # The cleaning joins table rows and short lists (scripts/build-demo-db), so near-empty Chunks
    # are mostly headings, which ragite keeps as their own Chunks. Before the joining: 23 %.
    resp = await ds.client.get("/demo.json", params={
        "sql": "SELECT count(*) AS n, sum(length(chunk) < 30) AS short FROM docs_chunks", "_shape": "array"})
    assert resp.status_code == 200, resp.text
    row = resp.json()[0]
    assert row["short"] / row["n"] < 0.16, row
    nbsp = await ds.client.get("/demo.json", params={
        "sql": "SELECT count(*) AS n FROM docs_chunks WHERE instr(chunk, char(160)) > 0", "_shape": "array"})
    assert nbsp.json()[0]["n"] == 0


PASSAGE_QUERIES = ["vacuum", "Who uses B-trees and why?", "WAL", "backup", "What is write-ahead logging?"]


@pytest.mark.asyncio
async def test_short_hits_come_with_context(ds):
    found = await rows(ds, "search", q="vacuum")
    heading = next(r for r in found if r["chunk"] == "VACUUM")
    ctx = json.loads(heading["context"])
    assert 1 <= len(ctx) <= 2 and all(len(t) >= 40 for t in ctx), ctx
    assert ctx[0].startswith("The VACUUM command rebuilds the database file")
    for r in found:
        if len(r["chunk"]) >= 80:
            assert json.loads(r["context"]) == [], r["chunk"][:40]


@pytest.mark.asyncio
@pytest.mark.parametrize("q", PASSAGE_QUERIES)
async def test_each_passage_is_shown_once(ds, q):
    found = await rows(ds, "search", q=q)
    assert len(found) == 20
    # SPEC D9: no card displays a span (its hit or a context chunk) that is at least half displayed
    # by better cards of the same document already.
    shown = {}
    for r in found:
        spans = json.loads(r["spans"])
        assert len(spans) == len(json.loads(r["context"])) + 1
        for s, e in spans:
            seen = sum(max(0, min(e, e2) - max(s, s2)) for s2, e2 in shown.get(r["doc_id"], []))
            assert 2 * seen < e - s, (r["chunk"][:40], s, e, seen)
        shown.setdefault(r["doc_id"], []).extend(spans)
    # No card repeats the text of another card, and no hit is also shown as another card's context.
    keys = [" ".join([r["chunk"], *json.loads(r["context"])]).strip().lower() for r in found]
    assert len(set(keys)) == len(keys)
    ctx = [t for r in found for t in json.loads(r["context"])]
    assert not set(r["chunk"] for r in found) & set(ctx)
    assert [r["score"] for r in found] == sorted((r["score"] for r in found), reverse=True)


CONTEXT_QUERIES = PASSAGE_QUERIES + ["foreign key", "how does a b-tree work", "pragma journal_mode", "window functions"]


@pytest.mark.asyncio
@pytest.mark.parametrize("q", CONTEXT_QUERIES)
async def test_at_most_two_context_chunks(ds, q):
    for coll in ("", "sqlite-docs", "wikipedia", "ragite-docs"):
        for r in await rows(ds, "search", q=q, collection=coll):
            ctx = json.loads(r["context"])
            assert len(ctx) <= 2, (q, coll, r["chunk"][:40], len(ctx))
            assert len(json.loads(r["spans"])) == len(ctx) + 1


@pytest.mark.asyncio
async def test_split_paragraph_pieces_both_stay(ds):
    # A long paragraph is cut into pieces that share a short overlap (ragite REQ-70). The overlap alone
    # must not drop the neighbouring piece: "Window functions come in two varieties" is the best answer.
    found = await rows(ds, "search", q="window functions")
    piece = next((r for r in found if r["chunk"].startswith("Window functions come in two varieties")), None)
    assert piece is not None, [r["chunk"][:40] for r in found]
    neighbours = [r for r in found if r is not piece and r["doc_id"] == piece["doc_id"]
                  and r["start"] < piece["end"] and r["end"] > piece["start"]]
    assert neighbours, "expected an overlapping piece of the same paragraph in the results too"

@pytest.mark.asyncio
async def test_source_filter_limit_is_real(ds):
    # Documents the limit the search page warns about (pihme/ragite#49): the filter runs after fusion.
    # When ragite fixes it, this test fails and the hint can go.
    assert await rows(ds, "search", q="virtual table", collection="ragite-docs") == []
    resp = await ds.client.get("/demo.json", params={"sql": (
        "SELECT count(*) AS n FROM docs_chunks c JOIN doc_info i ON i.doc_id = c.doc_id "
        "WHERE i.collection = 'ragite-docs' AND lower(c.chunk) LIKE '%virtual table%'"), "_shape": "array"})
    assert resp.json()[0]["n"] > 0
