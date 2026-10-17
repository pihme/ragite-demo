# ragite-demo spec

## Goal

Show what ragite does in a few minutes, with no code to write: one command builds a SQLite file from freely licensed text, one command serves it with a search page and the full SQL interface.

## Decisions

- **D1 Datasette as the base.** Datasette loads SQLite extensions, so ragite's `MATCH` queries run in its SQL views and JSON API. The demo adds canned queries (`app/metadata.yml`) and one custom page (`app/templates/pages/search.html`) that calls them; no own web server.
- **D2 Public interface only.** Every search is ragite's hybrid `MATCH` on `docs` (documents) or `docs_chunks` (chunks). No vector-only or full-text-only mode and no queries against ragite's storage tables (`docs_vec`, `docs_fts`, ...): they are not part of the ragite 1.0 spec.
- **D3 Data.** SQLite documentation (public domain, a 74-page subset of the pinned doc archive), five Wikipedia articles (CC BY-SA 4.0, pinned revisions) and the ragite docs (MIT OR Apache-2.0, pinned commit). Only freely licensed data; no benchmark sets.
- **D4 demo.db is built, not committed.** It is ~24 MB and rebuilt from pinned inputs in seconds. CI uploads it as an artifact with `DATA_SOURCES.md`.
- **D5 HTML cleaning before indexing.** Page chrome, navigation, scripts, styles, SVG diagrams, infoboxes, footnote markers and link-only sections are removed so chunks hold prose. Text is not rewritten.
- **D6 Platform.** Linux x86-64 only, until ragite ships other release binaries (pihme/ragite#35).
- **D7 License.** Code MIT; data keeps its own license.
