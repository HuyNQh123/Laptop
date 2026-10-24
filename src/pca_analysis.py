import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA

def run_pca_and_plot(X_scaled, labels, best_k=3, df_names_brands=None, cluster_names=None, kmeans_model=None):
    """
    Thực hiện PCA để giảm chiều dữ liệu xuống 2D, vẽ biểu đồ và lưu file CSV.
    X_scaled: dữ liệu dạng số đã được chuẩn hóa (từ src.clustering).
    labels: mảng nhãn cluster đã dự đoán từ K-Means.
    best_k: số cụm (mặc định 3).
    df_names_brands: DataFrame phụ để lấy name, brand ghép vào file csv đầu ra.
    cluster_names: dict ánh xạ {cluster_id: label} để hiển thị chú giải chi tiết.
    kmeans_model: mô hình KMeans để tính và vẽ tọa độ tâm cụm (Centroids).
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
    
    # Bảng màu phân biệt rõ ràng 3 cụm: Xanh dương (Cụm 0), Đỏ (Cụm 1), Xanh lá (Cụm 2)
    colors = ['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd']
    labels_series = pd.Series(labels)
    
    for i in range(best_k):
        mask = (labels_series == i)
        count = mask.sum()
        c_label = cluster_names.get(i, f"Cụm {i}") if cluster_names else f"Cụm {i}"
        plt.scatter(
            X_pca[mask, 0], 
            X_pca[mask, 1], 
            c=colors[i % len(colors)], 
            label=f"Cụm {i}: {c_label} ({count} máy)", 
            alpha=0.75, 
            edgecolor='k', 
            s=70
        )
        
    # Đánh dấu tâm cụm (Centroids) nếu có mô hình KMeans
    if kmeans_model is not None:
        centroids_pca = pca.transform(kmeans_model.cluster_centers_)
        plt.scatter(
            centroids_pca[:, 0], 
            centroids_pca[:, 1], 
            c='black', 
            marker='X', 
            s=180, 
            linewidths=2, 
            label='Tâm Cụm (Centroids)', 
            zorder=10
        )
    
    plt.title(f'Bản đồ phân cụm laptop 2D bằng PCA (K = {best_k})', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel(f'Thành phần chính 1 (PC1) - Phương sai giải thích: {pc1_var:.1f}%', fontsize=11)
    plt.ylabel(f'Thành phần chính 2 (PC2) - Phương sai giải thích: {pc2_var:.1f}%', fontsize=11)
    plt.axhline(0, color='grey', linestyle='--', linewidth=0.8, alpha=0.5)
    plt.axvline(0, color='grey', linestyle='--', linewidth=0.8, alpha=0.5)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='best', frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig('static/charts/pca_clusters.png', dpi=200)
    plt.close()
    
    # ---------------------------
    # LƯU FILE CSV
    # ---------------------------
    os.makedirs('data', exist_ok=True)
    df_pca = pd.DataFrame({
        'name': df_names_brands['name'].values if df_names_brands is not None and 'name' in df_names_brands else range(len(labels)),
        'brand': df_names_brands['brand'].values if df_names_brands is not None and 'brand' in df_names_brands else ['Unknown'] * len(labels),
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
    """Hàm test độc lập để gọi riêng module này từ terminal với K = 3."""
    from src.data_cleaning import load_data, clean_data
    from src.clustering import prepare_clustering_data, scale_features, perform_kmeans, analyze_clusters, get_cluster_summary
    
    print("--- BƯỚC 1: Đọc và scale dữ liệu (Giả lập Clustering với K = 3) ---")
    df_raw = load_data('data/laptops.csv')
    if df_raw is None:
        return
        
    df_clean = clean_data(df_raw)
    X, valid_cols = prepare_clustering_data(df_clean)
    df_clean = df_clean.loc[X.index].copy()
    
    X_scaled, _ = scale_features(X)
    
    k = 3
    df_clustered, km_model = perform_kmeans(df_clean, X_scaled, k)
    summary = get_cluster_summary(df_clustered, valid_cols)
    details = analyze_clusters(summary, X.mean())
    c_names = {d['cluster_id']: d['label'] for d in details}
    
    print("\n--- BƯỚC 2: Chạy PCA ---")
    results = run_pca_and_plot(X_scaled, df_clustered['cluster'], k, df_clean[['name', 'brand']], cluster_names=c_names, kmeans_model=km_model)
    
    print(f"\n[Explained Variance]")
    print(f"PC1: {results['pc1_variance']:.2f}%")
    print(f"PC2: {results['pc2_variance']:.2f}%")
    print(f"Total Explained Variance: {results['total_variance']:.2f}%")
    
    print("\n[Thành công] Đã lưu:")
    print("- Hình: static/charts/pca_clusters.png")
    print("- Data: data/laptops_pca.csv")

if __name__ == '__main__':
    test_pca()
