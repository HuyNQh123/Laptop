# LapInsight interface and image review

Branch: `feat/refresh-ui`, based on `main` commit `6207cc6c166d504ae22bd5c3688d2311198ae8a9`.

The shared shell, homepage, catalog, comparison, prediction, analysis and clustering pages now use
a light surface, Vietnamese-capable system fonts, one blue accent, thin borders and responsive layouts.
Promotional copy, emoji, gradients, thick shadows and decorative animation are removed from these pages.
Existing routes and tools remain available.

## Product images

- Catalogue packshots replace the two earlier contextual/user photographs. Real manufacturer/retailer
  product pages are discovered using SKU searches, then opened and compared before selecting a gallery image.
- The 13-model pilot was checked in the running browser before expanding the same process across all 225 names.
  Current counts, missing reasons and source attempts are in `data/image_audit_summary.json` and
  `docs/laptop-image-audit.md`; every name has its own unique mapping in `data/laptop_images.json`.
- Product match and reuse rights are separate. No open license is invented. Sources with explicit restrictions,
  including HACOM's separate image policy, are rejected and alternatives sought. `not_declared` does not mean
  permission is granted. Notices and the exact checked scope are retained with each approved source.
- The shared component serves local WebP assets in white 4:3 frames with contain, intrinsic size caps, model alt
  text, lazy loading and broken-image fallback. It is used by catalog, comparison and prediction recommendations.
- `exact_model` means the product page confirms the catalog SKU; any source/CSV configuration conflict is recorded
  without editing training data. `same_series_representative` is supported and explicitly labeled, but is not used
  without evidence of the same exterior. Unknown models/images stay as “Chưa có ảnh”.
- See `static/images/laptops/README.md` for fields and the repeatable review/import workflow.

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

## Verification (2026-10-26)

- 21 regression/integration tests cover routes, real prediction/comparison, form validation, catalog search/filter/sort/pagination,
  unique mappings, image decoding/hash/size, catalogue visual gate, path confinement and separate rights states.
- Tests use read-only SQLite, copied model and temporary output directories; input/model/database hashes are checked.
- Browser checks and screenshots are documented in `docs/laptop-image-qa.md` after the final asset review.
- Existing pandas deprecation warning remains; no training, algorithm or input feature change is part of this update.
- Not verified: live MySQL, physical iOS/Android devices, Safari/Firefox, or JavaScript-disabled browser mode.

The working branch stays `feat/refresh-ui`. Main through a8075b8 has now been merged into this branch,
including its sources/statistics changes. The two template conflicts were resolved by combining their behavior;
see `docs/main-merge-review.md` for integration checks. PR #1 remains open and has not been merged into main.

Targeted image pass (2026-10-26): 69 laptops have imagery (67 exact, 2 same-exterior representatives),
156 still use the placeholder. Reusing assets and consolidating one byte-identical legacy duplicate leaves 66 WebP files; existing images
and rights states are retained. See `docs/targeted-image-pass.md`, `data/image_targeted_review.json`,
and `data/image_family_inventory.json` for all missing groups, match evidence and pending sources.
