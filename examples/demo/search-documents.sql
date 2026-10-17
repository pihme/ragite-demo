-- Against the demo database, read-only:
--   sqlite3 -readonly app/demo.db < examples/demo/search-documents.sql
SELECT load_extension('./libragite');

-- The five best documents for a question, with title and URL from doc_info.
WITH hits AS MATERIALIZED (
  SELECT doc_id, score FROM docs WHERE docs MATCH 'How does SQLite make transactions atomic?'
)
SELECT i.title, i.url, round(hits.score, 5) AS score
FROM hits JOIN doc_info i ON i.doc_id = hits.doc_id
ORDER BY hits.score DESC
LIMIT 5;
