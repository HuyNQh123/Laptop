import pandas as pd
import numpy as np
import random

def generate_laptops():
    brands = ['ASUS', 'Dell', 'Lenovo', 'HP', 'Acer', 'MSI', 'Apple']
    
    data = []
    for i in range(250):
        brand = random.choice(brands)
        
        # Phân khúc laptop (1: Giá rẻ, 2: Tầm trung, 3: Cao cấp, 4: Gaming)
        if brand == 'Apple':
            category = random.choice([2, 3]) 
        elif brand == 'MSI':
            category = random.choice([3, 4])
        else:
            category = random.choice([1, 2, 3, 4])
            
        if category == 1:
            cpu = random.choice(['Intel Core i3', 'AMD Ryzen 3'])
            cpu_score = random.randint(3000, 6000)
            gpu = 'Integrated'
            gpu_score = random.randint(500, 1500)
            ram = random.choice([4, 8])
            storage = random.choice([256, 512])
            screen_size = random.choice([14.0, 15.6])
            refresh_rate = 60
            weight = round(random.uniform(1.5, 1.8), 2)
            battery = random.randint(35, 45)
            price = random.randint(8000000, 12000000)
            rating = round(random.uniform(3.5, 4.2), 1)
            
        elif category == 2:
            cpu = random.choice(['Intel Core i5', 'AMD Ryzen 5'])
            cpu_score = random.randint(8000, 12000)
            gpu = random.choice(['Integrated', 'NVIDIA MX450', 'Intel Iris Xe'])
            gpu_score = random.randint(1500, 3000)
            ram = random.choice([8, 16])
            storage = 512
            screen_size = random.choice([14.0, 15.6])
            refresh_rate = 60
            weight = round(random.uniform(1.4, 1.7), 2)
            battery = random.randint(45, 60)
            price = random.randint(13000000, 20000000)
            rating = round(random.uniform(4.0, 4.6), 1)
            
        elif category == 3:
            cpu = random.choice(['Intel Core i7', 'AMD Ryzen 7', 'Apple M1', 'Apple M2']) if brand == 'Apple' else random.choice(['Intel Core i7', 'AMD Ryzen 7'])
            cpu_score = random.randint(13000, 18000)
            gpu = random.choice(['Integrated', 'NVIDIA RTX 3050', 'Intel Iris Xe']) if brand != 'Apple' else 'Apple GPU'
            gpu_score = random.randint(3000, 7000)
            ram = random.choice([16, 32])
            storage = random.choice([512, 1024])
            screen_size = random.choice([13.3, 14.0, 15.6, 16.0])
            refresh_rate = random.choice([60, 90, 120])
            weight = round(random.uniform(1.2, 1.9), 2)
            battery = random.randint(55, 80)
            price = random.randint(22000000, 45000000)
            rating = round(random.uniform(4.4, 4.9), 1)
            
        else: # Gaming
            cpu = random.choice(['Intel Core i7', 'AMD Ryzen 7', 'Intel Core i9', 'AMD Ryzen 9'])
            cpu_score = random.randint(16000, 25000)
            gpu = random.choice(['NVIDIA RTX 3060', 'NVIDIA RTX 3070', 'NVIDIA RTX 4060', 'NVIDIA RTX 4070'])
            gpu_score = random.randint(8000, 16000)
            ram = random.choice([16, 32, 64])
            storage = random.choice([512, 1024, 2048])
            screen_size = random.choice([15.6, 16.0, 17.3])
            refresh_rate = random.choice([120, 144, 165, 240])
            weight = round(random.uniform(2.0, 2.8), 2)
            battery = random.randint(60, 99)
            price = random.randint(25000000, 60000000)
            rating = round(random.uniform(4.2, 4.8), 1)

        resolution = random.choice(["1920x1080", "2560x1440", "2560x1600", "3840x2160"])
        os = 'macOS' if brand == 'Apple' else random.choice(['Windows 11', 'Windows 10', 'No OS'])
        units_sold = random.randint(50, 5000)
        
        # Thỉnh thoảng tạo dữ liệu missing hoặc chuỗi để test cleaning (10% cơ hội)
        if random.random() < 0.1:
            ram = str(ram) + "GB" # Test cleaning
        if random.random() < 0.05:
            price = None # Test missing value
        if random.random() < 0.05:
            brand = brand.lower() # Test normalize brand

        data.append({
            'name': f"{brand} Laptop Model {i}",
            'brand': brand,
            'cpu': cpu,
            'cpu_score': cpu_score,
            'gpu': gpu,
            'gpu_score': gpu_score,
            'ram': ram,
            'storage': storage,
            'screen_size': screen_size,
            'resolution': resolution,
            'refresh_rate': refresh_rate,
            'weight': weight,
            'battery': battery,
            'operating_system': os,
            'rating': rating,
            'price': price,
            'units_sold': units_sold
        })
        
    df = pd.DataFrame(data)
    
    # Thêm 5 dòng duplicate để test remove_duplicates
    duplicates = df.sample(5)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    df.to_csv('data/laptops.csv', index=False)
    print(f"Generated data/laptops.csv with {len(df)} rows.")

if __name__ == '__main__':
    generate_laptops()
