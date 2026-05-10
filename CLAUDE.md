# CLAUDE.md

## Project context
- Graduation project: subway pedestrian navigation server for visually impaired users.
- Team A (이예진) owns this Flask backend.
- Team B owns DB + KNN; integrates via `subway_server/core/locator.py`.
- Teams C, D own the Android app (separate repo, TBD).
- Principle: **completion over performance**. Working code beats elegant abstractions.

## Architecture at a glance
- App factory in `subway_server/__init__.py` — call `create_app(config)`.
- API layer (`subway_server/api/`) is thin: validate, dispatch, serialize.
- Domain logic (`subway_server/core/`) is pure Python — no Flask imports.
- DB layer (`subway_server/db/`) is Team B's territory; A only stubs interfaces.

## Coordinate convention (do not change)
North = 0°, East = 90°, South = 180°, West = 270° (CW positive).
Matches phone compass. Pinned by 4 cardinal-direction unit tests in `tests/unit/test_direction.py` — those tests are a **contract**.

## Team B integration boundary
- `subway_server/core/locator.py` defines `LocationEstimator = Callable[[list[WifiSample]], str]`.
- Default stub raises `NotImplementedError` → mapped to `KNN_ERROR` (500).
- Team B will add `subway_server/core/knn.py` exporting `knn_estimate`. App factory auto-imports it at startup if present.
- Tests use the `fake_estimator` fixture (`tests/conftest.py`).
- **DO NOT** change this seam without team agreement.

## Wi-Fi pipeline split
- `core/wifi.py::normalize_wifi(samples, bssid_order)` — A's responsibility (pure list manipulation, no DB).
- `db/fingerprint.py::FingerprintRepository::list_bssid_order()` — B's responsibility (DB schema dependent).
- B's `knn_estimate` calls both internally.

## Error envelope
All errors follow `docs/05-API명세.md §5.5`:
```json
{ "error": { "code": "...", "message": "..." } }
```
- Domain raises `AppError` subclasses (`subway_server/api/errors.py`).
- Flask error handler converts to JSON. Don't write ad-hoc error responses.
- Adding a new error code requires updating both `docs/05-API명세.md` and `errors.py`.

## Running and testing
- Dev server: `python app.py` (port 5000, uses `.env` or defaults).
- Swagger UI: `http://localhost:5000/apidocs`.
- Tests: `pytest` from repo root. **No MySQL required** — TestConfig isolates state, estimator stub guards against DB calls.
- Quick: `pytest tests/unit -q`. Full: `pytest`.

## Conventions
- Type hints on every function signature (Python 3.10+).
- Domain exceptions live in `api/errors.py`.
- One function = one responsibility. If you're adding a third level of abstraction, stop.
- No ORM, no Docker, no caching, no auth (see `docs/07-구현계획.md §7.3.4`).
- Korean comments are fine where they aid clarity; identifiers stay English.

## When extending
- New endpoint → new file in `subway_server/api/`, register via import in `api/__init__.py`, write integration test first.
- New graph operation → pure function in `core/graph.py`, unit test first.
- Change `data/*.json` shape → update `tests/fixtures/*.json` in lockstep.
- Change Swagger spec → keep `docs/05-API명세.md` in sync (it's the source of truth).

## Read before non-trivial changes
- `docs/05-API명세.md` — API contracts (request/response/error codes)
- `docs/06-데이터모델.md` — data shapes
- `docs/09-위험요소및결정항목.md` — open decisions; check before changing behavior
- `worklog/` — recent work history

## When work completes, write a worklog entry
After any meaningful work unit (= a real commit), add `worklog/YYYY-MM-DD-<slug>.md` following the template in `worklog/README.md`. Keep entries short — bullets, not paragraphs. The point is preserving "why" and "what's next" so the next session picks up cold.

## What this project is NOT
- Not a production system. No auth, no rate limiting, no observability.
- Not optimized — node graph is ~10–30 nodes; algorithms can be naive.
- Not multi-station — single-station demo only.
