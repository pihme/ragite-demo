-- Insert one document in each accepted format and look at the chunks ragite cut.
-- Run: sqlite3 < examples/03-insert-formats.sql
SELECT load_extension('./libragite');
CREATE VIRTUAL TABLE notes USING ragite;

-- text/plain (also the default when format is omitted)
INSERT INTO notes(text, source, format)
VALUES ('SQLite stores the whole database in a single file.', 'plain.txt', 'text/plain');

-- text/markdown: headings become the heading path of the chunks below them
INSERT INTO notes(text, source, format)
VALUES ('# Backups

## Online backup

Use VACUUM INTO to write a copy of a live database.', 'backup.md', 'text/markdown');

-- text/html: script and style are dropped, h1-h6 build the heading path
INSERT INTO notes(text, source, format)
VALUES ('<h1>Journal modes</h1><p>WAL lets readers and a writer work at the same time.</p><script>ignored()</script>',
        'journal.html', 'text/html');

-- application/vnd.docling.document+json: a DoclingDocument from Docling (PDF, Office, ...)
INSERT INTO notes(text, source, format)
VALUES ('{"schema_name":"DoclingDocument",
          "texts":[{"self_ref":"#/texts/0","label":"title","text":"Release notes"},
                   {"self_ref":"#/texts/1","label":"text","text":"Version 3 adds strict tables."}],
          "body":{"children":[{"$ref":"#/texts/0"},{"$ref":"#/texts/1"}]}}',
        'notes.pdf', 'application/vnd.docling.document+json');

-- One row per document. hash defaults to the SHA-256 of the text.
SELECT doc_id, source, format, substr(hash, 1, 12) AS hash FROM notes;

-- One row per chunk, with its position in the source and the heading path.
-- meta_json is set only for Docling chunks (page, section, element).
SELECT rowid AS chunk_id, doc_id, source, start, "end", heading_path, meta_json, chunk
FROM notes_chunks;
