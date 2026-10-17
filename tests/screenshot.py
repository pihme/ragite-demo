"""Take screenshots of the search page with Playwright (Chromium).

    python tests/screenshot.py http://127.0.0.1:8001 screenshots/

Fails when the page shows no result cards, so it doubles as a browser smoke test.
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SHOTS = [
    ("search.png", "/search?q=How+do+I+copy+a+database+while+it+is+in+use%3F"),
    ("search-wikipedia.png", "/search?q=What+is+a+B-tree%3F&collection=wikipedia"),
    # A NUL byte in the URL must still give results, not "Search failed: unterminated string".
    ("search-nul.png", "/search?q=How+does+WAL%00mode+work%3F"),
]


def main() -> None:
    base, out = sys.argv[1].rstrip("/"), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        # CHROME_PATH lets a machine without Playwright's own browsers use an installed Chrome.
        browser = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH") or None)
        page = browser.new_page(viewport={"width": 1100, "height": 1400})
        for name, path in SHOTS:
            page.goto(base + path)
            page.wait_for_selector(".rs-card", timeout=30_000)
            cards = page.locator(".rs-card").count()
            page.screenshot(path=str(out / name), full_page=False)
            print(f"{name}: {cards} cards")
            if cards == 0:
                sys.exit(f"{path}: no result cards")
        check_page_helpers(page)
        check_filter_hint(page, base, out)
        browser.close()


# (function, arguments, expected result) for window.ragiteSearch on the search page.
HELPER_CASES = [
    # Highlighting works on the raw text, so a query word never matches inside an escaped entity.
    ("highlight", ['Tom & "Jerry"', "amp quot"], "Tom &amp; &quot;Jerry&quot;"),
    ("highlight", ["amp & <amp>", "amp"], "<mark>amp</mark> &amp; &lt;<mark>amp</mark>&gt;"),
    ("highlight", ["WAL mode in wal.html", "wal"], "<mark>WAL</mark> mode in <mark>wal</mark>.html"),
    # A term must start a word and marks the whole word, never a piece of an identifier.
    ("highlight", ["auto_vacuum mode", "vacuum"], "<mark>auto_vacuum</mark> mode"),
    ("highlight", ["xvacuum", "vacuum"], "xvacuum"),
    # Neighbouring hits separated only by a space or hyphen become one mark.
    ("highlight", ["Write-Ahead Logging", "write ahead logging"], "<mark>Write-Ahead Logging</mark>"),
    # Context under a short hit: one paragraph per chunk, highlighted and escaped like the hit.
    ("contextHtml", ['["The VACUUM <command>"]', "vacuum"],
     '<div class="rs-card-context" title="The text that follows this passage in the document">'
     '<p class="rs-card-text">The <mark>VACUUM</mark> &lt;command&gt;</p></div>'),
    ("contextHtml", ["[]", "vacuum"], ""),
    # The source-filter hint (pihme/ragite#49): none without a filter, a warning when few rows remain.
    ("filterHintHtml", ["", 0], ""),
    ("filterHintHtml", ["ragite-docs", 0], None),
    # A NUL byte (or another control character) in the query becomes a space.
    ("cleanQuery", ["WAL\u0000mode\u0007 "], "WAL mode"),
]


def check_page_helpers(page) -> None:
    for fn, args, want in HELPER_CASES:
        got = page.evaluate(f"(args) => window.ragiteSearch.{fn}(...args)", args)
        if want is None:  # only the gist is checked
            if "No passages" not in got or "ragite/issues/49" not in got:
                sys.exit(f"{fn}{tuple(args)!r}: unexpected {got!r}")
            continue
        if got != want:
            sys.exit(f"{fn}{tuple(args)!r}: expected {want!r}, got {got!r}")
    print(f"page helpers: {len(HELPER_CASES)} checks ok")


def check_filter_hint(page, base: str, out: Path) -> None:
    """'virtual table' limited to the ragite docs returns no rows (pihme/ragite#49); the page must say why."""
    page.goto(base + "/search?q=virtual+table&collection=ragite-docs")
    page.wait_for_selector("#rs-filter-hint:not([hidden])", timeout=30_000)
    hint = page.inner_text("#rs-filter-hint")
    page.screenshot(path=str(out / "search-filter-hint.png"), full_page=False)
    if "ragite#49" not in hint:
        sys.exit(f"source filter hint missing: {hint!r}")
    print("filter hint: ok")


if __name__ == "__main__":
    main()

