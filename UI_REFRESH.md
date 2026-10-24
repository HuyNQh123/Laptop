# UI refresh

Scope: shared Flask/Jinja shell, homepage and laptop catalog. Base: `main` at
`6207cc6c166d504ae22bd5c3688d2311198ae8a9`. Work branch: `feat/refresh-ui`.

## Behavior

- Light background, system fonts supporting Vietnamese, one blue accent, responsive navigation.
- Catalog cards retain every technical field from the original table (additional fields expand in native details).
- Existing quick filters and sorting fields remain available; brand, budget, RAM and weight filters combine.
- Search, filters, numeric sorting and pagination run on GET requests. The UI enhances requests with debounced search and partial replacement, while URLs remain shareable. Back/Forward reload the URL state.
- Page size choices remain 10/15/25/50/100; default 15. Invalid pages and sort values are clamped/validated.
- Source links open a native dialog with date, status and notes. Without JavaScript, the API link still opens its JSON response.
- Local product frames have a fixed 4:3 ratio and `object-fit: contain`. Missing images and failed image loads use a labeled placeholder. See `static/images/laptops/README.md` for adding permitted photographs to the empty manifest.

No ML algorithms, training inputs, database contents or model artifacts are changed.
No automatic training or analysis pipeline was invoked during UI verification.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests explicitly select the bundled SQLite database in read-only mode. Normal application startup
retains the existing MySQL/SQLite selection behavior.

## Verification

- Seven regression tests pass: combined filters, all legacy quick filters, numeric sort and complete pagination, search and invalid parameters, image fallback/path confinement, HTTP pages/escaped query, source API/assets.
- HTTP 200 verified for `/`, `/laptops`, `/compare` and local CSS/JS/placeholder assets; unknown source ID returns 404.
- Browser checked at desktop 1440×1000 and mobile 390×844: home, catalog, native mobile menu, live search, empty results, combined filters, price order, page size, page 2, browser Back, source dialog and close button.
- Browser search `zenbook` returns 6 entries; `macbook` returns 21. ASUS + budget 30 million + RAM ≥16 GB + weight ≤1.5 kg returns 8 entries.
- No horizontal page overflow at 390px. Product frame measured 333.6×250.2 pixels (4:3), image fit `contain`.
- Simulated an existing but invalid WebP asset; browser switched to the placeholder, which loaded successfully. Temporary fixture was removed.
- No JavaScript console errors observed in normal flows. Existing pandas deprecation warning occurs in the unchanged data-cleaning module during `/compare` smoke test.

Not verified: actual MySQL connection, real iOS/Android hardware or Safari/Firefox, browser JavaScript-disabled mode, ML predictions/training and full analysis/clustering runs. No real product photos have been added.
