# Third-party software and data

ragite-demo itself is licensed under [MIT](LICENSE). This repository contains no third-party code or data: everything below is downloaded or installed when you build or run the demo, and keeps its own license.

## Data indexed into demo.db (downloaded, not included)

See [DATA_SOURCES.md](DATA_SOURCES.md) for the exact sources, revisions, changes and attribution.

| Data | License |
| --- | --- |
| SQLite documentation 3.54.1 (subset) | Public domain |
| Wikipedia articles (5, pinned revisions) | CC BY-SA 4.0 |
| ragite README, SPEC, GLOSSARY | MIT OR Apache-2.0 |

## Programs used (run, not included)

| Name | Version | License | Used for |
| --- | --- | --- | --- |
| [ragite](https://github.com/pihme/ragite) `libragite.so` | 0.3.0 | MIT OR Apache-2.0 | SQLite extension that chunks, embeds and searches. Downloaded from the GitHub release and checked by SHA-256. It bundles SQLite, sqlite-vec, the potion-retrieval-32M model (MIT) and other components; their notices are in the release's [THIRD_PARTY_NOTICES.md](https://github.com/pihme/ragite/releases/download/ragite/v0.3.0/THIRD_PARTY_NOTICES.md). |
| [Datasette](https://datasette.io/) | 0.65.5 | Apache-2.0 | Web interface and JSON API (`requirements.txt`). |
| [Python](https://www.python.org/) | 3.10+ | PSF-2.0 | Build script (standard library only) and tests. |

## Development and CI only

| Name | Version | License |
| --- | --- | --- |
| pytest | 8.4.2 | MIT |
| pytest-asyncio | 1.2.0 | Apache-2.0 |
| PyYAML | 6.0.3 | MIT |
| Playwright for Python (and the Chromium it installs) | 1.55.0 | Apache-2.0 (Chromium: BSD-3-Clause and others) |
