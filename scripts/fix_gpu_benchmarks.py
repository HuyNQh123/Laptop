import urllib.request
import ssl
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# PassMark verified URLs and IDs
PASSMARK_GPU_VERIFIED = {
    'Intel UHD Graphics': (1450, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Intel+UHD+Graphics&id=3894'),
    'Intel Iris Xe Graphics': (2550, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Intel+Iris+Xe&id=4265'),
    'Intel Arc Graphics': (4150, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Intel+Arc+A350M&id=4553'),
    'AMD Radeon 610M': (1150, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+610M&id=4730'),
    'AMD Radeon Vega 7': (1750, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+Vega+7&id=4359'),
    'AMD Radeon Vega 8': (1980, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+Vega+8&id=3895'),
    'AMD Radeon 660M': (2450, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+660M&id=4641'),
    'AMD Radeon 680M': (3650, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+680M&id=4574'),
    'AMD Radeon 760M': (3580, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+760M&id=4842'),
    'AMD Radeon 780M': (4650, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+780M&id=4818'),
    'AMD Radeon RX 6550M': (6250, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+RX+6550M&id=4802'),
    'AMD Radeon RX 7600S': (11800, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+RX+7600S&id=4814'),
    'NVIDIA GeForce MX450': (3250, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+MX450&id=4296'),
    'NVIDIA GeForce MX550': (4850, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+MX550&id=4544'),
    'NVIDIA GeForce GTX 1650': (6850, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+GTX+1650+(Mobile)&id=4090'),
    'NVIDIA GeForce RTX 2050': (7450, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+2050&id=4584'),
    'NVIDIA GeForce RTX 3050 Laptop': (9850, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+3050+Laptop+GPU&id=4408'),
    'NVIDIA GeForce RTX 3050 Ti Laptop': (10950, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+3050+Ti+Laptop+GPU&id=4413'),
    'NVIDIA GeForce RTX 3060 Laptop': (13200, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+3060+Laptop+GPU&id=4342'),
    'NVIDIA GeForce RTX 3070 Laptop': (15400, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+3070+Laptop+GPU&id=4331'),
    'NVIDIA GeForce RTX 3070 Ti Laptop': (16800, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+3070+Ti+Laptop+GPU&id=4521'),
    'NVIDIA GeForce RTX 3080 Laptop': (17600, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+3080+Laptop+GPU&id=4344'),
    'NVIDIA GeForce RTX 4050 Laptop': (14350, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+4050+Laptop+GPU&id=4763'),
    'NVIDIA GeForce RTX 4060 Laptop': (17450, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+4060+Laptop+GPU&id=4752'),
    'NVIDIA GeForce RTX 4070 Laptop': (19650, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+4070+Laptop+GPU&id=4756'),
    'NVIDIA GeForce RTX 4080 Laptop': (24350, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+4080+Laptop+GPU&id=4736'),
    'NVIDIA GeForce RTX 4090 Laptop': (28750, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+RTX+4090+Laptop+GPU&id=4737'),
    'NVIDIA RTX A1000 Laptop': (9150, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=RTX+A1000+Laptop+GPU&id=4610'),
    'NVIDIA RTX 2000 Ada Laptop': (14100, 'PassMark G3D Mark', 'https://www.videocardbenchmark.net/gpu.php?gpu=RTX+2000+Ada+Generation+Laptop+GPU&id=4824'),
    # Apple Silicon: PassMark tracks them as SoC on cpubenchmark.net
    'Apple M1 GPU (7-core)': (3150, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M1+8+Core+3200+MHz&id=4104'),
    'Apple M1 GPU (8-core)': (3550, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M1+8+Core+3200+MHz&id=4104'),
    'Apple M2 GPU (8-core)': (3950, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M2+8+Core+3500+MHz&id=4795'),
    'Apple M2 GPU (10-core)': (4850, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M2+8+Core+3500+MHz&id=4795'),
    'Apple M2 Pro GPU (16-core)': (8600, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M2+Pro+10+Core+3500+MHz&id=5242'),
    'Apple M2 Pro GPU (19-core)': (9850, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M2+Pro+12+Core+3500+MHz&id=5166'),
    'Apple M2 Max GPU (30-core)': (14200, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M2+Max+12+Core+3700+MHz&id=5201'),
    'Apple M3 GPU (8-core)': (4500, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M3+8+Core&id=5755'),
    'Apple M3 GPU (10-core)': (5650, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M3+8+Core&id=5755'),
    'Apple M3 Pro GPU (14-core)': (9400, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M3+Pro+11+Core&id=5759'),
    'Apple M3 Pro GPU (18-core)': (11800, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M3+Pro+12+Core&id=5770'),
    'Apple M3 Max GPU (30-core)': (18500, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M3+Max+14+Core&id=5774'),
    'Apple M3 Max GPU (40-core)': (23400, 'PassMark Metal Score (Quy đổi)', 'https://www.cpubenchmark.net/cpu.php?cpu=Apple+M3+Max+16+Core&id=5775'),
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8'
}

print("Testing all 39 PassMark GPU URLs...")
success = 0
for gpu_name, (score, bench_name, url) in PASSMARK_GPU_VERIFIED.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            code = r.status
            final_url = r.geturl()
            html = r.read(10000).decode('utf-8', errors='ignore')
            m = re.search(r'<title>(.*?)</title>', html, re.I)
            t = m.group(1).strip() if m else ''
            print(f"[OK {code}] {gpu_name} -> {t[:60]}")
            success += 1
    except Exception as e:
        print(f"[ERR] {gpu_name} ({url}) -> {e}")

print(f"\nResult: {success} / {len(PASSMARK_GPU_VERIFIED)} URLs OK!")
