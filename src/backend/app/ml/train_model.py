"""
train model on preprocessed df passed in
returns cluster model and results
"""

from hdbscan import HDBSCAN
from sklearn.neighbors import NearestNeighbors

def train_model(df_scaled, df_ref):
    # takes in scaled df and reference df / original df
    clusterer = HDBSCAN(
        min_cluster_size=int(len(df_scaled)*0.02),
        min_samples=1,
        cluster_selection_epsilon=0,
        cluster_selection_method='leaf')
    labels = clusterer.fit_predict(df_scaled)

    df_results = df_ref.copy()
    df_results['cluster'] = labels

    return df_results, clusterer