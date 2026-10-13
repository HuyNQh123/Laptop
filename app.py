from flask import Flask, render_template, request
import sys
import os
import time

# Cho phép Python tìm thấy thư mục src
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.data_cleaning import load_data, clean_data
from src.data_analysis import get_top_bottom, calculate_statistics, create_charts
from src.radar_chart import create_radar_chart

app = Flask(__name__)

@app.route('/')
def index():
    df_raw = load_data('data/laptops.csv')
    total_laptops = 0
    total_brands = 0
    avg_price = 0
    max_price = 0
    
    if df_raw is not None:
        df_clean = clean_data(df_raw)
        total_laptops = len(df_clean)
        total_brands = df_clean['brand'].nunique()
        avg_price = df_clean['price'].mean()
        max_price = df_clean['price'].max()
        
    return render_template('index.html', 
                           total_laptops=total_laptops,
                           total_brands=total_brands,
                           avg_price=avg_price,
                           max_price=max_price)

@app.route('/laptops')
def laptops():
    df_raw = load_data('data/laptops.csv')
    if df_raw is not None:
        df_clean = clean_data(df_raw)
        # Chuyển đổi sang list of dicts để template dễ đọc
        laptops_data = df_clean.to_dict(orient='records')
    else:
        laptops_data = []
        
    return render_template('laptops.html', laptops=laptops_data)

@app.route('/analysis')
def analysis():
    df_raw = load_data('data/laptops.csv')
    if df_raw is None:
        return "Dataset not found", 404
        
    df_clean = clean_data(df_raw)
    
    # Thống kê tổng quan
    total_laptops = len(df_clean)
    total_brands = df_clean['brand'].nunique()
    
    avg_price = df_clean['price'].mean()
    med_price = df_clean['price'].median()
    std_price = df_clean['price'].std()
    
    # Top/Bottom
    top_price, bottom_price = get_top_bottom(df_clean, 'price', 3)
    top_cpu, bottom_cpu = get_top_bottom(df_clean, 'cpu_score', 3)
    top_gpu, bottom_gpu = get_top_bottom(df_clean, 'gpu_score', 3)
    
    # Bán chạy nhất
    if 'units_sold' in df_clean.columns:
        best_sellers, _ = get_top_bottom(df_clean, 'units_sold', 5)
    else:
        best_sellers = []
    
    # Bảng phân tích theo brand
    brand_stats = df_clean.groupby('brand').agg({
        'price': ['mean', 'median', 'std'],
        'cpu_score': 'mean',
        'gpu_score': 'mean'
    }).reset_index()
    # Làm phẳng multi-level columns
    brand_stats.columns = ['Brand', 'Mean Price', 'Median Price', 'Std Price', 'Mean CPU', 'Mean GPU']
    brand_stats_dict = brand_stats.to_dict(orient='records')
    
    # Tạo charts (ghi đè vào file ảnh cũ nếu có)
    create_charts(df_clean)
    
    # Lưu file results2.csv
    calculate_statistics(df_clean)

    return render_template('analysis.html', 
                           total_laptops=total_laptops,
                           total_brands=total_brands,
                           avg_price=avg_price,
                           med_price=med_price,
                           std_price=std_price,
                           top_price=top_price, bottom_price=bottom_price,
                           top_cpu=top_cpu, bottom_cpu=bottom_cpu,
                           top_gpu=top_gpu, bottom_gpu=bottom_gpu,
                           best_sellers=best_sellers,
                           brand_stats=brand_stats_dict)

