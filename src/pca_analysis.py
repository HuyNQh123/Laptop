import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA

def run_pca_and_plot(X_scaled, labels, best_k, df_names_brands):
    """
    Thực hiện PCA để giảm chiều dữ liệu xuống 2D, vẽ biểu đồ và lưu file CSV.
    X_scaled: dữ liệu dạng số đã được chuẩn hóa (từ src.clustering).
    labels: mảng nhãn cluster đã dự đoán từ K-Means.
    df_names_brands: DataFrame phụ để lấy name, brand ghép vào file csv đầu ra.
    """
    # Khởi tạo PCA 2 chiều
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    # Tính Variance giải thích được
    explained_variance = pca.explained_variance_ratio_
    pc1_var = explained_variance[0] * 100
    pc2_var = explained_variance[1] * 100
    total_var = pc1_var + pc2_var
    
    # ---------------------------
    # VẼ BIỂU ĐỒ SCATTER
    # ---------------------------
    os.makedirs('static/charts', exist_ok=True)
    plt.figure(figsize=(10, 6))
    
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', alpha=0.7, edgecolor='k')
    
    # Tạo bảng chú thích (Legend)
    handles, _ = scatter.legend_elements(prop="colors")
    legend_labels = [f"Cluster {i}" for i in range(best_k)]
    plt.legend(handles, legend_labels, title="Clusters")
    
    plt.title('PCA - Laptop Clusters Visualization (2D)')
    plt.xlabel(f'Principal Component 1 (PC1) - Explained Var: {pc1_var:.1f}%')
    plt.ylabel(f'Principal Component 2 (PC2) - Explained Var: {pc2_var:.1f}%')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('static/charts/pca_clusters.png')
    plt.close()
    
    # ---------------------------
    # LƯU FILE CSV
    # ---------------------------
    df_pca = pd.DataFrame({
        'name': df_names_brands['name'].values,
        'brand': df_names_brands['brand'].values,
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1],
        'cluster': labels
    })
    df_pca.to_csv('data/laptops_pca.csv', index=False)
    
    return {
        'pc1_variance': pc1_var,
        'pc2_variance': pc2_var,
        'total_variance': total_var
    }

def test_pca():
    """Hàm test độc lập để gọi riêng module này từ terminal."""
    from src.data_cleaning import load_data, clean_data
    from src.clustering import prepare_clustering_data, scale_features, find_best_k, perform_kmeans
    
    print("--- BƯỚC 1: Đọc và scale dữ liệu (Giả lập Clustering) ---")
    df_raw = load_data('data/laptops.csv')
    if df_raw is None:
        return
        
    df_clean = clean_data(df_raw)
    X, _ = prepare_clustering_data(df_clean)
    df_clean = df_clean.loc[X.index].copy()
    
    X_scaled, _ = scale_features(X)
    
    # Mượn tạm hàm clustering để lấy nhãn cluster
    _, _, _, best_k, _ = find_best_k(X_scaled)
    df_clustered, _ = perform_kmeans(df_clean, X_scaled, best_k)
    
    print("\n--- BƯỚC 2: Chạy PCA ---")
    results = run_pca_and_plot(X_scaled, df_clustered['cluster'], best_k, df_clean[['name', 'brand']])
    
    print(f"\n[Explained Variance]")
    print(f"PC1: {results['pc1_variance']:.2f}%")
    print(f"PC2: {results['pc2_variance']:.2f}%")
    print(f"Total Explained Variance: {results['total_variance']:.2f}%")
    
    print("\n[Thành công] Đã lưu:")
    print("- Hình: static/charts/pca_clusters.png")
    print("- Data: data/laptops_pca.csv")

if __name__ == '__main__':
    test_pca()
