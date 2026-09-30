import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def create_radar_chart(df, laptop1_name, laptop2_name, attributes):
    """
    Tạo Radar Chart so sánh 2 laptop dựa trên các thuộc tính được chọn.
    """
    # 1. Kiểm tra thuộc tính
    missing_attrs = [attr for attr in attributes if attr not in df.columns]
    if missing_attrs:
        print(f"Lỗi: Các thuộc tính sau không tồn tại trong dataset: {missing_attrs}")
        return False
        
    # Lấy dữ liệu 2 laptop
    l1_row = df[df['name'] == laptop1_name]
    l2_row = df[df['name'] == laptop2_name]
    
    if l1_row.empty or l2_row.empty:
        print("Lỗi: Không tìm thấy laptop.")
        return False

    # 2. Normalize toàn bộ dataset cho các thuộc tính đã chọn (Min-Max)
    # Chúng ta phải scale dữ liệu để radar chart hiển thị các chỉ số trên cùng thang đo (0 - 1)
    df_norm = df[attributes].copy()
    
    for attr in attributes:
        # Chuyển đổi sang dạng số để tính toán an toàn
        df_norm[attr] = pd.to_numeric(df_norm[attr], errors='coerce')
        min_val = df_norm[attr].min()
        max_val = df_norm[attr].max()
        
        if pd.isna(min_val) or pd.isna(max_val):
            df_norm[attr] = 0
        elif max_val > min_val:
            df_norm[attr] = (df_norm[attr] - min_val) / (max_val - min_val)
        else:
            # Nếu min == max (ví dụ tất cả các máy có cùng 1 thông số)
            df_norm[attr] = 0.5
            
    # Lấy chỉ số đã được normalize của laptop 1 và laptop 2
    l1_idx = l1_row.index[0]
    l2_idx = l2_row.index[0]
    
    values1 = df_norm.loc[l1_idx, attributes].values.tolist()
    values2 = df_norm.loc[l2_idx, attributes].values.tolist()
    
    # Thay thế các giá trị NaN bằng 0 (nếu có sau khi normalize)
    values1 = [0 if pd.isna(v) else v for v in values1]
    values2 = [0 if pd.isna(v) else v for v in values2]
    
    # 3. Chuẩn bị vẽ Radar Chart (cần khép kín đa giác)
    values1 += values1[:1]
    values2 += values2[:1]
    
    angles = [n / float(len(attributes)) * 2 * np.pi for n in range(len(attributes))]
    angles += angles[:1]
    
    # Khởi tạo figure
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    
    # Vẽ từng trục (attribute)
    plt.xticks(angles[:-1], attributes, color='grey', size=12)
    
    # Vẽ các mốc giá trị từ 0.2 đến 0.8
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10)
    plt.ylim(0, 1)
    
    # Vẽ vùng của Laptop 1
    ax.plot(angles, values1, linewidth=2, linestyle='solid', label=laptop1_name)
    ax.fill(angles, values1, alpha=0.25)
    
    # Vẽ vùng của Laptop 2
    ax.plot(angles, values2, linewidth=2, linestyle='solid', label=laptop2_name)
    ax.fill(angles, values2, alpha=0.25)
    
    # Thêm Legend và Title
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title(f"So sánh: {laptop1_name} vs {laptop2_name}", size=15, y=1.1)
    
    # 4. Lưu biểu đồ
    os.makedirs('static/charts', exist_ok=True)
    filepath = 'static/charts/radar_comparison.png'
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    
    return True

if __name__ == "__main__":
    # Test thử script
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.data_cleaning import load_data, clean_data
    
    print("--- Bắt đầu Test Radar Chart ---")
    df_raw = load_data('data/laptops.csv')
    if df_raw is not None:
        df = clean_data(df_raw)
        
        # Chọn 2 laptop đầu tiên trong danh sách
        laptop_names = df['name'].unique()
        if len(laptop_names) >= 2:
            l1 = laptop_names[0]
            l2 = laptop_names[1]
            attrs = ['cpu_score', 'gpu_score', 'ram', 'storage', 'screen_size', 'battery', 'price']
            
            print(f"Đang tạo biểu đồ so sánh giữa:\n1. {l1}\n2. {l2}")
            print(f"Thuộc tính: {attrs}")
            
            success = create_radar_chart(df, l1, l2, attrs)
            if success:
                print("\nTHÀNH CÔNG! Đã lưu file tại: static/charts/radar_comparison.png")
            else:
                print("\nTHẤT BẠI! Lỗi khi tạo biểu đồ.")
        else:
            print("Không đủ laptop trong dataset để test.")
