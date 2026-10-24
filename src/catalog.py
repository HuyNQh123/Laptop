"""Presentation helpers; does not alter the dataset or ML pipeline."""
import math
import unicodedata
from src.product_images import image_metadata

SORT_FIELDS = {
    'id': 'Thứ tự ban đầu', 'name': 'Tên laptop', 'brand': 'Thương hiệu',
    'cpu': 'CPU', 'cpu_score': 'Điểm CPU', 'gpu': 'GPU', 'gpu_score': 'Điểm GPU',
    'ram': 'RAM', 'storage': 'Lưu trữ', 'screen_size': 'Màn hình',
    'refresh_rate': 'Tần số quét', 'weight': 'Trọng lượng', 'battery': 'Pin',
    'rating': 'Đánh giá', 'price': 'Giá tham khảo',
}
QUICK_FILTERS = {
    'all': 'Tất cả', 'budget': 'Đến 20 triệu', 'light': 'Đến 1,5 kg',
    'gaming': 'Điểm GPU từ 7.000', 'ram16': 'RAM từ 16 GB', 'apple': 'Apple MacBook',
}

def normalize(value):
    value = str(value).casefold().replace('đ', 'd')
    return ''.join(c for c in unicodedata.normalize('NFD', value)
                   if unicodedata.category(c) != 'Mn')

def product_view(row):
    row = dict(row)
    row.update(image_metadata(row['name']))
    return row

def catalog_context(rows, args):
    def integer(key, default):
        try:
            return int(args.get(key, default))
        except (ValueError, TypeError):
            return default
    state = {
        'q': args.get('q', '').strip()[:200], 'brand': args.get('brand', ''),
        'quick': args.get('quick', 'all'), 'budget': args.get('budget', ''),
        'ram': args.get('ram', ''), 'weight': args.get('weight', ''),
        'sort': args.get('sort', 'id'), 'direction': args.get('direction', 'asc'),
        'per_page': integer('per_page', 15),
    }
    if state['sort'] not in SORT_FIELDS:
        state['sort'] = 'id'
    if state['direction'] not in ('asc', 'desc'):
        state['direction'] = 'asc'
    if state['quick'] not in QUICK_FILTERS:
        state['quick'] = 'all'
    if state['per_page'] not in (10, 15, 25, 50, 100):
        state['per_page'] = 15
    budgets = {'15000000': 15000000, '20000000': 20000000, '30000000': 30000000, '40000000': 40000000}
    if state['budget'] not in budgets:
        state['budget'] = ''
    if state['ram'] not in ('8', '16', '32', '64'):
        state['ram'] = ''
    if state['weight'] not in ('1.5', '2'):
        state['weight'] = ''
    terms = normalize(state['q']).split()
    filtered = []
    for row in rows:
        haystack = normalize(' '.join(str(row.get(k, '')) for k in SORT_FIELDS))
        if not all(term in haystack for term in terms):
            continue
        if state['brand'] and row['brand'] != state['brand']:
            continue
        if state['budget'] and row['price'] > budgets[state['budget']]:
            continue
        if state['ram'] and row['ram'] < int(state['ram']):
            continue
        if state['weight'] and row['weight'] > float(state['weight']):
            continue
        quick = state['quick']
        if ((quick == 'budget' and row['price'] > 20000000)
            or (quick == 'light' and row['weight'] > 1.5)
            or (quick == 'gaming' and row['gpu_score'] < 7000)
            or (quick == 'ram16' and row['ram'] < 16)
            or (quick == 'apple' and row['brand'].lower() != 'apple')):
            continue
        filtered.append(row)
    key = state['sort']
    filtered.sort(key=lambda r: (r.get(key) is None, normalize(r[key]) if isinstance(r.get(key), str) else r.get(key, 0)),
                  reverse=state['direction'] == 'desc')
    total = len(filtered)
    pages = max(1, math.ceil(total / state['per_page']))
    page = min(max(1, integer('page', 1)), pages)
    start = (page - 1) * state['per_page']
    return dict(laptops=[product_view(r) for r in filtered[start:start + state['per_page']]],
                state=state, total=total, catalog_total=len(rows), page=page, pages=pages,
                start=start + 1 if total else 0, end=min(start + state['per_page'], total),
                brands=sorted({r['brand'] for r in rows}), sort_fields=SORT_FIELDS,
                quick_filters=QUICK_FILTERS)