@app.route('/clustering')
def clustering():
    from src.clustering import run_clustering_pipeline
    
    results = run_clustering_pipeline()
    if not results:
        return "Clustering failed or dataset not found", 500
        
    return render_template('clustering.html', results=results)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    df_raw = load_data('data/laptops.csv')
    if df_raw is None:
        return "Dataset not found", 404
        
    df_clean = clean_data(df_raw)
    
    # Danh sách laptop để hiển thị trong dropdown
    laptop_names = sorted(df_clean['name'].dropna().unique().tolist())
    
    # Các thuộc tính có thể so sánh
    available_attributes = ['cpu_score', 'gpu_score', 'ram', 'storage', 'screen_size', 'refresh_rate', 'weight', 'battery', 'rating', 'price']
    
    error = None
    laptop1_name = request.args.get('laptop1')
    laptop2_name = request.args.get('laptop2')
    # Mặc định chọn một vài thuộc tính quan trọng
    selected_attributes = ['cpu_score', 'gpu_score', 'ram', 'storage', 'price']
    comparison_data = None
    rand_val = int(time.time())
    
    if request.method == 'POST':
        laptop1_name = request.form.get('laptop1')
        laptop2_name = request.form.get('laptop2')
        selected_attributes = request.form.getlist('attributes')
        
        # Validation
        if not laptop1_name or not laptop2_name:
            error = "Vui lòng chọn cả hai laptop để so sánh."
        elif laptop1_name == laptop2_name:
            error = "Vui lòng chọn hai laptop khác nhau."
        elif not selected_attributes:
            error = "Vui lòng chọn ít nhất 1 tiêu chí để so sánh."
        elif len(selected_attributes) < 3:
            error = "Cần chọn ít nhất 3 tiêu chí để vẽ biểu đồ mạng nhện (Radar Chart)."
        else:
            success = create_radar_chart(df_clean, laptop1_name, laptop2_name, selected_attributes)
            if success:
                # Lấy dữ liệu thật để hiển thị trên bảng
                l1_row = df_clean[df_clean['name'] == laptop1_name].iloc[0]
                l2_row = df_clean[df_clean['name'] == laptop2_name].iloc[0]
                
                comparison_data = []
                for attr in selected_attributes:
                    comparison_data.append((attr, l1_row[attr], l2_row[attr]))
            else:
                error = "Lỗi khi tạo biểu đồ. Vui lòng kiểm tra lại dữ liệu."
                
    return render_template('compare.html', 
                           laptop_names=laptop_names, 
                           available_attributes=available_attributes,
                           selected_attributes=selected_attributes,
                           laptop1_name=laptop1_name,
                           laptop2_name=laptop2_name,
                           comparison_data=comparison_data,
                           error=error,
                           rand=rand_val)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    from src.price_prediction import get_trained_model, predict_laptop_price, recommend_similar_laptops
    
    model_payload = get_trained_model()
    model_name = model_payload['model_name']
    active_key = 'rf' if 'Random Forest' in model_name else 'lr'
    
    error = None
    predicted_price = None
    recommendations = []
    form_data = {}
    
    if request.method == 'POST':
        form_data = {
            'cpu_score': request.form.get('cpu_score', '').strip(),
            'gpu_score': request.form.get('gpu_score', '').strip(),
            'ram': request.form.get('ram', '').strip(),
            'storage': request.form.get('storage', '').strip(),
            'screen_size': request.form.get('screen_size', '').strip(),
            'refresh_rate': request.form.get('refresh_rate', '').strip(),
            'weight': request.form.get('weight', '').strip(),
            'battery': request.form.get('battery', '').strip(),
            'rating': request.form.get('rating', '').strip(),
        }
        
        field_names_vi = {
            'cpu_score': 'Điểm hiệu năng CPU',
            'gpu_score': 'Điểm hiệu năng GPU',
            'ram': 'Dung lượng RAM',
            'storage': 'Dung lượng ổ cứng',
            'screen_size': 'Kích thước màn hình',
            'refresh_rate': 'Tần số quét',
            'weight': 'Trọng lượng',
            'battery': 'Dung lượng pin',
            'rating': 'Điểm đánh giá'
        }
        
        # Validation
        try:
            # Kiểm tra xem có trường nào bị bỏ trống không
            for key, val in form_data.items():
                if not val:
                    raise ValueError(f"Vui lòng không để trống trường '{field_names_vi.get(key, key)}'.")
            
            # Chuyển đổi kiểu dữ liệu sang float
            features = {
                'cpu_score': float(form_data['cpu_score']),
                'gpu_score': float(form_data['gpu_score']),
                'ram': float(form_data['ram']),
                'storage': float(form_data['storage']),
                'screen_size': float(form_data['screen_size']),
                'refresh_rate': float(form_data['refresh_rate']),
                'weight': float(form_data['weight']),
                'battery': float(form_data['battery']),
                'rating': float(form_data['rating'])
            }
            
            # Kiểm tra giá trị không âm và hợp lý
            for key, val in features.items():
                if val <= 0:
                    raise ValueError(f"Giá trị của '{field_names_vi.get(key, key)}' phải lớn hơn 0.")
            
            if features['rating'] > 5.0:
                raise ValueError("Điểm đánh giá (Rating) tối đa là 5.0.")
            if features['screen_size'] > 30.0:
                raise ValueError("Kích thước màn hình không hợp lý (> 30 inch).")
            if features['weight'] > 15.0:
                raise ValueError("Trọng lượng laptop không hợp lý (> 15 kg).")
                
            # Dự đoán giá
            predicted_price = predict_laptop_price(features)
            
            # Gợi ý khoảng 5 mẫu laptop có cấu hình tương tự và chênh lệch khoảng 1-2 triệu
            recommendations = recommend_similar_laptops(features, predicted_price, top_n=5)
            
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Đã xảy ra lỗi trong quá trình tính toán: {str(e)}"
            
    return render_template('predict.html', 
                           model_info=model_payload,
                           active_key=active_key,
                           predicted_price=predicted_price,
                           recommendations=recommendations,
                           form_data=form_data,
                           error=error)

if __name__ == '__main__':
    # Chạy Flask ở debug mode
    app.run(debug=True)

