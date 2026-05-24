# Architecture decisions

Lightweight ADRs. Format: context → decision → consequences.

---

## ADR-001: CSV as single source of truth

**Status:** Accepted

**Context:** Solo project, small library, no auth yet.

**Decision:** Live library in `backend/data/processed/books.csv`. Low-level access via `book_data.py`; services/routes prefer `repository/books_repository.py`.

**Consequences:** (+) Simple, portable (−) No concurrent-write safety; ephemeral disk on Render free tier.

---

## ADR-002: Monorepo, not microservices

**Status:** Accepted

**Decision:** Single repo: `backend/`, `frontend/`, `cli/`. Deploy API (Render) and UI (Vercel) separately.

**Consequences:** (+) One PR, shared ranking code (−) Correct Root Directory per host required.

---

## ADR-003: Production API calls bypass Vercel proxy

**Status:** Accepted

**Decision:** Production browser → Render via `apiUrl.ts`. Local dev → `/api/*` Next proxy.

**Consequences:** (+) Reliable on Vercel (−) CORS required for `shelftxt.vercel.app`.

---

## ADR-004: Title string as primary key

**Status:** Accepted

**Decision:** API matches books by exact `Title`.

**Consequences:** (+) Matches CSV exports (−) Duplicate/renamed titles are fragile.

---

## ADR-005: Layered backend (routes / services / repository)

**Status:** Accepted (2026-05)

**Context:** Monolithic `api.py` mixed HTTP, shelf rules, and persistence.

**Decision:**

| Layer | Location |
|-------|----------|
| App shell | `backend/api.py` |
| HTTP routes | `backend/routes/` |
| Request models | `backend/schemas/` |
| Business logic | `backend/services/` |
| Persistence facade | `backend/repository/` → `book_data.py` |

**Consequences:**

- (+) Clear boundaries; routes stay thin where extracted
- (+) `GET /recommend` isolated in `services/recommendation.py`
- (−) Some shelf PATCH logic still in `routes/books.py` until moved to `services/books.py`
- (−) `api_draft.py` kept temporarily as legacy reference — **do not extend**

---

## ADR-006: Two ingest paths

**Status:** Accepted

**Decision:** Web `POST /books/import` (JSON) vs batch `ingest/pipeline.py` (mapping JSON).

---

## ADR-007: Cached recommendations

**Status:** Accepted

**Decision:** `get_recommendation()` uses `@lru_cache(maxsize=1)`. `POST /recommend/refresh` clears cache after shelf changes (optional ops endpoint).

**Consequences:** (+) Fewer repeated scoring runs (−) Stale pick until refresh or process restart.

---

## When to add a new ADR

Persistence change, auth, new deploy target, or a trade-off future you will question.
