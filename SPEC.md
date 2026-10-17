# ragite-demo spec

## Goal

Show what ragite does in a few minutes, with no code to write: one command builds a SQLite file from freely licensed text, one command serves it with a search page and the full SQL interface.

## Decisions

- **D1 Datasette as the base.** Datasette loads SQLite extensions, so ragite's `MATCH` queries run in its SQL views and JSON API. The demo adds canned queries (`app/metadata.yml`) and one custom page (`app/templates/pages/search.html`) that calls them; no own web server.
- **D2 Public interface only.** Every search is ragite's hybrid `MATCH` on `docs` (documents) or `docs_chunks` (chunks); other queries use those two tables and the `ragite_*` functions. No vector-only or full-text-only mode and no queries against ragite's storage tables (`docs_vec`, `docs_fts`, ...): they are not part of the ragite 1.0 spec.
- **D3 Data.** SQLite documentation (public domain, a 74-page subset of the pinned doc archive), five Wikipedia articles (CC BY-SA 4.0, pinned revisions) and the ragite docs (MIT OR Apache-2.0, pinned commit). Only freely licensed data; no benchmark sets.
- **D4 demo.db is built, not committed.** It is ~22 MB and rebuilt from pinned inputs in seconds. CI uploads it as an artifact with `DATA_SOURCES.md`.
- **D5 HTML cleaning before indexing.** Page chrome, navigation, scripts, styles, SVG diagrams, infoboxes, footnote markers and link-only sections are removed so chunks hold prose. Text is not rewritten, with three layout exceptions so ragite does not cut near-empty chunks: each table row becomes one paragraph (cells joined by ` | `), each list whose items are all short (at most 100 characters, no nested blocks) becomes one paragraph (items joined by `; `), and Unicode spaces such as U+00A0 become plain spaces.
- **D6 Platform.** Linux x86-64 only, until ragite ships other release binaries (pihme/ragite#35).
- **D7 License.** Code MIT; data keeps its own license.
- **D8 Examples.** `examples/` holds runnable SQL for the public interface. Read-only examples are also canned queries; writes are not, so the served `demo.db` cannot be changed from the browser.
- **D9 Search results: context and each passage once.** The `search` query (`app/metadata.yml`), and with it the search page, works in SQL on `docs_chunks` and `doc_info` only. A short hit (under 80 characters, usually a bare heading) gets the next chunks of the same document and section as context: chunks that start after it, whose heading path begins with the hit's heading path, and that have at least 40 characters; up to two, and only until the card holds 200 characters. A card covers the range from the hit's start to the end of its last context chunk. Cards are taken in score order, and a hit is dropped when its card overlaps the range of a better card of the same document (a heading and the paragraph shown under it, or the overlapping pieces of a split paragraph) or when its text, context included, equals a better card's text after trimming and lower-casing (the same sentence on two pages). The query looks at the best 60 hits and returns at most 20 cards.
