# Flexible CSV pipeline

Batch ingestion for arbitrary user CSV schemas. Used from Python (`backend/ingest/pipeline.py`), not from the web Import tab (which posts JSON to `/books/import`).

## Entry points

| Function | Module | Purpose |
|----------|--------|---------|
| `validate_uploaded_csv` | `backend/ingest/pipeline.py` | Cheap gate before full processing |
| `run_flexible_pipeline` | `backend/ingest/pipeline.py` | Full validate → map → clean → rank |
| `load_csv` | `backend/ingest/load_csv.py` | Map columns + per-file validation |

## Pipeline stages

```txt
CSV file
  → validate_uploaded_csv (exists, parseable, non-empty, schema check)
  → load_csv (column_mappings → canonical DataFrame)
  → clean_books (ids, status, rating defaults)
  → normalize_rating
  → compute_recency
  → score_read_books + score_tbr_books
```

If validation status is `reject`, `run_flexible_pipeline` returns empty ranked frames and does not process further.

## Validation outcomes

| Status | Meaning |
|--------|---------|
| `accept` | No errors; may have warnings |
| `accept_with_warnings` | Usable data with non-fatal issues |
| `reject` | Missing file, parse failure, empty data, or schema errors |

Report shape:

```python
{
  "status": "accept" | "accept_with_warnings" | "reject",
  "errors": [],
  "warnings": [],
  "row_count": 42,
  "columns": ["Book Name", "Writer", ...],
}
```

### Common errors

- File not found
- CSV parse exception
- No data rows
- Missing required canonical field after mapping
- Required field has no usable non-empty values

### Common warnings

- Non-`.csv` extension (still attempts parse)
- Unknown `read_status` values
- Unknown `type_hints` keys

## Mapping configuration

Template: `backend/ingest/mapping.example.json`

### Keys

| Key | Type | Description |
|-----|------|-------------|
| `column_mappings` | `dict[str, str]` | Raw CSV header → canonical field name |
| `required_fields` | `list[str]` | Canonical fields that must exist and have data |
| `defaults` | `dict` | Values for canonical columns not present in CSV |
| `type_hints` | `dict[str, str]` | `"numeric"` or `"datetime"` coercion |

`column_mappings` keys are **source headers**; values are **canonical** names (`title`, `author`, …).

Configs merge with `DEFAULT_MAPPING_CONFIG` in `load_csv.py` (ShelfTxt export headers).

### Example

```json
{
  "column_mappings": {
    "Book Name": "title",
    "Writer": "author",
    "Category": "genre",
    "Status": "read_status",
    "My Rating": "rating",
    "Finished On": "last_date_read",
    "External Id": "book_id"
  },
  "required_fields": ["title", "read_status"],
  "defaults": {
    "author": "unknown",
    "genre": "unknown",
    "rating": null,
    "last_date_read": null,
    "book_id": null
  },
  "type_hints": {
    "rating": "numeric",
    "last_date_read": "datetime"
  }
}
```

## `run_flexible_pipeline` return value

```python
{
  "validation": { ... },      # merged validation + mapping warnings/errors
  "read_ranked": DataFrame,   # sorted by score, read rows only
  "tbr_ranked": DataFrame,    # sorted by score, to-read rows only
}
```

### Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| `rating_weight` | `0.7` | Weight for `rating_norm` in read scoring |
| `recency_weight` | `0.3` | Weight for `recency_norm` in read scoring |

## Usage examples

### Full pipeline

```python
from backend.ingest.pipeline import run_flexible_pipeline

result = run_flexible_pipeline(
    "data/raw/my_export.csv",
    mapping_config={
        "column_mappings": {
            "Book Name": "title",
            "Writer": "author",
            "Status": "read_status",
            "My Rating": "rating",
            "Finished On": "last_date_read",
        }
    },
)

if result["validation"]["status"] == "reject":
    print(result["validation"]["errors"])
else:
    print(result["tbr_ranked"].head())
```

### Validation only

```python
from backend.ingest.pipeline import validate_uploaded_csv

report = validate_uploaded_csv("upload.csv", mapping_config={...})
```

## `clean_books` behavior

`backend/preprocess/clean_books.py`:

- Ensures all canonical columns exist
- Lowercases and strips `read_status`
- Fills missing `book_id` with random 13-digit strings
- Fills missing ratings with column mean or `3.0`
- Fills missing `last_date_read` with today

## Tests

`tests/test_flexible_pipeline.py` — validation gates, mapping, ranking integration.

Run: `./venv/bin/python -m unittest discover -s test -v`
