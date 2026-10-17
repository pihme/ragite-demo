-- Create ragite tables. Each one also creates the read-only companion <name>_chunks.
-- Run: sqlite3 < examples/02-create-table.sql
SELECT load_extension('./libragite');

-- Without model=..., the table uses the build's default model.
CREATE VIRTUAL TABLE notes USING ragite;

-- Pin the model explicitly: the technical id from ragite_default_model().
CREATE VIRTUAL TABLE manuals USING ragite(model='potion-retrieval-32M@6fc8051fab2a1e0ee76689cf08c853792ac285e7');

-- The model each table is bound to.
SELECT 'notes' AS tbl, ragite_table_model('notes') AS model
UNION ALL
SELECT 'manuals', ragite_table_model('manuals');

-- Dropping the document table also drops its companion and storage.
DROP TABLE manuals;
SELECT name FROM sqlite_master WHERE name = 'notes_chunks';
