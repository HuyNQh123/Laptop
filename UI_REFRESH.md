# LapInsight interface and image review

Branch: `feat/refresh-ui`, based on `main` commit `6207cc6c166d504ae22bd5c3688d2311198ae8a9`.

The shared shell, homepage, catalog, comparison, prediction, analysis and clustering pages now use
a light surface, Vietnamese-capable system fonts, one blue accent, thin borders and responsive layouts.
Promotional copy, emoji, gradients, thick shadows and decorative animation are removed from these pages.
Existing routes and tools remain available.

## Product images

- 225 unique full-name mappings; 2 verified photographs and 223 explicit missing/unverified entries.
- Pilot: first 10 catalog entries; 0 approved, with concrete source/model/permission reasons recorded.
- Extended source audit: 175 distinct existing URLs across the full catalog. Source redirects and
  HTTP failures are recorded without inventing product/image URLs.
- Both shipped assets have CC BY-SA 4.0 provenance, model/generation evidence, author, source URLs,
  checksums and modification notes. Together they are 61,206 bytes of optimized WebP.
- The same component and mapping are used in the catalog, comparison and prediction recommendations.
- Missing/corrupt/failed images show “Chưa có ảnh”. Unverified candidates are not displayed.
- See `static/images/laptops/README.md` for full provenance, status counts and the expansion workflow.

## Preserved behavior

- Catalog GET search/filter/sort/pagination and all legacy quick filters; query state survives sharing and Back.
- Two-laptop comparison, selectable criteria, real value differences and optional radar. Its explanation
  now correctly says outward values are larger, including price/weight, rather than always better.
- Nine prediction inputs, the existing presets and trained model; recommendations attach image metadata
  only after prediction/ranking. Their actual price differences are shown without promising a fixed ±2 million range.
- Statistical highlights, brand summaries and charts; K-Means/PCA details, searchable/sortable/filterable
  cluster table and pagination. K remains 3; Silhouette is shown as a score, not an accuracy percentage.
- Comparison rejects unknown models/criteria and prediction rejects non-finite form values.

No ML feature list, training CSV/database, model artifact or algorithm is modified.

## Run/check

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000
.\.venv\Scripts\python.exe tools/check_product_images.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests use read-only SQLite, a temporary output directory and a copy of the existing model.
They explicitly prohibit training. Generated chart/analysis CSV outputs stay in temporary storage;
input/model/database hashes are checked after workflows. Browser-generated outputs are excluded/restored
before the source commit. Virtual environments and local caches are ignored.

## Verification (2026-10-25)

- 16 regression tests: combined/legacy catalog filters, numeric sorting, complete pagination, escaped/invalid
  queries, source API/404/assets, exact manifest coverage, duplicate keys, image checksum/decoding/size/license,
  verification gate, all six page routes with real data, actual model prediction and recommendation rendering,
  prediction errors/form preservation, comparison/errors, native decimal min/step constraints.
- Desktop 1440×1000 and mobile 390×844 browser checks: catalog filters and verified image, two-photo comparison,
  preset filling, successful prediction, recommendation photo, analysis, clustering search/sort/filter/pagination.
- M3 sample input returns 38,260,000 VND; first recommendation is MTL73SA/A with its verified image.
- Cluster search “Apple” returns 21 rows; selecting cluster 2 returns 13 rows and resets pagination.
- Shared photo frames use 4:3 with `object-fit: contain`; no page-level horizontal overflow observed at 390px.
- Broken-file image fallback has been tested; source/author/license links and alt text are present.
- No JavaScript console errors in normal workflows. The unchanged cleaning module emits a pandas deprecation warning.

Not verified: live MySQL, physical iOS/Android devices, Safari/Firefox, or browser JavaScript-disabled mode.
Product photo coverage remains deliberately incomplete: 223 entries need verifiable model/permission evidence.
