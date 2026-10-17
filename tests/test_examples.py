"""Run every examples/*.sql file statement by statement and check that each SELECT returns rows.

Scratch examples (examples/*.sql) run on an in-memory database; demo examples
(examples/demo/*.sql) run read-only against app/demo.db. CI also runs them through the
sqlite3 shell (scripts/run-examples), the way the README shows.
"""

import os
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LIB = os.environ.get("RAGITE_LIB") or str(ROOT / "libragite.so")
LIB_ARG = str(Path(LIB).resolve())
LIB_ARG = LIB_ARG[: -len(".so")] if LIB_ARG.endswith(".so") else LIB_ARG

SCRATCH = sorted((ROOT / "examples").glob("*.sql"))
DEMO = sorted((ROOT / "examples" / "demo").glob("*.sql"))


def statements(sql: str):
    buf = ""
    for line in sql.splitlines(keepends=True):
        buf += line
        if sqlite3.complete_statement(buf):
            stmt = "\n".join(l for l in buf.splitlines() if not l.lstrip().startswith("--")).strip()
            if stmt:
                yield stmt
            buf = ""
    assert not buf.strip() or all(l.lstrip().startswith("--") for l in buf.splitlines() if l.strip()), f"incomplete statement: {buf!r}"


def run(path: Path, con: sqlite3.Connection) -> int:
    con.enable_load_extension(True)
    con.isolation_level = None  # the examples manage their own transactions
    selects = 0
    for stmt in statements(path.read_text()):
        stmt = stmt.replace("load_extension('./libragite')", f"load_extension('{LIB_ARG}')")
        rows = con.execute(stmt).fetchall()
        head = stmt.lstrip("( \n").upper()
        if head.startswith(("SELECT", "WITH")) and "LOAD_EXTENSION" not in head:
            assert rows, f"{path.name}: no rows from\n{stmt}"
            selects += 1
    return selects


def test_examples_exist():
    assert len(SCRATCH) >= 6 and len(DEMO) >= 4


@pytest.mark.parametrize("path", SCRATCH, ids=lambda p: p.name)
def test_scratch_example(path):
    assert run(path, sqlite3.connect(":memory:")) > 0


@pytest.mark.parametrize("path", DEMO, ids=lambda p: p.name)
def test_demo_example(path):
    db = ROOT / "app" / "demo.db"
    assert db.exists(), "build app/demo.db first: scripts/build-demo-db"
    assert run(path, sqlite3.connect(f"file:{db}?mode=ro", uri=True)) > 0


def test_examples_use_only_the_public_interface():
    for path in SCRATCH + DEMO:
        text = path.read_text()
        for internal in ("_vec", "_fts", "_chunk_rows", "_documents", "_model"):
            assert f"docs{internal}" not in text and f"notes{internal}" not in text, (path.name, internal)
