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
        browser.close()


if __name__ == "__main__":
    main()
