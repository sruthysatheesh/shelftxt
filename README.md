# ShelfTxt

A personal reading library and recommendation app — organize what you own, track what you are reading, and get a suggested next book from your to-read shelf.

**Live:** [shelftxt.vercel.app](https://shelftxt.vercel.app) · **API:** [shelftxt.onrender.com/docs](https://shelftxt.onrender.com/docs)

---

## Mission

ShelfTxt exists to make **reading more accessible and less overwhelming**.

Reading should not depend on expensive platforms or opaque algorithms. ShelfTxt helps you:

- **Organize a personal library** — want-to-read, currently reading, finished, and DNF shelves in one place
- **Reduce decision fatigue** — a ranked suggestion from *your* list, based on authors you have already enjoyed
- **Stay in control of your data** — a simple CSV-backed library you can export, back up, or inspect
- **Keep access affordable** — built to run on free-tier hosting (Vercel + Render) and open-source tooling

**Long-term goal:** A dependable, transparent reading companion — strong recommendations, flexible imports, and backend architecture that stays maintainable as the project grows — without locking readers into a paid ecosystem.

---

## Features

What works today:

- **Library shelves** — want to read, reading (with progress %), read (with ratings), and DNF
- **Add, edit, and remove books** — title, author, page count, shelf moves via the web UI
- **Next-read suggestion** — `GET /recommend` ranks your to-read list using read-history author preferences
- **CSV import** — upload a spreadsheet from the Import tab; duplicates skipped automatically
- **REST API** — FastAPI backend with OpenAPI docs at `/docs`
- **Batch CSV pipeline** — map arbitrary export formats to a canonical schema for offline analysis ([pipeline docs](docs/pipeline.md))
- **CLI helper** — interactive shelf updates via `python -m cli.manage_books`

No bundled sample library — `backend/data/processed/books.csv` is created empty on first use.

---

## Live demo

| Surface | URL |
|---------|-----|
| **Frontend** | https://shelftxt.vercel.app |
| **API (Swagger)** | https://shelftxt.onrender.com/docs |
| **Health check** | https://shelftxt.onrender.com/health |

---

## Tech stack

| Layer | Tools |
|-------|--------|
| **Backend** | Python, FastAPI, pandas, uvicorn |
| **Frontend** | Next.js 16 (App Router), React, TypeScript |
| **Data processing** | pandas/numpy preprocessing, custom ranking in `backend/ranking/` |
| **Persistence** | CSV (`backend/data/processed/books.csv`) |
| **Deployment** | Render (API), Vercel (UI) |

Backend layout: routes → services → repository → `book_data.py`. See [system overview](docs/architecture/system-overview.md).

---

## Quick start

### Backend

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.api:app --reload
```

- API: http://127.0.0.1:8000  
- Swagger: http://127.0.0.1:8000/docs  

### Frontend

```bash
cd frontend && npm install && npm run dev
```

Open http://localhost:3000.

By default, dev uses a local API on port 8000. To use the hosted API without running uvicorn:

```bash
cp frontend/.env.local.example frontend/.env.local
# edit API_BASE_URL if needed, then restart npm run dev
```

Full setup: [docs/development.md](docs/development.md)

---

## Testing

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

Covers FastAPI routes (mocked persistence) and the flexible ingest pipeline.

---

## Project structure

```text
shelftxt/
├── backend/           # FastAPI app, services, ranking, CSV persistence
│   ├── routes/        # HTTP handlers
│   ├── services/      # Business logic (recommend, delete, …)
│   ├── ranking/       # TBR/read scoring algorithms
│   ├── preprocess/    # rating_norm, recency_norm
│   ├── ingest/        # Batch CSV pipeline (mapping + validation)
│   └── data/          # Live library CSV (gitignored)
├── frontend/          # Next.js UI
├── cli/               # Interactive shelf helper
├── tests/             # Python unit tests
└── docs/              # Technical + engineering documentation
```

Run Python commands from the **repo root** so `backend` resolves as a package.

---

## Documentation

| Doc | Topic |
|-----|-------|
| [docs/README.md](docs/README.md) | **Doc index** — start here |
| [docs/architecture.md](docs/architecture.md) | System design, layers, topology |
| [docs/architecture/system-overview.md](docs/architecture/system-overview.md) | Folder responsibilities |
| [docs/deployment.md](docs/deployment.md) | Render + Vercel runbook |
| [docs/decisions.md](docs/decisions.md) | Architecture decisions (ADRs) |
| [docs/contributing.md](docs/contributing.md) | How to contribute |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Common errors |
| [docs/development.md](docs/development.md) | Local setup |
| [docs/api.md](docs/api.md) | REST reference |
| [docs/data-model.md](docs/data-model.md) | CSV schemas |
| [docs/ranking.md](docs/ranking.md) | Scoring algorithms |
| [docs/pipeline.md](docs/pipeline.md) | Batch CSV pipeline |
| [docs/frontend.md](docs/frontend.md) | Next.js UI |

---

## Engineering notes

ShelfTxt is actively developed — refactors, deploy fixes, and architecture notes are logged in the open.

| Resource | Description |
|----------|-------------|
| [DEVLOG.md](DEVLOG.md) | Devlog index — timeline and major refactors |
| [docs/devlogs/](docs/devlogs/) | Dated engineering entries |
| [docs/architecture/](docs/architecture/) | Architecture docs and system overview |
| [docs/screenshots/](docs/screenshots/) | Optional visuals for devlogs |

Recent work: backend layered refactor (routes, services, repository) — [2026-05-24 devlog](docs/devlogs/2026-05-24-backend-refactor.md).

---

## Roadmap

Realistic directions — not commitments:

- **Architecture** — finish moving shelf CRUD/PATCH into `services/books.py`; remove legacy `api_draft.py`
- **Caching** — smarter recommendation cache invalidation; optional persistence beyond in-process LRU
- **Recommendations** — richer ranking signals (genre, recency weighting UI, multiple suggestions)
- **Import / export** — Goodreads-style export, better CSV column mapping in the web UI
- **Accessibility** — keyboard navigation, screen-reader labels, reduced-motion-friendly UI
- **Discovery** — surface *legal free* reading options (public domain, library links) tied to books already on your shelf — research phase only
- **Storage** — optional database or persistent disk for production libraries on Render

Track in [DEVLOG.md](DEVLOG.md) and [refactor backlog](docs/architecture/system-overview.md#refactor-backlog).

---

## Contributing

See [docs/contributing.md](docs/contributing.md) for workflow, PR checklist, and where to put new code.

---

## License

MIT — see [LICENSE](LICENSE).
