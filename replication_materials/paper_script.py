# This script contains the code used for the illustration example

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from clearn.data_preprocessing import (
    missing_values_heatmap,
    impute_missing_values,
    plot_imputation_distribution_assessment,
    remove_outliers
)
from clearn.dimensionality_reduction import DimensionalityReduction
from clearn.clustering import Clustering
from clearn.classifier import Classifier
from sklearn.cluster import KMeans, AgglomerativeClustering

# Set the seed
np.random.seed(42)

# Numerical and categorical variable lists
num_vars = ['AGE', 'PAREDINT', 'BMMJ1',
            'BFMJ2', 'HISEI', 'DURECEC', 'BSMJ', 'MMINS',
            'LMINS', 'SMINS', 'TMINS', 'FCFMLRTY', 'SCCHANGE', 'CHANGE',
            'STUBMI', 'ESCS', 'UNDREM', 'METASUM', 'METASPAM', 'ICTHOME',
            'ICTSCH', 'HOMEPOS', 'CULTPOSS', 'HEDRES', 'WEALTH', 'ICTRES',
            'DISCLIMA', 'TEACHSUP', 'DIRINS', 'PERFEED', 'EMOSUPS',
            'STIMREAD', 'ADAPTIVITY', 'TEACHINT', 'JOYREAD', 'SCREADCOMP',
            'SCREADDIFF', 'PERCOMP', 'PERCOOP', 'ATTLNACT', 'COMPETE',
            'WORKMAST', 'GFOFAIL', 'EUDMO', 'SWBP', 'RESILIENCE', 'MASTGOAL',
            'GCSELFEFF', 'GCAWARE', 'ATTIMM', 'INTCULT', 'PERSPECT', 'COGFLEX',
            'RESPECT', 'AWACOM', 'GLOBMIND', 'DISCRIM', 'BELONG',
            'BEINGBULLIED', 'ENTUSE', 'HOMESCH', 'USESCH', 'INTICT', 'COMPICT',
            'AUTICT', 'SOIAICT', 'ICTCLASS', 'ICTOUTSIDE', 'INFOCAR',
            'INFOJOB1', 'INFOJOB2', 'FLCONFIN', 'FLCONICT', 'FLSCHOOL',
            'FLFAMILY', 'BODYIMA', 'SOCONPA'
            ]
cat_vars = ['ST004D01T', 'IMMIG', 'REPEAT']

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'data', 'pisa_spain_sample_v2.csv')
img_dir = os.path.join(script_dir, "img")

# Validation: Check if data file exists
if not os.path.exists(data_file_path):
    raise FileNotFoundError(
        f"Data file not found: {data_file_path}")

# Validation: Check if img directory exists, create if not
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    print(f"Pasta 'img' criada em: {img_dir}")
else:
    print(f"Pasta 'img' já existe em: {img_dir}")

# Load data
df = pd.read_csv(data_file_path)

# DATA PREPROCESSING
print('--- DATA PREPROCESSING ---')

# Compute missing values
n_missing = df.isnull().sum().sum()
print('Missing values:', n_missing, f'({n_missing*100/df.size}%)')

# Generate missing values heat map
missing_values_heatmap(
    df,
    output_path=os.path.join(img_dir, "missing_heatmap.jpg")
)

# Impute missing values
df_imp = impute_missing_values(df, num_vars=num_vars, cat_vars=cat_vars)

# Plot the comparison between the distribution of a selection of
# variables before and after imputation
plot_imputation_distribution_assessment(
    df.loc[df_imp.index], df_imp, ['COMPICT', 'BODYIMA', 'PERCOOP', 'SOCONPA'],
    output_path=os.path.join(img_dir, "imputation_distribution_assessment.jpg")
    )

# Remove outliers
df_, outliers = remove_outliers(df_imp, num_vars+cat_vars)

# DIMENSIONALITY REDUCTION
print('--- DIMENSIONALITY REDUCTION ---')
df_ = df_.reset_index(drop=True)

# Instantiate class, project to a lower dimensionality with optimal number of components
dr = DimensionalityReduction(df_, num_vars=num_vars, cat_vars=cat_vars, num_algorithm='spca')
df_t = dr.transform(min_explained_variance_ratio=None)
print(dr.n_components_, len(dr.num_components_), len(dr.cat_components_))

