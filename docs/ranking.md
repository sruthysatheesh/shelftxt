# Ranking

Scoring lives in `backend/ranking/score.py`. Normalization prerequisites live in `backend/preprocess/normalize.py`.

## Feature normalization

### `normalize_rating(df)`

Resolves column: `rating` or `Star Rating`.

- Coerces to numeric; fills NaN with column mean.
- If all missing → `rating_norm = 0.5` for all rows.
- Otherwise min–max scale to [0, 1] via `_min_max()`.

### `compute_recency(df)`

Resolves column: `last_date_read` or `Last Date Read`.

- `days_since_read` = days from finish date to today (missing dates → today).
- `recency_norm` = min–max of days, **reversed** (smaller gap since read → higher score).

Neutral default when no date column: `recency_norm = 0.5`.

---

## Read books: `score_read_books`

**Input filter:** `read_status` / `Read Status` == `read`

**Formula:**

```txt
score = rating_weight × rating_norm + recency_weight × recency_norm
```

Defaults: `rating_weight=0.7`, `recency_weight=0.3`.

- Clipped to [0, 1].
- Sorted descending by `score`.

Used in the flexible pipeline output `read_ranked`. Not exposed as a standalone HTTP endpoint today.

---

## To-read books: `score_tbr_books`

**Input filter:** status == `to-read`

### Steps

1. **Dedupe** — drop duplicate `(title, author)` on TBR rows.
2. **Author preference** — from **read** rows only, group by author and mean `rating_norm` → `author_score`.
3. **Merge** — left join `author_score` onto each TBR row by author.
4. **Cold start** — authors never read: fill with global mean of read books’ `rating_norm`, or `0.5` if no read history.
5. **Noise** — add `Uniform(-randomness_strength, +randomness_strength)` per row (default `0.05`).
6. **Clip** — `score` in [0, 1].
7. **Sort** — descending by `score`.
8. **Diversity** (default `diverse_authors=True`) — keep first row per author only.

### Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| `randomness_strength` | `0.05` | Jitter magnitude |
| `diverse_authors` | `True` | One TBR book per author in ranked output |

---

## Recommendation: `recommend_one`

Called from `GET /recommend` after `score_tbr_books`.

```python
top_slice = tbr_ranked.head(5)
recommendation = top_slice.sample(1)  # uniform random
```

- Returns `None` if TBR ranked frame is empty → API returns `[]`.
- Otherwise returns a one-row DataFrame (serialized as a one-element JSON array).

**Design intent:** bias toward high author-preference scores while avoiding always picking rank #1.

---

## Column resolution

Both ranking and normalize modules use `_resolve_column(df, candidates)` to support app CSV and canonical DataFrames without duplicating logic.

Example status resolution: `["read_status", "Read Status"]`.

---

## API vs batch usage

| Call site | Functions invoked |
|-----------|-------------------|
| `GET /recommend` | `normalize_rating` → `compute_recency` → `score_tbr_books` → `recommend_one` |
| `run_flexible_pipeline` | above + `score_read_books` on full standardized frame |

Scores are **not** written back to `books.csv`.
