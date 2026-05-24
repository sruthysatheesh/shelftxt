# Roadmap

Directions for ShelfTxt — not promises or deadlines. The maintainer adjusts priorities as real usage and constraints emerge.

See also [DEVLOG.md](DEVLOG.md) for what already shipped.

---

## Near-term

- **Recommendation ranking** — tune scoring weights, edge cases (empty read history, single TBR title)
- **Backend cleanup** — finish moving shelf CRUD into `services/books.py`; retire legacy `api_draft.py`
- **Caching** — smarter invalidation for recommendation cache; less stale data after shelf moves
- **Testing coverage** — more service-layer tests with mocked repository, ranking unit tests

---

## Mid-term

- **Recommendations** — richer signals (genre hints, multiple suggestions, optional recency weighting in UI)
- **Accessibility** — keyboard navigation, screen-reader labels, reduced-motion-friendly UI
- **Free / legal book discovery** — research linking public-domain or library options to books already on your shelf (no piracy, no gray-market scraping)

---

## Long-term

- **Smarter recommendation systems** — learn from ratings and DNF patterns without opaque black-box models
- **Scalable ingestion** — batch pipeline that handles larger exports and repeatable offline analysis

---

## Out of scope (for now)

- Paid subscription tiers or locked features
- Bundled proprietary book catalogs
- Replacing CSV persistence before there is a concrete production need

Ideas welcome via [feature requests](.github/ISSUE_TEMPLATE/feature_request.md). Large changes benefit from a short design note in an issue first.
