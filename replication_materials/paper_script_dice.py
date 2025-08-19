# Script baseado no paper_script.py com integração do DICE para explicabilidade de clusters
# Este script adiciona análise de contrafactuais usando DiCE (Diverse Counterfactual Explanations)

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
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Importações para DICE
try:
    import dice_ml
    from dice_ml import Dice
    DICE_AVAILABLE = True
except ImportError:
    print("AVISO: DiCE não está instalado. Para instalar: pip install dice-ml")
    DICE_AVAILABLE = False

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
img_dir = os.path.join(script_dir, "img_dice")
dice_results_dir = os.path.join(script_dir, "dice_results")

# Validation: Check if data file exists
if not os.path.exists(data_file_path):
    raise FileNotFoundError(
        f"Data file not found: {data_file_path}")

# Validation: Check if directories exist, create if not
for directory in [img_dir, dice_results_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Pasta '{os.path.basename(directory)}' criada em: {directory}")
    else:
        print(f"Pasta '{os.path.basename(directory)}' já existe em: {directory}")

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

# DICE ANALYSIS - EXPLICABILIDADE COM CONTRAFACTUAIS
print('\n--- DICE COUNTERFACTUAL ANALYSIS ---')

if DICE_AVAILABLE:
    try:
        # Preparar dados para DICE
        # Usar apenas variáveis numéricas para simplificar a análise inicial
        dice_features = [col for col in num_vars if col in df_.columns]
        
        # Criar dataset para DICE
        dice_data = df_[dice_features + ['cluster']].copy()
        dice_data = dice_data.dropna()
        
        # FIX: Garantir que a coluna do cluster seja do tipo string para compatibilidade com DICE
        dice_data['cluster'] = dice_data['cluster'].astype(str)
        
        print(f"Dataset para DICE: {dice_data.shape[0]} amostras, {len(dice_features)} features")
        print(f"Clusters únicos: {sorted(dice_data['cluster'].unique())}")
        
        # Dividir dados em treino e teste
        X = dice_data[dice_features]
        y = dice_data['cluster']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
        
        # Treinar modelo simples para DICE (Random Forest)
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        print(f"Acurácia do modelo Random Forest: {rf_model.score(X_test, y_test):.3f}")
        
        # Configurar DICE
        dice_data_interface = dice_ml.Data(
            dataframe=dice_data,
            continuous_features=dice_features,
            outcome_name='cluster'
        )
        
        dice_model = dice_ml.Model(
            model=rf_model,
            backend='sklearn'
        )
        
        dice_explainer = Dice(dice_data_interface, dice_model, method='random')
        
        # Abordagem funcional para DICE - Análise binária
        print("\n--- Gerando Contrafactuais com DICE (Análise Binária) ---")
        
        # Criar análises binárias entre pares de clusters para contornar limitações do DICE
        clusters_to_analyze = sorted(dice_data['cluster'].unique())
        successful_analyses = 0
        counterfactuals_results = {}
        
        # Analisar pares de clusters (0 vs 1, 0 vs 2, 1 vs 2)
        cluster_pairs = [(clusters_to_analyze[0], clusters_to_analyze[1]),
                        (clusters_to_analyze[0], clusters_to_analyze[2]),
                        (clusters_to_analyze[1], clusters_to_analyze[2])]
        
        for cluster_a, cluster_b in cluster_pairs:
            try:
                print(f"\n--- Análise Binária: Cluster {cluster_a} vs Cluster {cluster_b} ---")
                
                # Criar dataset binário
                binary_data = dice_data[dice_data['cluster'].isin([cluster_a, cluster_b])].copy()
                binary_data['binary_target'] = (binary_data['cluster'] == cluster_b).astype(int)
                
                if len(binary_data) < 10:
                    print(f"✗ Dados insuficientes para análise {cluster_a} vs {cluster_b}")
                    continue
                
                # Treinar modelo binário
                X_binary = binary_data[dice_features]
                y_binary = binary_data['binary_target']
                
                X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
                    X_binary, y_binary, test_size=0.3, random_state=42, stratify=y_binary
                )
                
                rf_binary = RandomForestClassifier(n_estimators=50, random_state=42)
                rf_binary.fit(X_train_bin, y_train_bin)
                
                print(f"Acurácia modelo binário: {rf_binary.score(X_test_bin, y_test_bin):.3f}")
                
                # Configurar DICE para problema binário
                dice_data_binary = binary_data[dice_features + ['binary_target']].copy()
                
                dice_interface_binary = dice_ml.Data(
                    dataframe=dice_data_binary,
                    continuous_features=dice_features,
                    outcome_name='binary_target'
                )
                
                dice_model_binary = dice_ml.Model(
                    model=rf_binary,
                    backend='sklearn'
                )
                
                dice_explainer_binary = Dice(dice_interface_binary, dice_model_binary, method='random')
                
                # Selecionar amostras para análise
                cluster_a_samples = binary_data[binary_data['cluster'] == cluster_a]
                if len(cluster_a_samples) > 0:
                    sample_idx = cluster_a_samples.index[0]
                    query_instance = dice_data_binary.loc[[sample_idx], dice_features]
                    
                    print(f"Gerando contrafactuais para mudar de Cluster {cluster_a} para Cluster {cluster_b}...")
                    
                    # Gerar contrafactuais
                    counterfactuals = dice_explainer_binary.generate_counterfactuals(
                        query_instance,
                        total_CFs=3,
                        desired_class=1  # Classe de destino (cluster_b)
                    )
                    
                    # Verificar resultados
                    if counterfactuals.cf_examples_list and len(counterfactuals.cf_examples_list) > 0:
                        cf_df = counterfactuals.cf_examples_list[0].final_cfs_df
                        
                        if len(cf_df) > 0:
                            print(f"✓ Contrafactuais gerados: {len(cf_df)}")
                            
                            # Salvar contrafactuais
                            cf_filename = os.path.join(dice_results_dir, f"counterfactuals_{cluster_a}_to_{cluster_b}.csv")
                            cf_df.to_csv(cf_filename, index=False)
                            
                            # Analisar mudanças
                            original_values = query_instance.iloc[0]
                            cf_values = cf_df.iloc[0][dice_features]
                            differences = cf_values - original_values
                            
                            # Mostrar principais mudanças
                            significant_changes = differences[abs(differences) > 0.1].sort_values(key=abs, ascending=False)
                            if len(significant_changes) > 0:
                                print("Principais mudanças necessárias:")
                                for feature, change in significant_changes.head(5).items():
                                    print(f"  {feature}: {change:+.3f}")
                            
                            counterfactuals_results[f"{cluster_a}_to_{cluster_b}"] = {
                                'counterfactuals': counterfactuals,
                                'changes': significant_changes.head(10).to_dict()
                            }
                            successful_analyses += 1
                            
                            print(f"Contrafactuais salvos em: {cf_filename}")
                        else:
                            print(f"✗ Nenhum contrafactual gerado para {cluster_a} -> {cluster_b}")
                    else:
                        print(f"✗ Falha ao gerar contrafactuais para {cluster_a} -> {cluster_b}")
                        
            except Exception as e:
                print(f"✗ Erro na análise {cluster_a} vs {cluster_b}: {str(e)}")
        
        print(f"\n--- RESUMO DA ANÁLISE DICE ---")
        print(f"Análises binárias realizadas: {len(cluster_pairs)}")
        print(f"Análises bem-sucedidas: {successful_analyses}")
        
        # Criar visualização dos contrafactuais se houver resultados
        if successful_analyses > 0:
            print("\n--- Criando Visualização dos Contrafactuais ---")
            
            # Criar gráfico de importância das mudanças
            all_changes = {}
            for analysis_key, result in counterfactuals_results.items():
                for feature, change in result['changes'].items():
                    if feature not in all_changes:
                        all_changes[feature] = []
                    all_changes[feature].append(abs(change))
            
            # Calcular importância média das features
            feature_importance = {}
            for feature, changes in all_changes.items():
                feature_importance[feature] = np.mean(changes)
            
            # Salvar análise de importância
            importance_df = pd.DataFrame(list(feature_importance.items()), 
                                       columns=['Feature', 'Avg_Change_Magnitude'])
            importance_df = importance_df.sort_values('Avg_Change_Magnitude', ascending=False)
            
            importance_file = os.path.join(dice_results_dir, "feature_importance_counterfactuals.csv")
            importance_df.to_csv(importance_file, index=False)
            print(f"Análise de importância salva em: {importance_file}")
            
            # Mostrar top 10 features mais importantes
            print("\nTop 10 features mais importantes para mudanças de cluster:")
            for idx, row in importance_df.head(10).iterrows():
                print(f"  {row['Feature']}: {row['Avg_Change_Magnitude']:.3f}")
        
        all_changes = list(counterfactuals_results.keys())
        
        # Criar relatório resumido
        report_path = os.path.join(dice_results_dir, "dice_analysis_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE ANÁLISE DICE - CONTRAFACTUAIS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Dataset analisado: {dice_data.shape[0]} amostras\n")
            f.write(f"Features utilizadas: {len(dice_features)}\n")
            f.write(f"Clusters analisados: {clusters_to_analyze}\n")
            f.write(f"Análises realizadas: {len(all_changes)}\n\n")
            
            for change in all_changes:
                f.write(f"- {change}\n")
        
        print(f"Relatório salvo em: {report_path}")
        
    except Exception as e:
        print(f"Erro na análise DICE: {str(e)}")
        print("Verifique se o DiCE está instalado corretamente: pip install dice-ml")
else:
    print("DiCE não está disponível. Para usar esta funcionalidade, instale: pip install dice-ml")

print("\n--- ANÁLISE COMPLETA FINALIZADA ---")
print(f"Resultados salvos em: {img_dir}")
if DICE_AVAILABLE:
    print(f"Resultados DICE salvos em: {dice_results_dir}")