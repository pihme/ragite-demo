"""Unit tests for the HTML cleaning in scripts/build-demo-db (no demo.db or libragite.so needed)."""

import importlib.machinery
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_loader = importlib.machinery.SourceFileLoader("build_demo_db", str(ROOT / "scripts" / "build-demo-db"))
_spec = importlib.util.spec_from_loader("build_demo_db", _loader)
build = importlib.util.module_from_spec(_spec)
_loader.exec_module(build)


def clean(raw: str) -> str:
    return build.clean_html(raw)[0]


def test_unicode_spaces_become_plain_spaces():
    assert clean("<h3>&nbsp;WAL Mode&nbsp;</h3><p>a&emsp;b</p>") == "<h3> WAL Mode </h3><p>a b</p>"


def test_table_row_is_one_paragraph():
    out = clean("<table><tr><td><b>.mode box</b></td><td>Show the current output mode</td></tr>"
                "<tr><th>Option</th><th>Meaning</th></tr></table>")
    assert out == ("<table><tr><p><b>.mode box</b> | Show the current output mode</p></tr>"
                   "<tr><p>Option | Meaning</p></tr></table>")


def test_row_with_a_block_inside_is_left_alone():
    raw = "<table><tr><td><p>One</p></td><td>Two</td></tr></table>"
    assert clean(raw) == raw


def test_empty_cells_are_dropped_and_an_empty_row_disappears():
    assert clean("<table><tr><td>pgno</td><td>&nbsp;</td><td>page number</td></tr><tr><td> </td></tr></table>") == (
        "<table><tr><p>pgno | page number</p></tr></table>")


def test_short_list_is_one_paragraph():
    assert clean("<ul><li><a>Full-featured SQL</a></li><li>Single-file database</li></ul>") == (
        "<p><a>Full-featured SQL</a>; Single-file database</p>")


def test_list_with_a_long_item_or_a_nested_list_is_left_alone():
    long_item = "x" * (build.SHORT_ITEM + 1)
    raw = f"<ul><li>short</li><li>{long_item}</li></ul>"
    assert clean(raw) == raw
    nested = "<ul><li>a</li><li>b<ul><li>c</li><li>d</li></ul></li></ul>"
    assert clean(nested) == "<ul><li>a</li><li>b<p>c; d</p></li></ul>"
