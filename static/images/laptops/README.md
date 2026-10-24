# Product photographs

Place permitted, verified product photographs here, preferably WebP, approximately 800×600 pixels.
Do not stretch or crop the laptop itself. The UI fits each image inside a 4:3 frame using `object-fit: contain`.

Add an entry in `data/laptop_images.json` keyed by the exact model/SKU name from the catalog:

```json
{
  "Exact model name and SKU": {
    "path": "images/laptops/model-sku.webp",
    "alt": "Tên máy và góc chụp",
    "source_url": "https://manufacturer.example/product",
    "license": "Permission or license reference",
    "verified_date": "YYYY-MM-DD"
  }
}
```

The manifest is empty intentionally: no unverified or generated product photos are presented as real products.
Missing entries/files use the local placeholder. Failed browser image loads also fall back to the placeholder.
Do not use database auto-increment IDs as image keys: reimports can change them.
