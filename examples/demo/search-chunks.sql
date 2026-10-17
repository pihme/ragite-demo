-- sqlite3 -readonly app/demo.db < examples/demo/search-chunks.sql
SELECT load_extension('./libragite');

-- The best passages, with their heading path inside the page.
SELECT source, heading_path, chunk, round(score, 5) AS score
FROM docs_chunks
WHERE docs_chunks MATCH 'How do I import a CSV file in the sqlite3 shell?'
LIMIT 5;

-- Only the Wikipedia articles: filter on the source URL.
SELECT source, chunk FROM docs_chunks
WHERE docs_chunks MATCH 'Which version control system hosts the SQLite code?' AND source LIKE 'https://en.wikipedia.org/%'
LIMIT 3;
