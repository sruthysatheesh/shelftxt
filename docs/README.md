# LibroRank — Technical documentation

Developer-facing reference for architecture, APIs, data models, and pipelines.

## Contents

| Doc | Description |
|-----|-------------|
| [architecture.md](architecture.md) | System layout, module boundaries, data paths |
| [data-model.md](data-model.md) | App CSV schema, canonical fields, shelf mapping |
| [api.md](api.md) | FastAPI REST reference and Next.js proxy routes |
| [pipeline.md](pipeline.md) | Flexible CSV ingest, mapping config, validation |
| [ranking.md](ranking.md) | Scoring formulas and recommendation behavior |
| [frontend.md](frontend.md) | Next.js app structure and UI behavior |
| [development.md](development.md) | Local setup, tests, CLI, deployment, env vars |

## Quick links

- Interactive API docs (when server is running): `http://127.0.0.1:8000/docs`
- Mapping template: [`ingest/mapping.example.json`](../ingest/mapping.example.json)
- Persistence layer: [`book_data.py`](../book_data.py)
