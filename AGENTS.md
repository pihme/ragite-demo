# AGENTS.md

This file is for the coding agent working in this repo. Read it at the start of a session.

## What this repo is

**ragite-demo** is a Datasette demo for the RAGite SQLite extension: it indexes the SQLite docs, a few Wikipedia articles and the RAGite docs into one SQLite file and offers a search page plus canned SQL queries. Spec and decisions: `SPEC.md`. User docs: `README.md`.

License: **MIT** (`LICENSE`). Copyright line: "ragite-demo contributors"; keep it that way.
MIT because it is an example for an open library: people copy demo code. The indexed data keeps its own licenses (`DATA_SOURCES.md`).

## How to work here

- Reference environment: `nix/reference-env` is Python 3.12, pip and GNU make. `nix/sqlite` adds the sqlite3 CLI. `nix/browsers` adds Chromium (`CHROME_PATH`), includes the other two, and puts Nix libstdc++ on `LD_LIBRARY_PATH` so pip wheels such as greenlet load. Run `nix develop ./nix/browsers -c make test`. Each `flake.lock` is committed; Dependabot updates it.
Stack: Python 3.10+ (build script uses the standard library only), Datasette 0.65.5, RAGite release `libragite.so` (Linux x86-64).

- `data/sources.json`: every input, pinned (RAGite release and model by SHA-256 and id, SQLite doc archive by SHA-256, Wikipedia by revision id, RAGite docs by commit).
- `scripts/build-demo-db`: downloads, cleans HTML, builds `app/demo.db` (tables `docs` via RAGite, `doc_info`, `build_info`). `scripts/smoke`: HTTP checks against a running server.
- `app/`: Datasette configuration directory (`metadata.yml` canned queries, `settings.json`, `templates/pages/search.html`, `static/`).
- `examples/`: runnable SQL for RAGite's public interface (scratch database and read-only on `demo.db`; the write canned queries `create_table` and `insert_document` are the only writes to `demo.db`, and tests run them on a copy); `scripts/run-examples` runs them in the sqlite3 shell.
- `tests/`: Datasette test-client checks, `test_examples.py` (`test_demo.py`) and the Playwright screenshot script used in CI.

Invariants: no data, `demo.db` or `libragite.so` in git; only freely licensed data, with attribution in `DATA_SOURCES.md` and `doc_info`; no CDN or external service at run time; use only ragite's public SQL interface (hybrid `MATCH` on `docs` and `docs_chunks`, never its storage tables, SPEC D2); heavy work runs in CI.

- Tests: `make test` must pass before anything lands on `main`. Tests stay offline: no real accounts, tokens or live services.
- Releases: release-please (`release-please-config.json`, `.release-please-manifest.json`, version file `version.txt`, `CHANGELOG.md`). CI uploads `demo.db` as an artifact on every run except release pull requests; each release also attaches it.

## Shared rules

### Commits and changes

