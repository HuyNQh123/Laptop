# Product photographs and image audit

## Included assets

| Local asset | Product match | Author | License |
| --- | --- | --- | --- |
| `air-m2.webp` | Apple MacBook Air M2 13-inch (2022), A2681, Silver; catalog SKU MLY03SA/A | メイド理世 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| `pro14-m3.webp` | Apple MacBook Pro M3 14-inch (Nov 2023), Space Gray; catalog SKU MTL73SA/A | Kyu3a | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

These optimized derivatives remain under CC BY-SA 4.0. The manifest contains original file URLs,
source page URLs, original and derivative SHA-256 checksums, source dimensions, author,
license, model evidence and modification notices. Runtime cards display source/author/license links.

Images are resized proportionally to at most 1000 pixels, encoded WebP at quality 84, without
cropping, generated content, color replacement or background removal. Combined payload: 61,206 bytes.
Photos verify the physical model/generation and visible color, not the RAM/SSD inside an individual machine.
The M3 photo has a Japanese keyboard; this distinction is recorded in its manifest note.

## Sources

- [MacBook Air A2681 photo and license](https://commons.wikimedia.org/wiki/File:MacBook_Air_(A2681)_front.jpg)
- [MacBook Pro 14-inch M3 Space Gray photo and license](https://commons.wikimedia.org/wiki/File:M3_Macbook_Pro_14_inch_Space_Grey_model.jpg)
- [Apple MacBook Pro model/part-number identification](https://support.apple.com/en-us/108052)
- [Apple MacBook Air M2 technical specifications](https://support.apple.com/kb/SP869)
- [MLY03 Silver product listing used for SKU/color cross-check](https://toolhome.co.za/products/apple-macbook-air-13-inch-with-m2-chip-8-core-cpu-and-10-core-gpu-512gb-ssd-silver)

## Coverage, checked 2026-10-25 (Asia/Bangkok)

`data/laptop_images.json` has exactly 225 entries, keyed by the full unique catalog name;
`laptop_key` repeats that key for validation. Auto-increment database IDs and ambiguous family names
are not mapping keys. `data/image_audit_summary.json` records the totals.

| Verification state | Laptop records |
| --- | ---: |
| `verified` | 2 |
| `model_unverified` | 118 |
| `rights_unconfirmed` | 1 |
| `source_mismatch` | 13 |
| `source_unavailable` | 91 |

The first 10 catalog entries were the pilot. None passed both model-specific image verification
and redistribution permission. The process was then extended to all 225 records (175 distinct existing
source URLs). HTTP outcomes across the 225 records: 134 returned 200, 38 returned 403, 31 returned 404,
22 timed out or had network errors. HTTP 200 alone is never treated as image verification.

Pilot examples: UX3405 pages mix MA/CA generations; UM3406 contains HA/GA variants; UX8406 redirects
to a category; K3405/K3605 redirect to the homepage. UX5304MA is identified on the page but image
redistribution rights are unconfirmed. Full individual reasons, resolved URLs and source titles
are recorded in the manifest. The existing source/training CSVs are intentionally unchanged.

Some Apple source URLs in the original dataset now return iPhone pages or another Mac model.
They are marked as source mismatches. An available M1 Gold photo and a 15-inch M2 Starlight photo
were rejected for catalog SKUs with a different or unverified color. No photo was substituted across
M2/M3 generations or Air/Pro screen sizes. Unverified images are not downloaded into this directory.

## Add another photo

1. Open the exact manufacturer/product source and verify model code, generation, screen size and visible color.
2. Confirm redistribution permission; record its evidence/URL. Being publicly accessible is insufficient.
3. Save a permitted original outside the repository, then run:

   ```powershell
   python tools/optimize_product_image.py C:\path\permitted-original.jpg unique-model-code.webp
   ```

4. Update only the matching full-name entry in `data/laptop_images.json`. Required fields for display:
   `verification_status: verified`, `path`, `source_url`, `image_url`, `model_source_url`,
   `model_evidence`, `author`, `license`, `license_url`, `alt`, `sha256`, `checked_date`, and `modifications`.
   Copy the tool's checksum and keep the original download URL observed on the source page.
5. Recalculate the audit summary and run `python tools/check_product_images.py` and the tests.

The optimizer does not assert model identity, permission or mark an entry as verified.
Duplicate JSON keys (including case/whitespace/Unicode-normalization collisions) are rejected.
Only verified local assets confined to this directory are served as product photographs.
The shared image component supplies a labeled placeholder, alt text, lazy loading, and broken-image fallback.
