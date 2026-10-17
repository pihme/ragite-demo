# Contributing

ragite-demo is open source under the [MIT License](LICENSE).

## Issues

Issues, bug reports and ideas are very welcome. Pick the matching [issue form](https://github.com/pihme/ragite-demo/issues/new/choose) (bug report, feature request, documentation, question). A good report names the ragite-demo version or commit, your OS and runtime versions, what you ran, what you expected and what happened.

## Pull requests

Pull requests are welcome; contributions are accepted under the [MIT License](LICENSE). For anything bigger than a small fix, please open an issue first so we can agree on the change. Keep a pull request to one change, fill in the [pull request template](.github/pull_request_template.md), give it a [Conventional Commit](https://www.conventionalcommits.org/) title (`fix: …`, `feat: …`, `docs: …`; it becomes the squash commit and decides the next release), and make sure `make test` passes.

## Security and secrets

The tracker is public. Never paste tokens, keys, credentials or real service responses into an issue or pull request. Please report vulnerabilities privately, as described in [SECURITY.md](SECURITY.md).

## Build and test locally

Linux x86-64 and Python 3.10+ (see the README). The build downloads `libragite.so` (~135 MB) and the pinned sources in `data/sources.json`; the tests need that build but no accounts or tokens.

```bash
pip install -r requirements-dev.txt
make demo-db test
```

New or changed data must be freely licensed and listed in `data/sources.json` and `DATA_SOURCES.md`.
