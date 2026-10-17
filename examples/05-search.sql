-- Hybrid search (vector similarity + BM25, fused by Reciprocal Rank Fusion) with MATCH.
-- Run: sqlite3 < examples/05-search.sql
SELECT load_extension('./libragite');
CREATE VIRTUAL TABLE notes USING ragite;

INSERT INTO notes(text, source, format) VALUES
  ('# Backups

Use VACUUM INTO or the online backup API to copy a live database.', 'backup.md', 'text/markdown'),
  ('# Write-ahead log

In WAL mode, readers do not block the writer.', 'wal.md', 'text/markdown'),
  ('# JSON

The json_extract function reads a value out of a JSON document.', 'json.md', 'text/markdown');

-- Search documents: one row per document, ranked by its best chunk.
SELECT doc_id, source, score FROM notes
WHERE notes MATCH 'How do I copy a database that is in use?'
LIMIT 3;

-- Search chunks: one row per chunk, best first.
SELECT chunk, source, heading_path, score FROM notes_chunks
WHERE notes_chunks MATCH 'readers and writers at the same time'
LIMIT 3;

-- Combine MATCH with ordinary filters.
SELECT chunk, score FROM notes_chunks
WHERE notes_chunks MATCH 'copy a database' AND source = 'backup.md';

-- Join a chunk to its document: the full text, format and position of the match.
WITH hits AS MATERIALIZED (
  SELECT rowid AS chunk_id, doc_id, start, "end", chunk, score
  FROM notes_chunks
  WHERE notes_chunks MATCH 'extract a value from JSON'
  LIMIT 1
)
SELECT d.source, d.format, hits.start, hits."end", hits.chunk,
       substr(d.text, hits.start + 1, hits."end" - hits.start) = hits.chunk AS offsets_match
FROM hits JOIN notes d ON d.doc_id = hits.doc_id;
