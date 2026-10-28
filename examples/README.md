# SQL examples

Runnable examples of RAGite's public SQL interface (v1.1.2, the version 1 interface). They use only the Document table, its `_chunks` companion and the `ragite_*` functions, never RAGite's storage tables. Run them from the repository root, next to `libragite.so`; CI runs every file (`scripts/run-examples` and `tests/test_examples.py`).

## On a new, empty database

```bash
sqlite3 < examples/03-insert-formats.sql
```

| File | Shows |
| --- | --- |
| [01-default-model.sql](01-default-model.sql) | `ragite_default_model()`, `ragite_list_models()` |
| [02-create-table.sql](02-create-table.sql) | `CREATE VIRTUAL TABLE ... USING ragite`, with and without a pinned model; `ragite_table_model()`; `DROP TABLE` |
| [03-insert-formats.sql](03-insert-formats.sql) | `INSERT` in each format: `text/plain`, `text/markdown`, `text/html`, `application/vnd.docling.document+json`; the chunks with `start`, `end`, `heading_path`, `meta_json` |
| [04-update-delete.sql](04-update-delete.sql) | `UPDATE` of metadata only and of text and format (re-chunks), `DELETE`, `ROLLBACK` |
| [05-search.sql](05-search.sql) | `MATCH` on documents and on chunks, with a filter, and a chunk joined to its document |
| [06-embed.sql](06-embed.sql) | `ragite_embed()`, `ragite_embed_model()`, an embedding in a generated column |

## On the demo database (read-only)

```bash
sqlite3 -readonly app/demo.db < examples/demo/search-chunks.sql
```

| File | Shows |
| --- | --- |
| [demo/search-documents.sql](demo/search-documents.sql) | Best documents for a question, with title and URL |
| [demo/search-chunks.sql](demo/search-chunks.sql) | Best passages, and passages from one source only |
| [demo/chunk-with-document.sql](demo/chunk-with-document.sql) | A chunk joined to its document and attribution; all chunks of one document |
| [demo/model-and-embed.sql](demo/model-and-embed.sql) | The extension's model, the table's model, a query embedding |

The read-only ones are also canned queries in Datasette (`search`, `search_documents`, `chunks_with_document`, `document_chunks`, `model`, `embed`). Two writable canned queries, `create_table` and `insert_document`, create the ragite table `notes` in `demo.db` and add documents to it (run `create_table` first; both are repeatable). They change your local `demo.db`; to get the original back, download `demo.db` again from the [release](https://github.com/pihme/ragite-demo/releases) or rebuild it with `scripts/build-demo-db`. `UPDATE` and `DELETE` stay in the files above.

In Python, load the extension with `con.enable_load_extension(True)` and `con.load_extension('./libragite')`; the SQL is the same.
