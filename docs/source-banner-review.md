# Source comparison and homepage addition

Working branch: `feat/refresh-ui`; application baseline `cf3f15e`.
Compared with fetched `origin/main` at `3327ff3` without checkout or merge.

## Selective integration

Main's source modal provides the five-column source/status/note/link layout and
Vietnamese status labels. The current branch already had delegated source links,
`/api/laptop-sources/<id>`, `LaptopSource.to_dict()` and the same SQLite schema.
Keep that API and native dialog, rather than copying main's full catalog or jQuery
table. Render all API text as text nodes; allow only absolute HTTP(S) links without
embedded credentials. Preserve source statuses independently of URL availability.
The dialog supports loading, empty results, retry, cancellation, mismatched laptop
identity and horizontal table scrolling with keyboard focus on mobile.

The important missing change was audited source data. All 1,125 local source rows
were still `Verified`. Main's 1,125 rows exactly match the existing
`data/laptop_sources.csv` (all source fields checked); laptop rows and schema match.
`scripts/sync_audited_sources.py` updates only source metadata by the unique key
`(laptop_name, field_name)`, keeping source IDs, laptop rows, prices and model inputs.
It validates keys/schema/statuses before writes and makes a SQLite backup first.
Re-running after the update changes zero rows and creates no duplicates.

Current statuses inherited from main's audit (not newly verified on the web):
571 `Đã xác minh`, 60 `Chưa xác minh được`, 494 `Chưa có nguồn xác minh`.
No external URL scanning runs at startup or when opening pages/dialogs.

Dry run and apply, from the repository root:

```sh
python scripts/sync_audited_sources.py
python scripts/sync_audited_sources.py --apply --backup-dir .runtime/source-backups
```

The applied local backup is outside the checkout under
`D:\Laptop-main\source-banner-review\backups`. No database was copied over from main.
This script updates SQLite only; it does not alter a separately configured MySQL server.

For deployment, the updated `data/laptops.db` is tracked and included in this commit,
not only changed in an ignored local database. Set `DATABASE_BACKEND=sqlite` in the
Render demo Environment to select that exact bundled file without a MySQL probe.
Build and Start commands remain as documented in `RENDER_STARTUP.md`; no init or
training scripts run. A persistent disk must not mask the repository's `data/`
directory with an older database. A separately managed MySQL deployment needs its
own selective source migration; the SQLite script does not modify MySQL.

## Presentation

Homepage keeps its navigation, search, quick filters, featured cards and tool links.
Its introductory area now has a navy backdrop, HTML actions and three static,
slightly angled catalogue images selected by exact existing laptop names. Images
and source credits reuse the verified local manifest; no downloads, hotlinks, AI
images, new claims or model features were added. Intrinsic sizes and contain frames
reserve space. Mobile uses a compact three-image composition. No continuous animation.

Gunicorn configuration, lazy imports, Matplotlib cache and ML logic are unchanged.
`src/config.py` adds an explicit SQLite selection; default auto behavior remains.

Changed files: `app.py`, `templates/index.html`, `static/css/style.css`,
`static/js/ui.js`, `data/laptops.db`, `scripts/sync_audited_sources.py`,
`tests/test_source_sync.py`, `tests/test_workflows.py`, and this document.
Deployment selection adds `src/config.py`, `tests/test_database_config.py` and updates
`docs/RENDER_STARTUP.md`.
The pre-existing `static/charts/radar_comparison.png` modification is not part of this work.

## Verification

- 33 Python tests pass, including explicit deployment database selection, all page routes, comparison/radar PNG generation,
  prediction and recommendations, source identity/status contracts, migration backup,
  idempotence and duplicate-key rejection. Scientific imports remain excluded at boot.
- Fresh import measured about 1.8–1.9 seconds locally, no scientific libraries/font
  cache loaded; `/` and `/laptops` return 200. This is a Windows measurement, not Render.
- Browser: desktop 1440px, tablet 768px, mobile 390px, width checks at 320px; no page
  overflow observed. Checked banner images, search/filter/sort/pagination, real
  comparison and prediction (16,490,000 VND, five suggestions), statistics filtering.
- Actual Acer A314-36M-391A modal matches the audited blocked/verified/missing states.
  Escape restores trigger focus; mobile table scrolls with ArrowRight and shows focus.
  Image hover still scales 1.04. Menu click/tap/keyboard paths work.
- An isolated local fixture (outside the checkout, stopped after use) exercised
  loading/cancel, empty/API failure/retry, mismatched names, unsafe URLs and HTML
  injection strings. Only a safe HTTPS link rendered; injected tags remained text.
- Original uncommitted radar bytes restored; generated charts/CSVs restored after
  browser checks. CSV/model hashes and catalog rows unchanged; SQLite integrity OK.
- Screenshots kept outside the checkout in `D:\Laptop-main\source-banner-review`.
  No physical phone, Linux Gunicorn, Render deployment, emulated reduced-motion setting
  or hover-only menu pointer traversal was tested this time. Reduced-motion CSS and
  the existing desktop hover menu implementation remain in place.

The release includes the audited SQLite database and existing catalogue assets from
Git. No main merge or Render deployment is performed by the release checks.
