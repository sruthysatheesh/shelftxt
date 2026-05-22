# Architecture

## Overview

LibroRank is a monorepo with three runnable surfaces:

| Surface | Stack | Entry |
|---------|-------|-------|
| API | FastAPI + pandas | `api.py` |
| Web UI | Next.js (App Router) | `frontend/app/page.tsx` |
| Batch pipeline | Python modules | `ingest/pipeline.py` |

All app-facing state lives in a single CSV file: `data/processed/books.csv`, managed by `book_data.py`.

## Component diagram

```mermaid
flowchart TB
  subgraph client [Browser]
    Page[page.tsx]
  end
  subgraph next [Next.js server]
    BooksRoute["/api/books"]
    RecommendRoute["/api/recommend"]
    ImportRoute["/api/books/import"]
    RemoveRoute["/api/books/remove"]
  end
  subgraph python [FastAPI]
    API[api.py]
    BD[book_data.py]
    Norm[preprocess/normalize.py]
    Score[ranking/score.py]
  end
  subgraph batch [Batch only]
    Pipe[ingest/pipeline.py]
    Load[ingest/load_csv.py]
    Clean[preprocess/clean_books.py]
  end
  CSV[(books.csv)]

  Page --> BooksRoute & RecommendRoute & ImportRoute & RemoveRoute
  BooksRoute & RecommendRoute & ImportRoute & RemoveRoute --> API
  API --> BD --> CSV
  API --> Norm --> Score
  Pipe --> Load --> Clean --> Norm --> Score
```

## Two data paths

### App path (UI + API + CLI)

- **Schema:** Goodreads-style columns (`Title`, `Authors`, `Read Status`, …).
- **Read/write:** `book_data.load_data()` / `save_data()`.
- **Ranking:** Called on demand in `GET /recommend`; does not persist scores to CSV.

### Batch path (flexible pipeline)

- **Schema:** Canonical lowercase fields (`title`, `author`, `read_status`, …).
- **Input:** Arbitrary user CSV + JSON mapping config.
- **Output:** In-memory ranked DataFrames (`read_ranked`, `tbr_ranked`); not automatically merged into `books.csv`.

The batch path reuses `preprocess/normalize.py` and `ranking/score.py` so scoring behavior stays consistent. Column name resolution in those modules accepts both canonical and app column names via `_resolve_column()`.

## Module responsibilities

| Module | Responsibility |
|--------|----------------|
| `book_data.py` | Ensure CSV exists, define columns, load/save with type coercion |
| `api.py` | HTTP routes, Pydantic models, shelf transitions, CORS, Render keep-warm scheduler |
| `ingest/load_csv.py` | Map raw headers → canonical columns, validate, coerce types |
| `ingest/pipeline.py` | `validate_uploaded_csv`, `run_flexible_pipeline` orchestration |
| `preprocess/clean_books.py` | Fill missing ids, normalize status strings, default ratings |
| `preprocess/normalize.py` | `rating_norm`, `recency_norm`, optional combined score |
| `ranking/score.py` | Rank read/TBR lists, `recommend_one` sampling |
| `cli/manage_books.py` | Thin interactive wrapper over `book_data` |

## Cross-cutting concerns

**CORS** — `api.py` allows `localhost:3000`, `127.0.0.1:3000`, and the production frontend origin.

**JSON safety** — `clean_for_json()` replaces `NaN` with `null` before serializing DataFrames.

**Title as key** — Updates and deletes match on `Title` string equality. Duplicate titles are prevented on rename.

**Render keep-warm** — `AsyncIOScheduler` pings `/health` every 14 minutes during app lifespan (see `development.md`).
