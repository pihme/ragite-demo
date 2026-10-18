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
| Retrieval-augmented generation | en | [1377227095](https://en.wikipedia.org/w/index.php?title=Retrieval-augmented_generation&oldid=1377227095) | [history](https://en.wikipedia.org/w/index.php?title=Retrieval-augmented_generation&action=history) |
| Retrieval-Augmented Generation | de | [270780895](https://de.wikipedia.org/w/index.php?title=Retrieval-Augmented_Generation&oldid=270780895) | [history](https://de.wikipedia.org/w/index.php?title=Retrieval-Augmented_Generation&action=history) |
| Large language model | en | [1380435450](https://en.wikipedia.org/w/index.php?title=Large_language_model&oldid=1380435450) | [history](https://en.wikipedia.org/w/index.php?title=Large_language_model&action=history) |
| Information retrieval | en | [1375036430](https://en.wikipedia.org/w/index.php?title=Information_retrieval&oldid=1375036430) | [history](https://en.wikipedia.org/w/index.php?title=Information_retrieval&action=history) |
| Semantic search | en | [1376135669](https://en.wikipedia.org/w/index.php?title=Semantic_search&oldid=1376135669) | [history](https://en.wikipedia.org/w/index.php?title=Semantic_search&action=history) |
| Full-text search | en | [1364195936](https://en.wikipedia.org/w/index.php?title=Full-text_search&oldid=1364195936) | [history](https://en.wikipedia.org/w/index.php?title=Full-text_search&action=history) |
| Inverted index | en | [1354610034](https://en.wikipedia.org/w/index.php?title=Inverted_index&oldid=1354610034) | [history](https://en.wikipedia.org/w/index.php?title=Inverted_index&action=history) |
| Okapi BM25 | en | [1372301996](https://en.wikipedia.org/w/index.php?title=Okapi_BM25&oldid=1372301996) | [history](https://en.wikipedia.org/w/index.php?title=Okapi_BM25&action=history) |
| Tf–idf | en | [1380707612](https://en.wikipedia.org/w/index.php?title=Tf%E2%80%93idf&oldid=1380707612) | [history](https://en.wikipedia.org/w/index.php?title=Tf%E2%80%93idf&action=history) |
| Word embedding | en | [1374850731](https://en.wikipedia.org/w/index.php?title=Word_embedding&oldid=1374850731) | [history](https://en.wikipedia.org/w/index.php?title=Word_embedding&action=history) |
| Sentence embedding | en | [1380359878](https://en.wikipedia.org/w/index.php?title=Sentence_embedding&oldid=1380359878) | [history](https://en.wikipedia.org/w/index.php?title=Sentence_embedding&action=history) |
| Cosine similarity | en | [1378075969](https://en.wikipedia.org/w/index.php?title=Cosine_similarity&oldid=1378075969) | [history](https://en.wikipedia.org/w/index.php?title=Cosine_similarity&action=history) |
| Vector database | en | [1374243120](https://en.wikipedia.org/w/index.php?title=Vector_database&oldid=1374243120) | [history](https://en.wikipedia.org/w/index.php?title=Vector_database&action=history) |
| Nearest neighbor search | en | [1372424608](https://en.wikipedia.org/w/index.php?title=Nearest_neighbor_search&oldid=1372424608) | [history](https://en.wikipedia.org/w/index.php?title=Nearest_neighbor_search&action=history) |
| Hierarchical navigable small world | en | [1369131893](https://en.wikipedia.org/w/index.php?title=Hierarchical_navigable_small_world&oldid=1369131893) | [history](https://en.wikipedia.org/w/index.php?title=Hierarchical_navigable_small_world&action=history) |

- Retrieved through the MediaWiki API (`action=parse&oldid=<revision>`), so the text is the pinned revision. Templates are expanded by Wikipedia at download time, so the rendered markup may drift slightly when a template changes later.
- Changes: infoboxes, images, math formulas, navigation boxes, edit links, footnote markers and the sections that only hold links or citations (for example "See also", "References", "External links"; "Weblinks", "Einzelnachweise" in German) are removed. Table rows and lists of short items are joined into paragraphs and no-break spaces become plain spaces, as for the SQLite documentation. The remaining text is unchanged and is split into chunks by RAGite. These changes are an adaptation under CC BY-SA 4.0; the adapted text in `demo.db` is under the same license.
- Images are not included.

## 3. RAGite documentation (MIT OR Apache-2.0)

- Files: `README.md`, `SPEC.md`, `GLOSSARY.md`, the user guide `docs/guide.md` and the tinkering guide `docs/tinkering.md` from [pihme/ragite](https://github.com/pihme/ragite) at commit [`8d9595c`](https://github.com/pihme/ragite/tree/8d9595cacdb4f31f5213b3499b6fa6ac1878c948), the commit tagged `ragite/v1.0.0`, the RAGite release the demo runs, so the files describe that release's behaviour.
- License: `MIT OR Apache-2.0`, Copyright (c) 2026 ragite contributors ([LICENSE-MIT](https://github.com/pihme/ragite/blob/8d9595cacdb4f31f5213b3499b6fa6ac1878c948/LICENSE-MIT), [LICENSE-APACHE](https://github.com/pihme/ragite/blob/8d9595cacdb4f31f5213b3499b6fa6ac1878c948/LICENSE-APACHE)).
- Changes: none; indexed as Markdown.

## Not included

The benchmark datasets used by RAGite (SciFact, FiQA and others) are not part of this demo: SciFact is licensed for noncommercial use only, and FiQA's license is unclear.
