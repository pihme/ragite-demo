# ragite-demo

Search the SQLite docs and Wikipedia in your browser with [ragite](https://github.com/pihme/ragite) and [Datasette](https://datasette.io/), offline and in one SQLite file.

![The search page: a question about copying a live database, answered with passages from the SQLite Backup API docs](docs/search.png)

ragite is a SQLite extension for retrieval: it splits documents into chunks, embeds them on the CPU and finds the best passages with a hybrid search (vector similarity plus BM25 full text). This demo indexes about 1.7 MB of freely licensed text and serves it with Datasette, so you get a search page without writing a web app, and the full SQL interface next to it.

## Requirements

- **Linux x86-64.** ragite publishes release binaries for Linux only so far ([pihme/ragite#35](https://github.com/pihme/ragite/issues/35)). On macOS or Windows, use a Linux container or build ragite yourself.
- Python 3.10+ whose `sqlite3` module can load extensions (true for most Linux builds; check with `python3 -c "import sqlite3; sqlite3.connect(':memory:').enable_load_extension(True)"`).
- About 165 MB of disk: `libragite.so` is ~135 MB because the embedding model is built in; `demo.db` is ~24 MB.

## Quickstart

```bash
git clone https://github.com/pihme/ragite-demo.git
cd ragite-demo
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# Downloads libragite.so (ragite v0.3.0) and the pinned sources, checks them, builds app/demo.db.
scripts/build-demo-db

# The demo with the search page: http://127.0.0.1:8001/search
datasette serve app --load-extension ./libragite --port 8001
```

`app/` is a Datasette [configuration directory](https://docs.datasette.io/en/stable/settings.html#configuration-directory-mode): it holds `demo.db`, the canned queries in `metadata.yml`, the search page in `templates/pages/search.html` and its local CSS and JavaScript in `static/`. No CDN or external service is used at run time.

Only the database, with Datasette's plain table and SQL views:

```bash
datasette app/demo.db --load-extension ./libragite
```

Pass the library path **without** `.so`: SQLite adds the suffix itself (see the ragite README). Already have a `libragite.so`? `scripts/build-demo-db --lib /path/to/libragite.so` uses it instead of downloading.

## What you can do

**Search page** (`/search`): type a question and optionally limit it to one source. Results are cards with the document title, the heading path inside the document, the matching chunk with your words highlighted, the source link and the score. Every search links to the same query as SQL.

**Canned queries** (`/demo`, hybrid search only), usable from the browser or as JSON (`/demo/search.json?q=...&collection=&_shape=array`):

| Query | Ranking | Score |
| --- | --- | --- |
| `search` | Hybrid: `docs_chunks MATCH :q`, vector and BM25 fused by Reciprocal Rank Fusion | RRF score, higher is better (at most 2/61) |
| `search_documents` | Hybrid, one row per document (`docs MATCH :q`) | RRF score of the best chunk |

Both use only ragite's public interface, `MATCH` on the Document table and its `_chunks` companion. `collection` is empty for all sources, or one of `sqlite-docs`, `wikipedia`, `ragite-docs`.

**Raw SQL** (`/demo?sql=...`), for example:

```sql
SELECT i.title, c.chunk, c.score
FROM docs_chunks c JOIN doc_info i ON i.doc_id = c.doc_id
WHERE docs_chunks MATCH 'How do I change the output mode of the sqlite3 shell?'
LIMIT 5;
```

SQLite normally runs the search first and then looks up `doc_info` by `doc_id`. The canned queries make that order explicit with a `MATERIALIZED` CTE, so a different query plan can never run the search once per row of the joined table.

## Data

| Collection | Documents | Cleaned text | License |
| --- | --- | --- | --- |
| SQLite documentation 3.54.1 (subset, incl. the `sqlite3` CLI page) | 74 | 1.54 MB | Public domain |
| Wikipedia: SQLite (en, de), SQL, Relational database, B-tree | 5 | 0.11 MB | CC BY-SA 4.0 |
| ragite README, SPEC, GLOSSARY | 3 | 0.05 MB | MIT OR Apache-2.0 |

That is 8,778 chunks and a 24 MB `demo.db` (2 KB of vector per chunk). Exact sources, pinned revisions, the cleaning steps and attribution: [DATA_SOURCES.md](DATA_SOURCES.md).

`demo.db` is not committed: it is a 24 MB binary that the build script recreates from pinned inputs in a few seconds, and keeping the Wikipedia text out of the repository keeps the code under one license. CI uploads each build as an artifact (`demo-db`, with `DATA_SOURCES.md`).

## Limits

- The built-in model (potion-retrieval-32M) is trained for English. In this small set, German questions still find the German Wikipedia article, but expect weaker ranking for non-English text in general.
- ragite's full-text side matches the query as one phrase, so long questions usually rank by vector similarity alone; short keyword queries get both.
- The SQLite docs link to sqlite.org, which may already describe a newer version than 3.54.1.

## Tests

```bash
pip install -r requirements-dev.txt
make demo-db test            # build, then Datasette test-client checks
make serve & make smoke      # the same searches over HTTP
```

CI builds `demo.db`, runs the tests, queries a running `datasette serve` with `curl`, and uploads screenshots of the search page (artifact `screenshots`).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security issues: [SECURITY.md](SECURITY.md).

## How this project is built

ragite-demo is developed agent-first. AI coding agents write all code,
tests, and documentation, and review each other's changes, under human
direction: specs, design decisions, and acceptance based on observed
behaviour and test results. No human reads the code line by line. This
is a deliberate choice. Quality rests on automated tests, CI, and
independent agent review.

Evaluate the code against your own requirements before you depend on it.
Found a problem? Open an issue.

## License

Code: [MIT](LICENSE). The indexed data keeps its own licenses ([DATA_SOURCES.md](DATA_SOURCES.md)). Third-party software and data: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
