import os
import sys
import math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Chạy backend không GUI cho Flask
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from src.data_cleaning import load_data, clean_data

# Danh sách các thông số định lượng cốt lõi cần phân tích
NUM_COLS = [
    'price', 'ram', 'storage', 'cpu_score', 
    'gpu_score', 'screen_size', 'refresh_rate', 
    'weight', 'battery'
]

# Danh sách các cột số dùng cho phân tích phân cụm K-Means và tương thích
NUMERIC_COLS = [
    'cpu_score', 'gpu_score', 'ram', 'storage', 
    'screen_size', 'refresh_rate', 'weight', 'battery', 
    'rating', 'price', 'units_sold'
]

# Tên hiển thị tiếng Việt gần gũi, rõ ràng
COL_LABELS = {
    'price': 'Giá bán (VND)',
    'ram': 'RAM (GB)',
    'storage': 'Ổ cứng (GB)',
    'cpu_score': 'Điểm CPU',
    'gpu_score': 'Điểm GPU',
    'screen_size': 'Màn hình (inch)',
    'refresh_rate': 'Tần số quét (Hz)',
    'weight': 'Trọng lượng (kg)',
    'battery': 'Pin (Wh)'
}

# Metadata phục vụ vẽ biểu đồ và hiển thị đơn vị
COL_META = {
    'price': {'label': 'Giá bán (VND)', 'unit': 'VND', 'scale': 1, 'decimals': 0},
    'ram': {'label': 'RAM (GB)', 'unit': 'GB', 'scale': 1, 'decimals': 1},
    'storage': {'label': 'Ổ cứng (GB)', 'unit': 'GB', 'scale': 1, 'decimals': 0},
    'cpu_score': {'label': 'Điểm hiệu năng CPU', 'unit': 'điểm', 'scale': 1, 'decimals': 1},
    'gpu_score': {'label': 'Điểm hiệu năng GPU', 'unit': 'điểm', 'scale': 1, 'decimals': 1},
    'screen_size': {'label': 'Kích thước màn hình (inch)', 'unit': 'inch', 'scale': 1, 'decimals': 1},
    'refresh_rate': {'label': 'Tần số quét màn hình (Hz)', 'unit': 'Hz', 'scale': 1, 'decimals': 1},
    'weight': {'label': 'Trọng lượng máy (kg)', 'unit': 'kg', 'scale': 1, 'decimals': 2},
    'battery': {'label': 'Dung lượng pin (Wh)', 'unit': 'Wh', 'scale': 1, 'decimals': 1}
}

