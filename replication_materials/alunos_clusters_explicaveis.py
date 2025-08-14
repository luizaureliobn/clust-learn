# === Script baseado no framework "A comprehensive framework for explainable cluster analysis"
# === Adaptado para dados educacionais: 'alunos_graduacao.csv'
# === Autor: [Seu Nome]
# === Referências: Alvarez-Garcia et al. (2024), Clust-learn

import os
import numpy as np
import pandas as pd

from clearn.data_preprocessing import (
    impute_missing_values,
    remove_outliers,
    missing_values_heatmap,
    plot_imputation_distribution_assessment,
)
from clearn.dimensionality_reduction import DimensionalityReduction
from clearn.clustering import Clustering
from clearn.classifier import Classifier

from lime.lime_tabular import LimeTabularExplainer

np.random.seed(42)
os.makedirs("img", exist_ok=True)

# === 1. CARREGAR E DETECTAR VARIÁVEIS ===
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data", "alunos_graduacao.csv")
df = pd.read_csv(data_path)
num_vars = df.select_dtypes(include=[np.number]).columns.tolist()
cat_vars = df.select_dtypes(exclude=[np.number]).columns.tolist()

print(f"Numéricas: {num_vars}")
print(f"Categóricas: {cat_vars}")

# === 2. DATA PREPROCESSING ===
print("--- DATA PREPROCESSING ---")
missing_values_heatmap(df, output_path="img/missing_heatmap.jpg")

df_imp = impute_missing_values(df, num_vars=num_vars, cat_vars=cat_vars)
plot_imputation_distribution_assessment(
    df.loc[df_imp.index],
    df_imp,
    imputed_vars=num_vars[:4],
    output_path="img/imputation_distribution.jpg",
)

df_clean, outliers = remove_outliers(df_imp, variables=num_vars + cat_vars)
print(f"Outliers removidos: {len(outliers)}")

# === 3. DIMENSIONALITY REDUCTION ===
print("--- DIMENSIONALITY REDUCTION ---")
df_clean = df_clean.reset_index(drop=True)

dr = DimensionalityReduction(
    df_clean,
    num_vars=num_vars,
    cat_vars=cat_vars,
    num_algorithm="spca",
    cat_algorithm="mca",
)

df_t = dr.transform(min_explained_variance_ratio=None)
print(f"Componentes extraídos: {dr.n_components_}")

dr.plot_num_explained_variance(
    0.5, plots=["cumulative", "normalized"], output_path="img/explained_variance.jpg"
)

# Explicar componentes principais (opcional)
print(dr.num_main_contributors(dim_idx=0))
dr.plot_num_main_contributors(dim_idx=0, output_path="img/main_contributors.jpg")

# === 4. CLUSTERING ===
print("--- CLUSTERING ---")
cl = Clustering(df_t, algorithms=["kmeans", "ward"], normalize=False)
cl.compute_clusters(n_clusters=None, max_clusters=20, prefix="ALU")
print(f"Configuração ótima: {cl.optimal_config_}")

cl.plot_clustercount(output_path="img/cluster_count.jpg")
cl.plot_optimal_components_normalized(output_path="img/elbow_curve.jpg")

df_clean["cluster"] = cl.df["cluster"].values

# === 5. CLASSIFIER + SHAP ===
print("--- CLASSIFIER ---")
predictor_cols = [c for c in df_clean.columns if c not in ["cluster"]]
classifier = Classifier(
    df_clean,
    predictor_cols=predictor_cols,
    target=df_clean["cluster"],
    num_cols=num_vars,
    cat_cols=cat_vars,
)

classifier.train_model(
    features_to_keep=[],  # ajuste se quiser fixar variáveis-chave
    hyperparameter_tuning=True,
    param_grid=dict(n_estimators=[30, 60], eta=[0.15, 0.25], max_depth=[3, 5, 7]),
)

classifier.plot_shap_importances(output_path="img/global_shap.jpg")
classifier.plot_shap_importances_beeswarm(
    class_id=0, output_path="img/local_shap_cluster0.jpg"
)
classifier.plot_confusion_matrix(output_path="img/confusion_matrix.jpg")
classifier.plot_roc_curves(output_path="img/roc_curves.jpg")

print("Feature importances (SHAP):")
print(classifier.feature_importances.head())
print("Classification report:")
print(classifier.classification_report())

# === 6. LIME (EXTENSÃO RECOMENDADA) ===
print("--- LIME EXPLANATION ---")
X_train = classifier.train_data[predictor_cols]
X_test = classifier.test_data[predictor_cols]
class_names = [str(c) for c in classifier.classifier.classes_]

explainer = LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=predictor_cols,
    class_names=class_names,
    mode="classification",
)

idx = 0  # exemplo de primeira instância
exp = explainer.explain_instance(
    X_test.iloc[idx].values, classifier.classifier.predict_proba, num_features=10
)
exp.save_to_file(f"img/lime_explanation_instance_{idx}.html")

print("Pipeline completo executado com sucesso.")
