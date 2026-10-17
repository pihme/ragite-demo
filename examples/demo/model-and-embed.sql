-- sqlite3 -readonly app/demo.db < examples/demo/model-and-embed.sql
SELECT load_extension('./libragite');

-- The model of the extension and the model the docs table was built with.
SELECT name, technical_id, ragite_table_model('docs') = technical_id AS same_model
FROM ragite_default_model();

-- A query embedding with the table's model: 512 float32 values.
SELECT length(ragite_embed('docs', 'write-ahead logging', 'query')) / 4 AS dimensions,
       hex(substr(ragite_embed('docs', 'write-ahead logging', 'query'), 1, 8)) AS first_bytes;
