# Data sources

`scripts/build-demo-db` downloads the data below and indexes it into `app/demo.db`. The data is **not** stored in this repository; [`data/sources.json`](data/sources.json) pins every input. The code in this repository is MIT licensed ([LICENSE](LICENSE)); the data keeps its own license, listed here. A built `demo.db` contains all three collections, so whoever passes it on must keep the notices in this file with it, and the Wikipedia part of it stays under CC BY-SA 4.0.

Every document also carries its license, URL and revision in the `doc_info` table of `demo.db`, so the attribution travels with the file.

## 1. SQLite documentation (public domain)

- Source: the documentation archive [`sqlite-doc-3540100.zip`](https://sqlite.org/2026/sqlite-doc-3540100.zip) for SQLite 3.54.1, from <https://sqlite.org/download.html>.
- Pinned by SHA-256 `e9f634ac28a4c7b48f5c389e4b08c039654ec1487512092b330ccfcfdc0816e0` (SHA3-256 as published on the download page: `6ea5c0eff56c7fb305ca85e820070eacd96da44ae9edfb04d4c82d909540297b`).
- License: public domain. "All of the code and documentation in SQLite has been dedicated to the public domain by the authors" (<https://sqlite.org/copyright.html>).
- Subset: 74 pages, chosen for end users (overview, SQL language, CLI, pragmas, JSON, FTS5, WAL, transactions, query planner, backup, limits):
  `about.html`, `whentouse.html`, `features.html`, `serverless.html`, `zeroconf.html`, `selfcontained.html`, `transactional.html`, `onefile.html`, `different.html`, `quirks.html`, `faq.html`, `quickstart.html`, `cli.html`, `datatype3.html`, `flextypegood.html`, `stricttables.html`, `nulls.html`, `lang_select.html`, `lang_createtable.html`, `lang_insert.html`, `lang_update.html`, `lang_delete.html`, `lang_upsert.html`, `lang_returning.html`, `lang_with.html`, `lang_expr.html`, `lang_corefunc.html`, `lang_aggfunc.html`, `lang_datefunc.html`, `lang_mathfunc.html`, `lang_createindex.html`, `lang_createview.html`, `lang_createtrigger.html`, `lang_transaction.html`, `lang_savepoint.html`, `lang_vacuum.html`, `lang_attach.html`, `lang_altertable.html`, `lang_explain.html`, `windowfunctions.html`, `json1.html`, `fts5.html`, `rtree.html`, `pragma.html`, `wal.html`, `atomiccommit.html`, `lockingv3.html`, `isolation.html`, `foreignkeys.html`, `autoinc.html`, `rowidtable.html`, `withoutrowid.html`, `gencol.html`, `partialindex.html`, `expridx.html`, `queryplanner.html`, `optoverview.html`, `eqp.html`, `backup.html`, `inmemorydb.html`, `tempfiles.html`, `howtocorrupt.html`, `limits.html`, `loadext.html`, `vtab.html`, `uri.html`, `mmap.html`, `threadsafe.html`, `appfileformat.html`, `fasterthanfs.html`, `useovernet.html`, `recovery.html`, `security.html`, `lts.html`.
- Changes: page navigation, scripts, styles, tables of contents, images and the inline SVG syntax diagrams are removed before indexing. Each table row is joined into one paragraph (cells separated by ` | `), each list of short items into one paragraph (items separated by `; `), and no-break spaces become plain spaces. The text is otherwise unchanged. `doc_info.url` points to the same page on sqlite.org, which may describe a newer SQLite version.

## 2. Wikipedia articles (CC BY-SA 4.0)

Text from Wikipedia, the free encyclopedia, licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/). The authors are listed in each article's revision history.

| Article | Language | Revision (pinned) | Authors |
| --- | --- | --- | --- |
| SQLite | en | [1378624739](https://en.wikipedia.org/w/index.php?title=SQLite&oldid=1378624739) | [history](https://en.wikipedia.org/w/index.php?title=SQLite&action=history) |
| SQLite | de | [270943976](https://de.wikipedia.org/w/index.php?title=SQLite&oldid=270943976) | [history](https://de.wikipedia.org/w/index.php?title=SQLite&action=history) |
| SQL | en | [1374625236](https://en.wikipedia.org/w/index.php?title=SQL&oldid=1374625236) | [history](https://en.wikipedia.org/w/index.php?title=SQL&action=history) |
| Relational database | en | [1375508962](https://en.wikipedia.org/w/index.php?title=Relational_database&oldid=1375508962) | [history](https://en.wikipedia.org/w/index.php?title=Relational_database&action=history) |
| B-tree | en | [1377462701](https://en.wikipedia.org/w/index.php?title=B-tree&oldid=1377462701) | [history](https://en.wikipedia.org/w/index.php?title=B-tree&action=history) |

- Retrieved through the MediaWiki API (`action=parse&oldid=<revision>`), so the text is the pinned revision. Templates are expanded by Wikipedia at download time, so the rendered markup may drift slightly when a template changes later.
- Changes: infoboxes, images, navigation boxes, edit links, footnote markers and the sections that only hold links or citations (for example "See also", "References", "External links"; "Weblinks", "Einzelnachweise" in German) are removed. Table rows and lists of short items are joined into paragraphs and no-break spaces become plain spaces, as for the SQLite documentation. The remaining text is unchanged and is split into chunks by ragite. These changes are an adaptation under CC BY-SA 4.0; the adapted text in `demo.db` is under the same license.
- Images are not included.

## 3. ragite documentation (MIT OR Apache-2.0)

- Files: `README.md`, `SPEC.md`, `GLOSSARY.md` from [pihme/ragite](https://github.com/pihme/ragite) at commit [`ede2d57`](https://github.com/pihme/ragite/tree/ede2d57e16ad82027fb8c968d8828d035455b7b4).
- License: `MIT OR Apache-2.0`, Copyright (c) 2026 ragite contributors ([LICENSE-MIT](https://github.com/pihme/ragite/blob/ede2d57e16ad82027fb8c968d8828d035455b7b4/LICENSE-MIT), [LICENSE-APACHE](https://github.com/pihme/ragite/blob/ede2d57e16ad82027fb8c968d8828d035455b7b4/LICENSE-APACHE)).
- Changes: none; indexed as Markdown.

## Not included

The benchmark datasets used by ragite (SciFact, FiQA and others) are not part of this demo: SciFact is licensed for noncommercial use only, and FiQA's license is unclear.
