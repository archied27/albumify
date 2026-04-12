"""
train model on preprocessed df passed in
returns cluster model and results
"""

from hdbscan import HDBSCAN, membership_vector
from sklearn.neighbors import NearestNeighbors
import numpy as np

def train_model(df_scaled, df_ref):
    # takes in scaled df and reference df / original df
    clusterer = HDBSCAN(
        min_cluster_size=max([int(len(df_scaled)*0.02), 10]),
        min_samples=3,
        cluster_selection_epsilon=0,
        cluster_selection_method='leaf',
        prediction_data=True)
    labels = clusterer.fit_predict(df_scaled)

    noise_mask = labels == -1
    soft = membership_vector(clusterer, df_scaled[noise_mask])
    
    best_cluster = np.argmax(soft, axis=1)
    best_prob = soft[np.arange(len(soft)), best_cluster]

    assigned_soft = best_prob >= 0.01
    noise_indices = np.where(noise_mask)[0]
    labels[noise_indices[assigned_soft]] = best_cluster[assigned_soft]

    df_results = df_ref.copy()
    df_results['cluster'] = labels

    return df_results, clusterer