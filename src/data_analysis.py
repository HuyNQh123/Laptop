import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Cần thiết để matplotlib không gọi GUI khi chạy qua Flask
import matplotlib.pyplot as plt
import os

from src.data_cleaning import load_data, clean_data

# Danh sách các cột số cần tính toán
NUMERIC_COLS = ['cpu_score', 'gpu_score', 'ram', 'storage', 'screen_size', 'refresh_rate', 'weight', 'battery', 'rating', 'price', 'units_sold']

def get_top_bottom(df, column, n=3):
    """Lấy Top n và Bottom n của một cột."""
    top_n = df.nlargest(n, column)[['name', 'brand', column]].to_dict(orient='records')
    bottom_n = df.nsmallest(n, column)[['name', 'brand', column]].to_dict(orient='records')
    return top_n, bottom_n

def calculate_statistics(df):
    """Tính toán mean, median, std cho toàn dataset và theo brand, lưu kết quả ra CSV."""
    
    # 1. Tính cho toàn bộ dataset
    all_stats = df[NUMERIC_COLS].agg(['mean', 'median', 'std'])
    all_stats['group'] = 'all'
    all_stats['statistic'] = all_stats.index
    
    # 2. Tính theo từng brand
    brand_stats_list = []
    brands = df['brand'].unique()
    
    for brand in brands:
        brand_df = df[df['brand'] == brand]
        if not brand_df.empty:
            b_stats = brand_df[NUMERIC_COLS].agg(['mean', 'median', 'std'])
            b_stats['group'] = brand
            b_stats['statistic'] = b_stats.index
            brand_stats_list.append(b_stats)
            
    # Kết hợp lại
    final_stats = pd.concat([all_stats] + brand_stats_list, ignore_index=True)
    
    # Sắp xếp lại thứ tự cột cho giống format yêu cầu
    cols = ['group', 'statistic'] + NUMERIC_COLS
    final_stats = final_stats[cols]
    
    # Lưu ra file CSV
    os.makedirs('data', exist_ok=True)
    final_stats.to_csv('data/results2.csv', index=False)
    print("Đã lưu kết quả thống kê vào data/results2.csv")
    
    return final_stats

def create_charts(df):
    """Tạo các biểu đồ phân tích và lưu vào thư mục static/charts/."""
    os.makedirs('static/charts', exist_ok=True)
    
    # 1. Histogram cho các cột numeric
    for col in NUMERIC_COLS:
        plt.figure(figsize=(8, 5))
        plt.hist(df[col].dropna(), bins=20, color='skyblue', edgecolor='black')
        plt.title(f'Histogram of {col.replace("_", " ").title()}')
        plt.xlabel(col.replace("_", " ").title())
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(f'static/charts/{col}_histogram.png')
        plt.close()
        
    # 2. Average Price by Brand
    plt.figure(figsize=(10, 6))
    avg_price_brand = df.groupby('brand')['price'].mean().sort_values(ascending=False)
    avg_price_brand.plot(kind='bar', color='coral', edgecolor='black')
    plt.title('Average Price by Brand')
    plt.xlabel('Brand')
    plt.ylabel('Average Price (VND)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/charts/avg_price_by_brand.png')
    plt.close()
    
    # 3. CPU Score vs Price
    plt.figure(figsize=(8, 5))
    plt.scatter(df['cpu_score'], df['price'], alpha=0.6, color='purple')
    plt.title('CPU Score vs Price')
    plt.xlabel('CPU Score')
    plt.ylabel('Price (VND)')
    plt.tight_layout()
    plt.savefig('static/charts/cpu_vs_price.png')
    plt.close()
    
    # 4. GPU Score vs Price
    plt.figure(figsize=(8, 5))
    plt.scatter(df['gpu_score'], df['price'], alpha=0.6, color='green')
    plt.title('GPU Score vs Price')
    plt.xlabel('GPU Score')
    plt.ylabel('Price (VND)')
    plt.tight_layout()
    plt.savefig('static/charts/gpu_vs_price.png')
    plt.close()
    
    # 5. RAM vs Price
    plt.figure(figsize=(8, 5))
    # Sử dụng boxplot sẽ thể hiện mức giá phân bổ theo từng mốc RAM rõ hơn
    df.boxplot(column='price', by='ram', grid=False, figsize=(8,5))
    plt.title('Price Distribution by RAM')
    plt.suptitle('') # Xóa title mặc định của pandas boxplot
    plt.xlabel('RAM (GB)')
    plt.ylabel('Price (VND)')
    plt.tight_layout()
    plt.savefig('static/charts/ram_vs_price.png')
    plt.close()
    
    print("Đã tạo và lưu các biểu đồ vào thư mục static/charts/")

if __name__ == '__main__':
    print("Bắt đầu test Data Analysis...")
    df_raw = load_data('data/laptops.csv')
    if df_raw is not None:
        df_clean = clean_data(df_raw)
        print(f"Tổng số laptop: {len(df_clean)}")
        print(f"Tổng số brand: {df_clean['brand'].nunique()}")
        
        # Test Tính toán thống kê & Lưu CSV
        calculate_statistics(df_clean)
        
        # Test Top/Bottom Price
        top_price, bottom_price = get_top_bottom(df_clean, 'price', 3)
        print("\nTop 3 đắt nhất:")
        for idx, row in enumerate(top_price):
            print(f"{idx+1}. {row['name']} ({row['brand']}) - {row['price']:,.0f} VND")
            
        print("\nBottom 3 rẻ nhất:")
        for idx, row in enumerate(bottom_price):
            print(f"{idx+1}. {row['name']} ({row['brand']}) - {row['price']:,.0f} VND")
            
        # Test Tạo Charts
        create_charts(df_clean)
        print("Data Analysis module hoạt động hoàn hảo!")
