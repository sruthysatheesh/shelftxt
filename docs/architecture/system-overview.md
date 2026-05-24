# System overview

High-level map of the shelftxt codebase. For production topology and ADRs, see [architecture.md](../architecture.md) and [decisions.md](../decisions.md).

---

## Monorepo at a glance

```txt
shelftxt/
├── backend/          # Python API, ranking, persistence
├── frontend/         # Next.js UI (Vercel)
├── cli/              # Local interactive helper
├── tests/            # Python unit tests
└── docs/             # Technical + engineering docs
```

**Production:** Browser → [Vercel frontend](https://shelftxt.vercel.app) → [Render API](https://shelftxt.onrender.com).

---

## `backend/`

The Python application package. All FastAPI and shelf logic lives here.

| Path | Responsibility |
|------|----------------|
| `api.py` | FastAPI app: CORS, keep-warm scheduler, registers routers |
| `routes/` | HTTP handlers only — parse request, call service, return response |
| `schemas/` | Pydantic request/response models |
| `services/` | Business use-cases (recommend, delete book, …) |
| `repository/` | Thin persistence facade over `book_data.py` |
| `book_data.py` | CSV load/save, column schema, type coercion |
| `data/` | Runtime data (`processed/books.csv` gitignored) |
| `ingest/` | Batch CSV pipeline (mapping, validation) — not used by live UI import |
| `preprocess/` | Normalization transforms for ranking (`rating_norm`, `recency_norm`) |
| `ranking/` | Scoring and recommendation algorithms (`score_tbr_books`, `recommend_one`) |

**Request flow (simplified):**

```text
HTTP request
  → routes/
  → services/     (orchestration)
  → repository/ → book_data.py → books.csv
  → preprocess/ + ranking/        (algorithms only, no I/O)
```

---

## `backend/services/`

**Purpose:** “Do one thing for the user” — orchestrate data loading, call algorithms, shape responses.

| Module | Role |
|--------|------|
| `recommendation.py` | Load shelf → normalize → score TBR → pick one book → JSON-safe list |
| `books.py` | Delete-by-title, date helpers (shelf PATCH still migrating from routes) |

**Rules:** No FastAPI routers here. No raw HTTP status codes unless raising `HTTPException` for business rules.

---

## `backend/ranking/`

**Purpose:** Pure ranking math — how books are scored and ordered.

| Module | Role |
|--------|------|
| `score.py` | Rank read list and TBR list; author preference; optional diversity; `recommend_one` sampling |

Accepts DataFrames with either app columns (`Title`, `Read Status`) or canonical columns (`title`, `read_status`) via column resolution helpers.

**Rules:** No file I/O, no HTTP, no knowledge of CSV paths.

---

## `backend/preprocess/`

**Purpose:** Feature engineering before scoring.

| Module | Role |
|--------|------|
| `normalize.py` | `rating_norm`, `recency_norm` |
| `clean_books.py` | Defaults and cleanup for batch/canonical schema |

Used by both the live recommendation path and the batch ingest pipeline.

---

## `backend/routes/`

**Purpose:** FastAPI routers — the HTTP surface.

| Router | Paths |
|--------|-------|
| `health.py` | `GET /`, `GET|HEAD /health` |
| `books.py` | CRUD, import, shelf PATCH |
| `recommendation.py` | `GET /recommend`, `POST /recommend/refresh` |

**Goal:** Stay thin. Validation via `schemas/`; heavy logic delegates to `services/`.

---

## Backend layer rules

```text
routes/  →  services/  →  repository/  →  book_data.py  →  CSV
                ↘  preprocess/ , ranking/  (algorithms, no I/O)
```

| Layer | Do | Don't |
|-------|-----|--------|
| `routes/` | HTTP, call services, use `schemas/` | Shelf algorithms, direct CSV rules long-term |
| `services/` | Orchestration, `HTTPException` for business rules | Import FastAPI routers |
| `repository/` | `get_all_books`, `save_books` | Ranking or PATCH branching |
| `book_data.py` | CSV path, columns, load/save | HTTP or shelf logic |
| `schemas/` | Pydantic models only | Business logic |

**Imports:** `from backend.routes.books import ...` — always use the `backend.` package prefix.

---

## Testing notes

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

| Test file | App entry | Mock where used (examples) |
|-----------|-----------|----------------------------|
| `test_api.py` | `backend.api.app` | `backend.routes.books.load_data`, `backend.services.books.get_all_books`, `backend.routes.recommendation.get_recommendation` |
| `test_flexible_pipeline.py` | — | `backend.ingest.*` |

Patch where the name is **looked up** in the module under test, not where it is defined. See [troubleshooting.md](../troubleshooting.md#tests).

---

## Refactor backlog

Tracked here for visibility — not a contribution checklist. Log completed work in [DEVLOG.md](../../DEVLOG.md).

| Area | Status |
|------|--------|
| App shell + routers | Done — `backend/api.py` |
| Schemas | Done — `schemas/books.py` |
| `GET /recommend` | Done — `services/recommendation.py` |
| Delete book | Partial — `services/books.delete_book_by_title` |
| Add / import / PATCH shelf | In `routes/books.py` → move to `services/books.py` |
| Remove `api_draft.py` | Pending |

---

## `frontend/`

**Purpose:** Single-page Next.js app — library shelves, CSV import, discover tab.

| Area | Role |
|------|------|
| `app/page.tsx` | Main UI (client component) |
| `lib/apiUrl.ts` | Production: browser → Render API |
| `lib/backendUrl.ts` | Dev: Next.js proxy → local/remote backend |
| `app/api/*/route.ts` | Dev-only same-origin proxy (avoids CORS locally) |

Deployed on Vercel with Root Directory = `frontend`.

---

## What belongs where (quick reference)

| Question | Look in |
|----------|---------|
| Change an API path or status code | `backend/routes/` |
| Change how recommendations are picked | `backend/ranking/` + `backend/services/recommendation.py` |
| Change CSV columns or load behavior | `backend/book_data.py` |
| Change deploy / env | [deployment.md](../deployment.md) |
| Why we made a structural choice | [decisions.md](../decisions.md) |
| What we changed last week | [devlogs/](../devlogs/) |

---

## Related

- [architecture.md](../architecture.md) — diagrams, two data paths, testing
- [DEVLOG.md](../../DEVLOG.md) — engineering timeline
