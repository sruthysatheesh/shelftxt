# Contributing

Conventions for the Shelftxt monorepo.

---

## Prerequisites

Python 3.14+, Node.js 20+, Git. Setup: [development.md](development.md).

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

**Imports:** `from backend.routes.books import ...`, never `from book_data` without package prefix.

---

## Frontend

- Browser fetches: `apiUrl("/books")` etc. in `page.tsx`
- Do not hardcode Render URL in components
- Dev proxy: `app/api/*/route.ts` + `backendUrl.ts`

---

## Tests

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

| Test file | App entry | Mock targets (examples) |
|-----------|-----------|-------------------------|
| `test_api.py` | `backend.api.app` | `backend.routes.books.load_data`, `backend.services.recommendation.get_recommendation` |
| `test_flexible_pipeline.py` | — | `backend.ingest.*` |

Patch where the name is **looked up**, not where it is defined.

---

## Pull request checklist

- [ ] Tests pass
- [ ] No secrets or `books.csv` in diff
- [ ] Public paths unchanged (`/recommend`, `/books`, …) or documented in `api.md`
- [ ] Docs updated for behavior or layout changes

---

## Refactor status

| Area | Status |
|------|--------|
| App shell + routers | Done — `backend/api.py` |
| Schemas | Done — `schemas/books.py` |
| `GET /recommend` | Done — `services/recommendation.py` |
| Delete book | Partial — `services/books.delete_book_by_title` |
| Add / import / PATCH shelf | In `routes/books.py` → move to `services/books.py` when touched |
| Remove `api_draft.py` | Pending — after tests target `backend.api` only |

---

## Related

- [architecture.md](architecture.md)
- [decisions.md](decisions.md)
- [troubleshooting.md](troubleshooting.md)
