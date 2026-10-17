-- The model built into this libragite.so. Works before any ragite table exists.
-- Run: sqlite3 < examples/01-default-model.sql   (from the repository root)
SELECT load_extension('./libragite');

SELECT name, technical_id FROM ragite_default_model();

-- A version 1 build contains exactly one model.
SELECT name, technical_id FROM ragite_list_models();
