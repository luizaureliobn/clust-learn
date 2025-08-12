import pandas as pd
import numpy as np
import os
from clearn.data_preprocessing import impute_missing_values, remove_outliers
from clearn.dimensionality_reduction import DimensionalityReduction
from clearn.clustering import Clustering
from sklearn.cluster import KMeans, AgglomerativeClustering

np.random.seed(42)

# Load and preprocess data
num_vars = ['AGE', 'PAREDINT', 'BMMJ1', 'BFMJ2', 'HISEI', 'DURECEC', 'BSMJ', 'MMINS',
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
            'FLFAMILY', 'BODYIMA', 'SOCONPA']
cat_vars = ['ST004D01T', 'IMMIG', 'REPEAT']

df = pd.read_csv('data/pisa_spain_sample_v2.csv')
df_imp = impute_missing_values(df, num_vars=num_vars, cat_vars=cat_vars)
df_, outliers = remove_outliers(df_imp, num_vars+cat_vars)
df_ = df_.reset_index(drop=True)

# Dimensionality reduction
dr = DimensionalityReduction(df_, num_vars=num_vars, cat_vars=cat_vars, num_algorithm='spca')
df_t = dr.transform(min_explained_variance_ratio=None)

# Clustering
cl = Clustering(df_t, algorithms=[KMeans(random_state=42), AgglomerativeClustering(linkage='ward')], normalize=False)
cl.compute_clusters(max_clusters=21, prefix='STU')

print('=== INFORMAÇÕES DOS CLUSTERS ===')
print(f'Configuração ótima: {cl.optimal_config_}')
print(f'Número de clusters: {cl.optimal_config_[1]}')
print(f'Algoritmo usado: {cl.optimal_config_[0]}')
print(f'Score: {cl.optimal_config_[2]}')

print('\n=== CONTAGEM POR CLUSTER ===')
cluster_counts = pd.Series(cl.labels_).value_counts().sort_index()
for cluster, count in cluster_counts.items():
    print(f'Cluster {cluster}: {count} estudantes')

print('\n=== COMPARAÇÃO DE MÉDIAS DOS CLUSTERS COM MÉDIA GLOBAL ===')
comparison = cl.compare_cluster_means_to_global_means()
print(comparison)

print('\n=== DESCRIÇÃO DOS CLUSTERS POR VARIÁVEL CATEGÓRICA (IMMIG) ===')
immig_description = cl.describe_clusters_cat(df_['IMMIG'], cat_name='IMMIG', normalize=True)
print(immig_description)

print('\n=== DESCRIÇÃO DOS CLUSTERS POR VARIÁVEIS CONTÍNUAS ===')
cluster_description = cl.describe_clusters(df_ext=df_[['ESCS', 'TEACHSUP']], statistics=['mean', 'std'])
print(cluster_description)