def _safe_float(val):
    """Chuyển numpy float/int sang Python float an toàn, NaN -> None."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    try:
        f = float(val)
        return None if math.isnan(f) else f
    except (TypeError, ValueError):
        return None

def compute_split_apply_combine(df, num_cols=None):
    """
    Phân nhóm và tổng hợp dữ liệu thống kê theo từng hãng và toàn bộ thị trường.
    Tính toán Trung bình, Trung vị, Độ lệch chuẩn và Số lượng mẫu.
    """
    if num_cols is None:
        num_cols = NUM_COLS

    # 1. Thống kê theo từng thương hiệu
    brand_stats_df = df.groupby('brand')[num_cols].agg(['mean', 'median', 'std', 'count']).round(2)
    
    # 2. Thống kê chung toàn bộ thị trường
    overall_stats_df = df[num_cols].agg(['mean', 'median', 'std', 'count']).round(2).T.reset_index()
    overall_stats_df.rename(columns={'index': 'feature'}, inplace=True)
    overall_stats_df['brand'] = 'Toàn bộ'
    
    # Chuyển bảng thống kê hãng sang dạng phẳng
    try:
        brand_flat = brand_stats_df.stack(level=0, future_stack=True).reset_index()
    except Exception:
        brand_flat = brand_stats_df.stack(level=0).reset_index()
        
    brand_flat.rename(columns={'level_1': 'feature'}, inplace=True)
    
    full_stats_df = pd.concat([overall_stats_df, brand_flat], ignore_index=True)
    
    # Lưu file kết quả chuẩn hóa (hỗ trợ cả kết quả cũ và mới)
    os.makedirs('data', exist_ok=True)
    full_stats_df.to_csv('data/laptop_results.csv', index=False, encoding='utf-8-sig')
    full_stats_df.to_csv('data/results2.csv', index=False, encoding='utf-8-sig')
    
    return full_stats_df.to_dict(orient='records')

def find_best_value_laptops(df, top_n=5):
    """
    Đánh giá Top Laptop có tỷ lệ 'Hiệu năng trên giá thành' (P/P - Price/Performance) tốt nhất.
    Sử dụng chuẩn hóa độ lệch hiệu năng CPU và mức giá để tìm ra những model đáng tiền nhất.
    """
    df_eval = df.dropna(subset=['price', 'cpu_score']).copy()
    if df_eval.empty:
        return []
        
    p_mean = df_eval['price'].mean()
    p_std = df_eval['price'].std()
    c_mean = df_eval['cpu_score'].mean()
    c_std = df_eval['cpu_score'].std()
    
    # Chuẩn hóa độ lệch giá và hiệu năng
    df_eval['price_norm'] = ((df_eval['price'] - p_mean) / (p_std if p_std else 1.0)).round(2)
    df_eval['cpu_norm'] = ((df_eval['cpu_score'] - c_mean) / (c_std if c_std else 1.0)).round(2)
    
    # Chỉ số giá trị P/P: Hiệu năng càng cao, giá càng tốt thì điểm càng lớn
    df_eval['value_score'] = (df_eval['cpu_norm'] - df_eval['price_norm']).round(2)
    
    top_value = df_eval.sort_values(by='value_score', ascending=False).head(top_n)
    return top_value.to_dict(orient='records')

def compute_eda(df):
    """
    Tổng hợp toàn bộ dữ liệu thống kê thị trường:
    - Top/Bottom 3 của từng thông số
    - Bảng thống kê theo từng hãng và toàn thị trường
    - Hãng dẫn đầu từng tiêu chí
    - Phân khúc và xếp hạng giá các thương hiệu
    - Danh sách laptop tối ưu chi phí (món hời)
    """
    for col in NUM_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 1. Top 3 cao nhất và thấp nhất theo từng thông số
    top_bottom = {}
    for col in NUM_COLS:
        valid = df.dropna(subset=[col])
        top3 = valid.nlargest(3, col)[['name', 'brand', col]].to_dict('records')
        bottom3 = valid.nsmallest(3, col)[['name', 'brand', col]].to_dict('records')
        for item in top3 + bottom3:
            item[col] = _safe_float(item[col])
        top_bottom[col] = {'top3': top3, 'bottom3': bottom3}

    # 2. Thống kê phân nhóm theo hãng và toàn bộ
    stats_rows = compute_split_apply_combine(df, NUM_COLS)
    for r in stats_rows:
        r['mean'] = _safe_float(r['mean'])
        r['median'] = _safe_float(r['median'])
        r['std'] = _safe_float(r['std'])
        r['count'] = int(r['count']) if r['count'] is not None and not math.isnan(r['count']) else 0

    brands = sorted([b for b in df['brand'].dropna().unique()])

    # 3. Thương hiệu dẫn đầu từng thông số
    leaders = {}
    brand_only = [r for r in stats_rows if r['brand'] != 'Toàn bộ']
    for col in NUM_COLS:
        col_rows = [r for r in brand_only if r['feature'] == col and r['mean'] is not None]
        if col_rows:
            best = max(col_rows, key=lambda x: x['mean'])
            leaders[col] = {
                'brand': best['brand'],
                'mean': best['mean'],
                'median': best['median']
            }

    # 4. Đánh giá & xếp hạng thương hiệu
    brand_lead_count = {}
    for col, info in leaders.items():
        b = info['brand']
        brand_lead_count[b] = brand_lead_count.get(b, 0) + 1
    brand_lead_sorted = sorted(brand_lead_count.items(), key=lambda x: -x[1])

    price_stats_by_brand = {}
    for r in brand_only:
        if r['feature'] == 'price' and r['mean'] is not None:
            price_stats_by_brand[r['brand']] = {
                'mean': r['mean'], 'median': r['median'], 'std': r['std']
            }

    sorted_by_price_mean = sorted(price_stats_by_brand.items(), key=lambda x: x[1]['mean'])
    sorted_by_price_std = sorted(
        [(b, v) for b, v in price_stats_by_brand.items() if v['std'] is not None],
        key=lambda x: x[1]['std'], reverse=True
    )

    evaluation = {
        'brand_lead_count': brand_lead_sorted,
        'total_criteria': len(NUM_COLS),
        'price_ranking': [
            {'brand': b, 'mean': v['mean'], 'median': v['median'], 'std': v['std']}
            for b, v in sorted_by_price_mean
        ],
        'most_diverse': sorted_by_price_std[0] if sorted_by_price_std else None,
        'premium_brands': [b for b, v in sorted_by_price_mean if v['mean'] and v['mean'] >= 35_000_000],
        'budget_brands': [b for b, v in sorted_by_price_mean if v['mean'] and v['mean'] <= 20_000_000],
    }

    # 5. Top laptop tối ưu giá trị nhất (P/P)
    best_value_laptops = find_best_value_laptops(df, top_n=5)

    return top_bottom, stats_rows, leaders, evaluation, brands, best_value_laptops

def get_top_bottom(df, column, n=3):
    """Hàm tương thích ngược: Lấy Top n và Bottom n của một cột."""
    top_n = df.nlargest(n, column)[['name', 'brand', column]].to_dict(orient='records')
    bottom_n = df.nsmallest(n, column)[['name', 'brand', column]].to_dict(orient='records')
    return top_n, bottom_n

def calculate_statistics(df):
    """Hàm tương thích ngược: Tính toán thống kê và lưu kết quả."""
    return compute_split_apply_combine(df, NUM_COLS)

def create_charts(df):
    """
    Tạo toàn bộ hệ thống biểu đồ phân tích thị trường và lưu vào static/charts/:
    1. Biểu đồ phân bố tần suất toàn thị trường (Overall Distribution) cho từng thông số.
    2. Biểu đồ phân bố theo từng thương hiệu (Distribution by Brand).
    3. Biểu đồ phân tích ảnh hưởng phần cứng lên giá bán (Hardware vs Price - 4 góc).
    4. Các biểu đồ bổ trợ tương thích ngược.
    """
    os.makedirs('static/charts', exist_ok=True)
    os.makedirs('charts', exist_ok=True)
    
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    # Đảm bảo các cột số hợp lệ
    for col in NUM_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # A. Biểu đồ phân bố toàn thị trường
    for col in NUM_COLS:
        meta = COL_META.get(col, {'label': col, 'unit': '', 'scale': 1, 'decimals': 1})
        s = df[col].dropna() * meta['scale']
        if s.empty:
            continue
            
        mean_val = s.mean()
        median_val = s.median()
        
        plt.figure(figsize=(9, 5.2))
        sns.histplot(s, kde=True, bins=15, color='#2563eb', edgecolor='black', alpha=0.55)
        
        # Đường tham chiếu Trung bình & Trung vị
        plt.axvline(mean_val, color='#dc2626', linestyle='--', linewidth=2, 
                    label=f'Trung bình: {mean_val:.{meta["decimals"]}f} {meta["unit"]}')
        plt.axvline(median_val, color='#16a34a', linestyle='-', linewidth=2, 
                    label=f'Trung vị: {median_val:.{meta["decimals"]}f} {meta["unit"]}')
        
        plt.title(f'Phân bố toàn thị trường: {meta["label"]}', fontsize=13, fontweight='bold', pad=12)
        plt.xlabel(meta['label'], fontsize=11, fontweight='600')
        plt.ylabel('Số lượng laptop', fontsize=11, fontweight='600')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper right', fontsize=10)
        plt.tight_layout()
        
        plt.savefig(f'static/charts/hist_overall_{col}.png', dpi=150)
        plt.savefig(f'static/charts/{col}_histogram.png', dpi=150)  # Tương thích tên cũ
        plt.close()

    # B. Biểu đồ phân bố theo từng thương hiệu
    for col in NUM_COLS:
        meta = COL_META.get(col, {'label': col, 'unit': '', 'scale': 1, 'decimals': 1})
        plot_df = df.dropna(subset=[col, 'brand']).copy()
        plot_df[col] = plot_df[col] * meta['scale']
        
        brand_counts = plot_df['brand'].value_counts()
        valid_brands = brand_counts[brand_counts >= 2].index
        plot_df = plot_df[plot_df['brand'].isin(valid_brands)]
        
        if plot_df.empty:
            continue
            
        brand_order = plot_df.groupby('brand')[col].median().sort_values(ascending=False).index.tolist()
        n_brands = len(brand_order)
        ncols = 3
        nrows = math.ceil(n_brands / ncols)
        
        fig, axes = plt.subplots(nrows, ncols, figsize=(14, max(4, nrows * 3.2)), sharex=True)
        axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
        
        palette = sns.color_palette('tab10', n_brands)
        
        for i, b in enumerate(brand_order):
            ax = axes[i]
            data_b = plot_df[plot_df['brand'] == b][col]
            mean_b = data_b.mean()
            median_b = data_b.median()
            
            sns.histplot(data_b, kde=True, ax=ax, color=palette[i % len(palette)], edgecolor='black', alpha=0.55)
            ax.axvline(mean_b, color='#dc2626', linestyle='--', linewidth=1.5, label=f'Mean: {mean_b:.{meta["decimals"]}f}')
            ax.axvline(median_b, color='#16a34a', linestyle='-', linewidth=1.5, label=f'Median: {median_b:.{meta["decimals"]}f}')
            
            ax.set_title(f'Hãng: {b} ({len(data_b)} sản phẩm)', fontsize=11, fontweight='bold')
            ax.set_xlabel(meta['label'] if i >= n_brands - ncols else '', fontsize=10)
            ax.set_ylabel('Số máy', fontsize=9)
            ax.legend(fontsize=8, loc='upper right')
            ax.grid(axis='y', linestyle='--', alpha=0.5)
        
        for j in range(n_brands, len(axes)):
            fig.delaxes(axes[j])
            
        fig.suptitle(f'Phân bố theo từng hãng: {meta["label"]}', fontsize=14, fontweight='bold', y=1.002)
        plt.tight_layout()
        plt.savefig(f'static/charts/hist_by_brand_{col}.png', dpi=150, bbox_inches='tight')
        plt.close()

    # C. Biểu đồ phân tích ảnh hưởng phần cứng lên giá bán (4 góc)
    hw_df = df[['price', 'cpu_score', 'gpu_score', 'ram']].dropna().copy()
    for c in hw_df.columns:
        hw_df[c] = pd.to_numeric(hw_df[c], errors='coerce')
    hw_df = hw_df.dropna()

    def vnd_formatter(x, pos):
        return f'{x / 1e6:.0f} tr'

    if not hw_df.empty:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Phân tích ảnh hưởng của cấu hình phần cứng lên mức giá bán laptop',
                     fontsize=15, fontweight='bold', y=0.98)

        # 1. CPU vs Price
        ax1 = axes[0, 0]
        ax1.scatter(hw_df['cpu_score'], hw_df['price'],
                    color='#7c3aed', alpha=0.6, edgecolors='black', linewidth=0.5, s=50)
        ax1.set_title('Tương quan Điểm CPU và Giá bán', fontsize=13, fontweight='bold', pad=10)
        ax1.set_xlabel('Điểm hiệu năng CPU (PassMark)', fontsize=11, fontweight='600')
        ax1.set_ylabel('Giá bán (triệu VNĐ)', fontsize=11, fontweight='600')
        ax1.yaxis.set_major_formatter(FuncFormatter(vnd_formatter))
        ax1.grid(True, linestyle='--', alpha=0.4)

        # 2. GPU vs Price
        ax2 = axes[0, 1]
        ax2.scatter(hw_df['gpu_score'], hw_df['price'],
                    color='#10b981', alpha=0.6, edgecolors='black', linewidth=0.5, s=50)
        ax2.set_title('Tương quan Điểm GPU và Giá bán', fontsize=13, fontweight='bold', pad=10)
        ax2.set_xlabel('Điểm hiệu năng GPU (PassMark G3D)', fontsize=11, fontweight='600')
        ax2.set_ylabel('Giá bán (triệu VNĐ)', fontsize=11, fontweight='600')
        ax2.yaxis.set_major_formatter(FuncFormatter(vnd_formatter))
        ax2.grid(True, linestyle='--', alpha=0.4)

        # 3. RAM vs Price
        ax3 = axes[1, 0]
        ram_order = sorted(hw_df['ram'].unique())
        sns.boxplot(data=hw_df, x='ram', y='price', order=ram_order, ax=ax3,
                    boxprops=dict(edgecolor='black', facecolor='#f8fafc'),
                    medianprops=dict(color='#dc2626', linewidth=2),
                    whiskerprops=dict(color='black'),
                    capprops=dict(color='black'),
                    flierprops=dict(marker='o', markerfacecolor='gray', markersize=4, alpha=0.5))
        ax3.set_title('Khoảng giá theo dung lượng RAM', fontsize=13, fontweight='bold', pad=10)
        ax3.set_xlabel('Dung lượng RAM (GB)', fontsize=11, fontweight='600')
        ax3.set_ylabel('Giá bán (triệu VNĐ)', fontsize=11, fontweight='600')
        ax3.yaxis.set_major_formatter(FuncFormatter(vnd_formatter))
        ax3.grid(axis='y', linestyle='--', alpha=0.4)

        # 4. Correlation Heatmap
        ax4 = axes[1, 1]
        corr_cols = ['price', 'cpu_score', 'gpu_score', 'ram']
        corr_labels = ['Giá bán', 'Điểm CPU', 'Điểm GPU', 'RAM (GB)']
        corr_matrix = hw_df[corr_cols].corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                    xticklabels=corr_labels, yticklabels=corr_labels,
                    linewidths=0.8, linecolor='white', ax=ax4,
                    annot_kws={'fontsize': 11, 'fontweight': 'bold'})
        ax4.set_title('Ma trận tương quan giữa cấu hình và giá bán', fontsize=13, fontweight='bold', pad=10)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig('static/charts/hardware_vs_price_analysis.png', dpi=150, bbox_inches='tight')
        plt.close()

    # D. Các biểu đồ bổ sung phục vụ tương thích
    plt.figure(figsize=(10, 6))
    avg_price_brand = df.groupby('brand')['price'].mean().sort_values(ascending=False)
    avg_price_brand.plot(kind='bar', color='#f97316', edgecolor='black')
    plt.title('Giá trung bình theo thương hiệu', fontsize=13, fontweight='bold')
    plt.xlabel('Thương hiệu', fontsize=11)
    plt.ylabel('Giá trung bình (VND)', fontsize=11)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/charts/avg_price_by_brand.png', dpi=150)
    plt.close()

    print("[OK] Đã hoàn thành cập nhật toàn bộ biểu đồ thị trường!")