- [Conventional Commits](https://www.conventionalcommits.org/) for every commit: `feat:`, `fix:`, `perf:`, `docs:`, `test:`, `refactor:`, `chore:`, `ci:`, `build:`, optional scope, `!` for breaking changes.
- **Trivial changes go straight to `main`:** typos, small docs fixes, obvious small bugs, housekeeping. Keep commits small and focused; pull before you commit, CI pushes release commits to `main`.
- **Non-trivial findings become GitHub issues** (with the matching issue form): bugs you do not fix right away, design questions, anything that needs a decision. Do not hide them in a commit.
- **Never force-push**, never rewrite pushed history, never delete branches or tags.
- **No comments, reviews, label changes, closes or merges on other people's issues and PRs** unless the maintainer asked for it in the session. Exception: Dependabot PRs (see below). Opening issues for your own findings and closing them with your own commits (`Closes #n`) is fine.
- **Never write the skip-CI token** (the word `skip` and `ci` in square brackets, or any of its variants) in a commit message, not even quoted or explained: GitHub then skips CI for that push and no release is cut. No tool in this repo needs it: release-please commits through its release pull request.

### Versions and releases

- **Releases use release-please, not `release.py`** (the Python counterpart of RAGite's release-plz setup). There is no `.github/release.json`. After CI passes on a push to `main`, the `release` job opens or updates a release pull request that bumps `version.txt` and `.release-please-manifest.json` and adds the new section to `CHANGELOG.md`. Merging that pull request tags `ragite-demo/vX.Y.Z`, creates the GitHub Release named `ragite-demo X.Y.Z` and attaches the `demo.db` built and tested in that run, `DATA_SOURCES.md`, `LICENSE` and `THIRD_PARTY_NOTICES.md`. On the release pull request itself (`release-please--*` branch) CI runs only `release-pr-check` (`scripts/check-release-pr`): the branch may change only those three files, and they must agree. The full demo job runs again on the push after the merge.
- `feat:` bumps minor, `fix:`/`perf:` patch, a breaking change (`!` or a `BREAKING CHANGE:` footer) major. `docs:`, `test:`, `refactor:`, `chore:`, `ci:`, `build:` never bump and stay out of the changelog. Commit titles become the changelog lines verbatim.
- **Choose a version** (only when the maintainer decided it): a commit with the footer `Release-As: X.Y.Z`, e.g. `git commit --allow-empty -m "chore: release 2.0" -m "Release-As: 2.0.0"`. **Squash merges keep only the commit messages, not the pull request body**, so the footer must be in a commit message of the branch; a `Release-As:` line in the PR description is ignored.
- Never tag, bump `version.txt` or create releases by hand, and never edit published release notes or past `CHANGELOG.md` sections.

### Dependabot

- Commit prefixes (set in `.github/dependabot.yml`): runtime dependencies and shipped Docker base images `fix(deps):` (patch release), dev dependencies `chore(deps-dev):`, GitHub Actions `ci(deps):`, images that are not shipped (examples, tests) `chore(deps):`.
- **Never turn a dependency update into `feat!:`** or reword its title. A major dependency update is still `fix(deps)` / `chore(deps-dev)`. If it forces a breaking change on users (for example a new minimum runtime), that is a separate, deliberate commit after the maintainer decides.
- **Merge Dependabot PRs when CI is green** (squash, keep the Dependabot title). If one conflicts, comment `@dependabot rebase`. If CI is red and the fix is not obvious, leave the PR open and open an issue.

### Third-party notices

- **Keep `THIRD_PARTY_NOTICES.md` current** (model: git-warden's). It lists everything the project contains, bundles or runs from others: compiled-in or installed dependencies with name, version and license taken from the real dependency metadata (lockfile, `go.mod`, the installed package's `package.json`/LICENSE), the license texts and NOTICE files they ask for, and external programs or images it runs but does not include. Never guess a license. Update it in the same commit as any dependency change (Dependabot included).
- **Ship it with every distributed artifact:** list it in `package.json` `files`, attach it to GitHub Releases next to `LICENSE` (`.github/release.json` assets), and copy it into any image a Dockerfile builds. Link it from the README's license section.
- **The "How this project is built" README section** (the maintainer's verbatim text, `<project>` replaced by the project name) stays in the README, just before the license section; do not reword it. New repos get it from the presets README template (`template/README.md`, copied by `bootstrap.sh`); fill its TODOs, keep the section.

### Secrets

- Never commit, print, log or paste tokens, API keys, credentials, `.env` files, session files or real service responses: not in code, tests, fixtures, issues, PRs or commit messages. Use synthetic fixtures.
- Security problems are reported privately (`SECURITY.md`). Do not discuss an unfixed vulnerability in a public issue.

### Contributions

- Outside pull requests are welcome under MIT (see `CONTRIBUTING.md` and `.github/pull_request_template.md`). The maintainer reviews and merges them (squash, Conventional Commit title).
- `CONTRIBUTING.md` holds **only content for outside people**: license, how to report, how to build and test. Internal working rules (this file) never go there.

### Website

- Site: none yet. When one is added, it is generated onto the `gh-pages` branch from outside this repo. Do not edit `gh-pages` by hand and never merge it into `main`.
- **Repo description = site tagline.** The hero tagline is the live GitHub repo description; change them together (the generator checks it).
- **Current status:** two link-free prose paragraphs, *what works* and *limits* (limits include the open issues, described in words, never as numbers or links). About 90–130 words each, plain English for someone who does not know the project, acronyms explained or avoided. No dates, SHAs or "as of" in the prose: metadata appears once, in the line `Last updated <date> · main@<sha>`. Only state what tests, CI, releases or the code show. The covered issues must match the open issues exactly.
- **Chronicles:** one paragraph per month, newest first, about 60–90 words, only the main milestones. Written as a modest medieval chronicler: the author is always *a humble brother* (or a monk of the order), never "the maker". Light archaic touch, plain verbs, no clock times, minimal dates, no superlatives or flourishes, facts only (never mention things that do not exist yet), one to three links to releases, commits or compares.
- **Jigsaw:** the project family lives in one central `family.json`. Each relation is described truthfully from both sides; a new project, a changed description or a changed relation means rebuilding all sites and the profile README.

## Do not invent

- No own web framework or frontend build: Datasette plus one page template and plain JavaScript.
- No benchmark datasets (SciFact, FiQA): license.
- No LLM answer generation: RAGite retrieves, it does not generate.
- See `SPEC.md` for the decisions.

## Agent skills

### Issue tracker

GitHub issues in `pihme/ragite-demo`, via `gh`. See `docs/agents/issue-tracker.md`.

### Triage labels

Labels: `needs-triage`, `needs-info`, `needs-input`, `ready-for-maintainer`, `ready-for-development`, `ready-for-qa`, `ready-for-human`, `wontfix`, plus `bug` / `enhancement`. `ready-for-maintainer` is for Maintainer (website, docs fixes, smaller changes), `ready-for-development` is for Developer (larger feature and code work), and `ready-for-qa` is for QA. Team roles, labels, handover, merging and release mode: `docs/agents/team.md` (same in every repo; change it in presets first). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: decisions in `SPEC.md`, optional root `GLOSSARY.md`. See `docs/agents/domain.md`.