# Explain fourth extracted component
print(dr.num_main_contributors(dim_idx=3))
dr.plot_num_main_contributors(dim_idx=3, output_path=os.path.join(img_dir, "dim_red_main_contributors.jpg"))

# Explain component extracted from categorical variables
print(dr.cat_main_contributors_stats())
dr.plot_cat_main_contributor_distribution(dim_idx=0, output_path=os.path.join(img_dir, "dim_red_cat_component.jpg"))

# Plot explained variance
dr.plot_num_explained_variance(0.5, plots=['cumulative', 'normalized'],
                            output_path=os.path.join(img_dir, "dim_red_explained_variance.jpg"))

# CLUSTERING
print('--- CLUSTERING ---')

# Instantiate class and compute clusters on projected space
cl = Clustering(df_t, algorithms=[KMeans(random_state=42), AgglomerativeClustering(linkage='ward')], normalize=False)
cl.compute_clusters(max_clusters=21, prefix='STU')
print(cl.optimal_config_)

# Plot cluster count
cl.plot_clustercount(output_path=os.path.join(img_dir, "cluster_count.jpg"))

# Plot elbow curve
cl.plot_optimal_components_normalized(output_path=os.path.join(img_dir, "clustering_elbow_curve.jpg"))

# Compare cluster means to global means
print(cl.compare_cluster_means_to_global_means())
cl.plot_cluster_means_to_global_means_comparison(xlabel='Principal Components', ylabel='Clusters',
                                                 levels=[-1, -0.67, -0.3, -0.15, 0.15, 0.3, 0.67, 1],
                                                 output_path=os.path.join(img_dir, "clustering_intra_comparison.jpg"))

# Plot distribution comparison by cluster
cl.plot_distribution_comparison_by_cluster(df_ext=df_[['ESCS', 'TEACHSUP']],
                                           output_path=os.path.join(img_dir, "clustering_distribution_comparison.jpg"))

# Plot clusters in 2D
cl.plot_clusters_2D('dim_01', 'dim_02', output_path=os.path.join(img_dir, "clustering_2d_plots.jpg"))

# Describe clusters by categorical variable
print(cl.describe_clusters_cat(df_['IMMIG'], cat_name='IMMIG', normalize=True))
cl.plot_cat_distribution_by_cluster(df_['IMMIG'], cat_label='IMMIG', cluster_label='Student clusters',
                                    output_path=os.path.join(img_dir, "clustering_cat_comparison.jpg"))

# Add cluster information to dataframe
df_['cluster'] = cl.df['cluster'].values
df_['cluster_cat'] = cl.df['cluster_cat'].values

# CLASSIFIER
print('--- CLASSIFIER ---')
np.random.seed(42)

# Instantiate class and train model
var_list = list(df_.columns[1:-3])
classifier = Classifier(df_, predictor_cols=var_list, target=df_['cluster'], num_cols=num_vars, cat_cols=cat_vars)

# Train model with hyperparameter tuning
classifier.train_model(features_to_keep=['ESCS'], hyperparameter_tuning=True,
                       param_grid=dict(n_estimators=[30, 60], eta=[0.15, 0.25], max_depth=[3, 5, 7]))

# Feature importances
print(classifier.feature_importances.head())

# Plot SHAP importances
classifier.plot_shap_importances(output_path=os.path.join(img_dir, "classifier_global_feature_importance.jpg"))
plt.clf()

# Plot SHAP importances for specific classes
classifier.plot_shap_importances_beeswarm(class_id=1,
                                          output_path=os.path.join(img_dir, "classifier_local_importance_cl1.jpg"))
plt.clf()
classifier.plot_shap_importances_beeswarm(class_id=2,
                                          output_path=os.path.join(img_dir, "classifier_local_importance_cl2.jpg"))
plt.clf()

# Hyperparameter tuning metrics
print(classifier.hyperparameter_tuning_metrics())

# Confusion matrix
classifier.plot_confusion_matrix(output_path=os.path.join(img_dir, "classifier_confusion_matrix.jpg"))

# Classification report
print(classifier.classification_report())

# ROC curves
classifier.plot_roc_curves(output_path=os.path.join(img_dir, "classifier_roc_curves.jpg"))







