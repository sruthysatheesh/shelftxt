# Working on ShelfTxt

ShelfTxt is a solo-maintained project. Contributions and forks are welcome, but expect a lightweight review pace. Small, focused changes beat large rewrites every time.

---

## Setup

From the repo root:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.api:app --reload
```

Frontend (optional):

```bash
cd frontend && npm install && npm run dev
```

Full details: [docs/development.md](docs/development.md)

Run Python commands from the **repo root** so `backend` resolves as a package.

---

## Architecture docs

Before moving code around, skim:

| Doc | Use when |
|-----|----------|
| [docs/architecture/system-overview.md](docs/architecture/system-overview.md) | Where files belong (`routes/`, `services/`, …) |
| [docs/architecture.md](docs/architecture.md) | Layers, data flow, production topology |
| [docs/decisions.md](docs/decisions.md) | Why structural choices were made |

New business logic belongs in `backend/services/`, not in route handlers.

---

## Self-review checklist

Before you push or open a PR:

- [ ] `python -m unittest discover -s tests -v` passes
- [ ] No secrets, `.env*`, or personal `books.csv` in the diff
- [ ] Public API paths unchanged **or** [docs/api.md](docs/api.md) updated
- [ ] Scope is one logical change — no unrelated drive-by refactors
- [ ] You read the layer rules in [system-overview](docs/architecture/system-overview.md#backend-layer-rules)

GitHub also provides a [pull request template](.github/PULL_REQUEST_TEMPLATE.md) with the same ideas.

---

## Testing

```bash
source .venv/bin/activate   # if not already active
python -m unittest discover -s tests -v
```

Covers FastAPI routes (mocked persistence) and the flexible ingest pipeline. CI runs the same command on push and pull requests.

---

## Documentation expectations

| If you changed… | Update… |
|-----------------|---------|
| API paths or payloads | [docs/api.md](docs/api.md) |
| Deploy / env vars | [docs/deployment.md](docs/deployment.md) |
| Folder layout | [docs/architecture/system-overview.md](docs/architecture/system-overview.md) |
| Non-obvious trade-off | [docs/decisions.md](docs/decisions.md) or a [devlog](docs/devlogs/) |
| Refactor worth remembering | [DEVLOG.md](DEVLOG.md) + dated entry under `docs/devlogs/` |
| User-visible bug fix pattern | [docs/troubleshooting.md](docs/troubleshooting.md) |

Not every typo needs a devlog — use judgment.

---

## Code conventions

**Do**

- Match naming and import style in the file you edit
- Use `from backend.X import Y` from repo root
- Use `apiUrl()` in the frontend — no hardcoded production API URLs

**Don't**

- Commit venvs, `.env.local`, or `backend/data/processed/books.csv`
- Add abstractions (DI frameworks, extra layers) without a concrete need
- Expand scope “while you’re here” without logging it in a devlog

More detail: [docs/contributing.md](docs/contributing.md) (workflow, commit message style).

---

## Solo-maintained repo

One maintainer handles merges, deploys, and triage. That means:

- Issues and PRs may sit for a while — not a sign of rejection
- Large redesigns are unlikely to merge without prior discussion
- Breaking changes need a clear reason and doc updates

If you are unsure whether an idea fits, open a [feature request](.github/ISSUE_TEMPLATE/feature_request.md) first.

---

## Contribution philosophy

**Small focused changes > massive rewrites.**

Prefer incremental PRs: one endpoint moved to services, one ranking tweak, one doc fix. Big-bang refactors are hard to review alone and easy to regress.

Readable history matters more than perfect architecture on the first try. Ship the minimal fix, document the trade-off, iterate.

---

## Related

- [ROADMAP.md](ROADMAP.md) — planned directions
- [CHANGELOG.md](CHANGELOG.md) — release notes
- [docs/opensource.md](docs/opensource.md) — why this project is open source
- [SECURITY.md](SECURITY.md) — report vulnerabilities privately
