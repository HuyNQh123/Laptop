import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from src.data_cleaning import load_data, clean_data
from src.data_analysis import NUMERIC_COLS

def prepare_clustering_data(df):
    """Lấy các cột số, xử lý NaN và chuẩn bị để đưa vào K-Means."""
    valid_cols = [col for col in NUMERIC_COLS if col in df.columns]
    X = df[valid_cols].copy()
    
    # Drop NaNs vì K-Means không chấp nhận NaN (Dù data_cleaning đã xử lý nhưng cứ cẩn thận)
    X = X.dropna()
    
    return X, valid_cols

def scale_features(X):
    """Chuẩn hóa dữ liệu bằng StandardScaler."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler

def find_best_k(X_scaled, max_k=8):
    """Tính inertia và silhouette score từ K=2 đến max_k."""
    inertias = []
    silhouette_scores = []
    k_values = range(2, max_k + 1)
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        score = silhouette_score(X_scaled, kmeans.labels_)
        silhouette_scores.append(score)
        print(f"K = {k}: Silhouette = {score:.4f}")
        
    best_k = k_values[np.argmax(silhouette_scores)]
    best_score = max(silhouette_scores)
    print(f"\nBest K: {best_k} (Silhouette = {best_score:.4f})")
    
    return k_values, inertias, silhouette_scores, best_k, best_score

def plot_elbow_method(k_values, inertias):
    """Vẽ biểu đồ Elbow."""
    os.makedirs('static/charts', exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, inertias, marker='o', linestyle='-', color='b')
    plt.title('Elbow Method')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Inertia')
    plt.xticks(k_values)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('static/charts/elbow_method.png')
    plt.close()

def plot_silhouette_scores(k_values, silhouette_scores, best_k):
    """Vẽ biểu đồ Silhouette."""
    os.makedirs('static/charts', exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, silhouette_scores, marker='o', linestyle='-', color='g')
    plt.axvline(x=best_k, color='r', linestyle='--', label=f'Best K = {best_k}')
    plt.title('Silhouette Score')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Score')
    plt.xticks(k_values)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('static/charts/silhouette_score.png')
    plt.close()

def perform_kmeans(df, X_scaled, k):
    """Huấn luyện mô hình K-Means và gán cluster labels vào dataframe gốc."""
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    
    df_clustered = df.copy()
    df_clustered['cluster'] = labels
    
    df_clustered.to_csv('data/laptops_clustered.csv', index=False)
    
    return df_clustered, kmeans

def get_cluster_summary(df_clustered, valid_cols):
    """Lấy thống kê trung bình (mean) của từng feature theo từng cluster."""
    summary = df_clustered.groupby('cluster')[valid_cols].mean().reset_index()
    counts = df_clustered['cluster'].value_counts().reset_index()
    counts.columns = ['cluster', 'count']
    
    summary = pd.merge(counts, summary, on='cluster')
    summary = summary.sort_values('cluster')
    return summary

def generate_cluster_label(row, overall_mean):
    """Đặt tên cluster dựa trên đặc điểm số liệu so với trung bình."""
    if row['gpu_score'] > overall_mean['gpu_score'] * 1.5:
        return "Gaming / High Performance"
    elif row['price'] > overall_mean['price'] * 1.5:
        return "Premium / High-end"
    elif row['price'] < overall_mean['price'] * 0.7:
        return "Budget / Office"
    else:
        return "Mainstream / Productivity"

def analyze_clusters(summary_df, overall_mean):
    """Trích xuất và định dạng chi tiết từng cluster."""
    details = []
    for _, row in summary_df.iterrows():
        cluster_id = int(row['cluster'])
        count = int(row['count'])
        label = generate_cluster_label(row, overall_mean)
        
        details.append({
            'cluster_id': cluster_id,
            'label': label,
            'count': count,
            'avg_cpu': row['cpu_score'],
            'avg_gpu': row['gpu_score'],
            'avg_ram': row['ram'],
            'avg_storage': row['storage'],
            'avg_price': row['price']
        })
    return details

def run_clustering_pipeline():
    """Chạy toàn bộ pipeline Clustering."""
    df_raw = load_data('data/laptops.csv')
    if df_raw is None:
        return None
    
    df_clean = clean_data(df_raw)
    
    X, valid_cols = prepare_clustering_data(df_clean)
    df_clean = df_clean.loc[X.index].copy()
    
    X_scaled, scaler = scale_features(X)
    
    k_values, inertias, silhouette_scores, best_k, best_score = find_best_k(X_scaled)
    
    plot_elbow_method(k_values, inertias)
    plot_silhouette_scores(k_values, silhouette_scores, best_k)
    
    df_clustered, kmeans_model = perform_kmeans(df_clean, X_scaled, best_k)
    
    cluster_summary = get_cluster_summary(df_clustered, valid_cols)
    overall_mean = X.mean()
    cluster_details = analyze_clusters(cluster_summary, overall_mean)
    
    # -------------------------------------
    # Chạy Tích hợp PCA Visualization (STEP 5)
    # -------------------------------------
    from src.pca_analysis import run_pca_and_plot
    pca_results = run_pca_and_plot(
        X_scaled=X_scaled, 
        labels=df_clustered['cluster'], 
        best_k=best_k, 
        df_names_brands=df_clustered[['name', 'brand']]
    )
    
    return {
        'total_laptops': len(df_clustered),
        'pca_results': pca_results,
        'best_k': best_k,
        'best_score': best_score,
        'cluster_summary': cluster_summary.to_dict(orient='records'),
        'cluster_details': cluster_details,
        'df_clustered': df_clustered.to_dict(orient='records')
    }

if __name__ == '__main__':
    print("\n--- CHẠY MODULE CLUSTERING ---")
    results = run_clustering_pipeline()
    if results:
        print(f"\nDataset loaded: {results['total_laptops']} laptops")
        
        print("\nCluster sizes:")
        for detail in results['cluster_details']:
            print(f"Cluster {detail['cluster_id']} ({detail['label']}): {detail['count']} laptops")
        
        print("\nĐã tạo thành công:")
        print("- static/charts/elbow_method.png")
        print("- static/charts/silhouette_score.png")
        print("- data/laptops_clustered.csv")
