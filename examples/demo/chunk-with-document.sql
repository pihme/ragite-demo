-- sqlite3 -readonly app/demo.db < examples/demo/chunk-with-document.sql
SELECT load_extension('./libragite');

-- A chunk joined to its document (docs) and its attribution (doc_info).
WITH hits AS MATERIALIZED (
  SELECT rowid AS chunk_id, doc_id, start, "end", chunk, score
  FROM docs_chunks
  WHERE docs_chunks MATCH 'What is a B-tree?'
  LIMIT 3
)
SELECT i.title, i.license, i.revision, d.format, hits.start, hits."end", hits.chunk
FROM hits
JOIN docs d ON d.doc_id = hits.doc_id
JOIN doc_info i ON i.doc_id = hits.doc_id
ORDER BY hits.score DESC;

-- All chunks of one document, in order (no MATCH: score is null).
SELECT rowid AS chunk_id, heading_path, substr(chunk, 1, 80) AS chunk
FROM docs_chunks
WHERE doc_id = (SELECT doc_id FROM doc_info WHERE url = 'https://sqlite.org/backup.html')
LIMIT 10;
