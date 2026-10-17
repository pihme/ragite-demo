# ragite-demo spec

## Goal

Show what ragite does in a few minutes, with no code to write: one command builds a SQLite file from freely licensed text, one command serves it with a search page and the full SQL interface.

## Decisions

- **D1 Datasette as the base.** Datasette loads SQLite extensions, so ragite's `MATCH` queries run in its SQL views and JSON API. The demo adds canned queries (`app/metadata.yml`) and one custom page (`app/templates/pages/search.html`) that calls them; no own web server.
- **D2 Search modes.** Hybrid uses ragite's public interface (`docs_chunks MATCH`, `docs MATCH`). Vector-only and full-text-only query the sqlite-vec and FTS5 tables ragite creates (`docs_vec`, `docs_fts`, documented in the ragite SPEC, section 5.1), with `ragite_embed` for the query vector. These two modes exist to compare rankings and depend on ragite's shadow-table layout.
- **D3 Data.** SQLite documentation (public domain, a 74-page subset of the pinned doc archive), five Wikipedia articles (CC BY-SA 4.0, pinned revisions) and the ragite docs (MIT OR Apache-2.0, pinned commit). Only freely licensed data; no benchmark sets.
- **D4 demo.db is built, not committed.** It is ~24 MB and rebuilt from pinned inputs in seconds. CI uploads it as an artifact with `DATA_SOURCES.md`.
- **D5 HTML cleaning before indexing.** Page chrome, navigation, scripts, styles, SVG diagrams, infoboxes, footnote markers and link-only sections are removed so chunks hold prose. Text is not rewritten.
- **D6 Platform.** Linux x86-64 only, until ragite ships other release binaries (pihme/ragite#35).
- **D7 License.** Code MIT; data keeps its own license.
