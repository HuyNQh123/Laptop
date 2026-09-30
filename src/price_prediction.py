import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data_cleaning import load_data, clean_data

# Danh sách thuộc tính đầu vào và mục tiêu dự đoán
FEATURE_COLS = [
    'cpu_score',
    'gpu_score',
    'ram',
    'storage',
    'screen_size',
    'refresh_rate',
    'weight',
    'battery',
    'rating'
]
TARGET_COL = 'price'
MODEL_PATH = 'models/laptop_price_model.pkl'

def prepare_data(df):
    """Chuẩn bị tập X (features) và y (target)."""
    X = df[FEATURE_COLS].copy()
    y = df[TARGET_COL].copy()
    return X, y

def train_and_evaluate_models():
    """Huấn luyện và so sánh Linear Regression và Random Forest."""
    df_raw = load_data('data/laptops.csv')
    if df_raw is None:
        raise FileNotFoundError("Không tìm thấy file dataset data/laptops.csv")
        
    df_clean = clean_data(df_raw)
    X, y = prepare_data(df_clean)
    
    # Chia tập train (80%) và test (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 1. Model Linear Regression (sử dụng Pipeline với StandardScaler)
    lr_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ])
    lr_pipeline.fit(X_train, y_train)
    lr_pred = lr_pipeline.predict(X_test)
    
    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    lr_r2 = r2_score(y_test, lr_pred)
    
    # 2. Model Random Forest Regressor
    rf_pipeline = Pipeline([
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    rf_pipeline.fit(X_train, y_train)
    rf_pred = rf_pipeline.predict(X_test)
    
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    rf_r2 = r2_score(y_test, rf_pred)
    
    # Chọn model có R² cao hơn để lưu và phục vụ dự đoán
    if rf_r2 >= lr_r2:
        best_model_name = "Random Forest Regressor"
        best_model = rf_pipeline
    else:
        best_model_name = "Linear Regression"
        best_model = lr_pipeline
        
    # Tạo thư mục models nếu chưa có
    os.makedirs('models', exist_ok=True)
    
    model_payload = {
        'model': best_model,
        'model_name': best_model_name,
        'features': FEATURE_COLS,
        'metrics': {
            'lr': {'mae': lr_mae, 'rmse': lr_rmse, 'r2': lr_r2},
            'rf': {'mae': rf_mae, 'rmse': rf_rmse, 'r2': rf_r2}
        },
        'train_size': len(X_train),
        'test_size': len(X_test),
        'total_size': len(df_clean)
    }
    
    joblib.dump(model_payload, MODEL_PATH)
    print(f"Đã lưu model tốt nhất ({best_model_name}) vào {MODEL_PATH}")
    
    return model_payload

def get_trained_model():
    """Tải model đã huấn luyện từ file .pkl hoặc tự động train nếu chưa có."""
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Lỗi khi load model ({e}), tiến hành train lại...")
    return train_and_evaluate_models()

def predict_laptop_price(features_dict):
    """
    Dự đoán giá laptop từ dictionary chứa các thông số kỹ thuật.
    Trả về giá dự đoán dạng số float.
    """
    payload = get_trained_model()
    model = payload['model']
    
    # Tạo DataFrame đúng thứ tự các cột features
    input_df = pd.DataFrame([features_dict])[FEATURE_COLS]
    predicted_price = model.predict(input_df)[0]
    return max(0.0, float(predicted_price))

if __name__ == '__main__':
    print("--- BẮT ĐẦU TRAINING & ĐÁNH GIÁ MÔ HÌNH DỰ ĐOÁN GIÁ ---")
    results = train_and_evaluate_models()
    
    print("\n--- KẾT QUẢ ĐÁNH GIÁ TRÊN TẬP TEST (20%) ---")
    print(f"Số mẫu Train: {results['train_size']} | Số mẫu Test: {results['test_size']}")
    print("-" * 55)
    print(f"1. Linear Regression:")
    print(f"   - MAE:  {results['metrics']['lr']['mae']:,.2f} VND")
    print(f"   - RMSE: {results['metrics']['lr']['rmse']:,.2f} VND")
    print(f"   - R²:   {results['metrics']['lr']['r2']:.4f}")
    print("-" * 55)
    print(f"2. Random Forest Regressor:")
    print(f"   - MAE:  {results['metrics']['rf']['mae']:,.2f} VND")
    print(f"   - RMSE: {results['metrics']['rf']['rmse']:,.2f} VND")
    print(f"   - R²:   {results['metrics']['rf']['r2']:.4f}")
    print("-" * 55)
    print(f"--> Model được chọn để dự đoán: {results['model_name']}")
    
    # Test thử dự đoán với 1 mẫu
    sample_input = {
        'cpu_score': 18000,
        'gpu_score': 12000,
        'ram': 16,
        'storage': 512,
        'screen_size': 15.6,
        'refresh_rate': 144,
        'weight': 2.1,
        'battery': 70,
        'rating': 4.5
    }
    sample_price = predict_laptop_price(sample_input)
    print(f"\nTest dự đoán cấu hình mẫu: {sample_price:,.0f} VND")
