-- Embeddings for your own tables: float32 BLOBs, 4 bytes per dimension (512 for the default model).
-- Run: sqlite3 < examples/06-embed.sql
SELECT load_extension('./libragite');
CREATE VIRTUAL TABLE notes USING ragite;

-- With the model of a ragite table. role is 'query' or 'passage'.
SELECT length(ragite_embed('notes', 'How do I copy a database?', 'query')) AS bytes;

-- With a model id directly; works without any ragite table.
SELECT length(ragite_embed_model(
  'potion-retrieval-32M@6fc8051fab2a1e0ee76689cf08c853792ac285e7',
  'Use VACUUM INTO to copy a database.', 'passage')) / 4 AS dimensions;

-- The functions are deterministic, so a generated column can store an embedding.
CREATE TABLE faq (
  question TEXT,
  embedding BLOB GENERATED ALWAYS AS (ragite_embed('notes', question, 'passage')) STORED
);
INSERT INTO faq(question) VALUES ('How big can a database be?');
SELECT question, length(embedding) AS bytes FROM faq;
