# Third-party software and data

ragite-demo itself is licensed under [MIT](LICENSE). The only third-party files in this repository are the web fonts listed first. Everything else below is downloaded or installed when you build or run the demo, and keeps its own license.

## Fonts (included)

Latin subsets in WOFF2 format in `app/static/fonts/`, served by the demo itself (no font CDN). Each is licensed under the [SIL Open Font License 1.1](https://openfontlicense.org/); the full licence text with the copyright line sits next to the font file. No Reserved Font Name is declared.

| Font | Version | File | Copyright | License text |
| --- | --- | --- | --- | --- |
| [Space Grotesk](https://github.com/floriankarsten/space-grotesk) (variable, weight 300–700) | 2.000 | `space-grotesk.woff2` | Copyright 2020 The Space Grotesk Project Authors | [`OFL-space-grotesk.txt`](app/static/fonts/OFL-space-grotesk.txt) |
| [Geist](https://github.com/vercel/geist-font) (variable, weight 100–900) | 1.800 | `geist.woff2` | Copyright 2024 The Geist Project Authors | [`OFL-geist.txt`](app/static/fonts/OFL-geist.txt) |
| [Geist Mono](https://github.com/vercel/geist-font) (variable, weight 100–900) | 1.701 | `geist-mono.woff2` | Copyright 2024 The Geist Project Authors | [`OFL-geist-mono.txt`](app/static/fonts/OFL-geist-mono.txt) |

## Data indexed into demo.db (downloaded, not in the repository)

The `demo.db` attached to each GitHub Release contains this data; `DATA_SOURCES.md` is attached next to it. See [DATA_SOURCES.md](DATA_SOURCES.md) for the exact sources, revisions, changes and attribution.

| Data | License |
| --- | --- |
| SQLite documentation 3.54.1 (subset) | Public domain |
| Wikipedia articles (20, pinned revisions) | CC BY-SA 4.0 |
| RAGite README, SPEC, GLOSSARY, user guide, tinkering guide | MIT OR Apache-2.0 |

## Programs used (run, not included)

| Name | Version | License | Used for |
| --- | --- | --- | --- |
| [RAGite](https://github.com/pihme/ragite) `libragite.so` | 1.1.2 | MIT OR Apache-2.0 | SQLite extension that chunks, embeds and searches. Downloaded from the GitHub release and checked by SHA-256. It bundles SQLite, sqlite-vec, the potion-retrieval-32M model (MIT) and other components; their notices are in the release's [THIRD_PARTY_NOTICES.md](https://github.com/pihme/ragite/releases/download/ragite/v1.1.2/THIRD_PARTY_NOTICES.md). |
| [Datasette](https://datasette.io/) | 0.65.5 | Apache-2.0 | Web interface and JSON API (`requirements.txt`). |
| [Python](https://www.python.org/) | 3.10+ | PSF-2.0 | Build script (standard library only) and tests. |

## Development and CI only

| Name | Version | License |
| --- | --- | --- |
| pytest | 9.2.0 | MIT |
| pytest-asyncio | 1.4.1 | Apache-2.0 |
| PyYAML | 6.0.3 | MIT |
| coverage.py | 7.17.0 | Apache-2.0 |
| sqlite3 shell (Ubuntu package, runs the examples) | distribution version | Public domain |
| Playwright for Python (and the Chromium it installs) | 1.64.1 | Apache-2.0 (Chromium: BSD-3-Clause and others) |
| GitHub Action `SonarSource/sonarqube-scan-action` (CI only, runs SonarScanner CLI 8.1.0.6389) | 8.3.0 | LGPL-3.0 |
