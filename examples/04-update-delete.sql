-- Update and delete documents. Name a document by doc_id.
-- Run: sqlite3 < examples/04-update-delete.sql
SELECT load_extension('./libragite');
CREATE VIRTUAL TABLE notes USING ragite;

INSERT INTO notes(text, source) VALUES ('Indexes speed up lookups.', 'draft-1.txt');
INSERT INTO notes(text, source) VALUES ('Triggers run SQL when rows change.', 'draft-2.txt');

-- Changing only metadata (source, hash) recomputes nothing.
UPDATE notes SET source = 'indexes.txt' WHERE doc_id = 1;

-- Changing text or format re-chunks and re-embeds the document in the same transaction.
UPDATE notes
SET text = '# Indexes

An index speeds up lookups and ORDER BY.', format = 'text/markdown'
WHERE doc_id = 1;

SELECT doc_id, source, format FROM notes;
SELECT doc_id, heading_path, chunk FROM notes_chunks WHERE doc_id = 1;

-- Deleting a document removes its chunks, vectors and full-text rows.
DELETE FROM notes WHERE doc_id = 2;
SELECT count(*) AS documents, (SELECT count(*) FROM notes_chunks) AS chunks FROM notes;

-- A ROLLBACK undoes ragite writes like any other write.
BEGIN;
DELETE FROM notes WHERE doc_id = 1;
ROLLBACK;
SELECT doc_id, source FROM notes;
