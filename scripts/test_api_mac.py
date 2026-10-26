import sys, os, urllib.request, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')
from app import app
from src.models import Laptop

with app.app_context():
    for query in ['%MacBook Air 13 M1%', '%Lenovo ThinkPad%', '%ASUS TUF%']:
        sample = Laptop.query.filter(Laptop.name.like(query)).first()
        if not sample: continue
        print(f"\n=== ID {sample.id}: {sample.name} ===")
        url = f"http://127.0.0.1:5000/api/laptop-sources/{sample.id}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            for s in data['sources']:
                print(f"  [{s['field_name']}] {s['source_name']}")
                print(f"     URL: {s['source_url'] if s['source_url'] else '(Đã ẩn theo Rule 5)'}")
                print(f"     Status: {s['status']}")
                print(f"     Note: {s['note']}")
