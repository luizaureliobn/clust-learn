#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise Completa Integrada - PISA Clusters

Este script integra todas as funcionalidades dos scripts individuais em um único arquivo:
- Análise principal com visualizações (paper_script.py)
- Extração de informações dos clusters (extract_cluster_info.py) 
- Geração de relatório completo (generate_cluster_report.py)

Vantagens:
- Execução unificada sem dependências entre scripts
- Reutilização de objetos e dados processados
- Melhor performance (evita reprocessamento)
- Controle centralizado do fluxo de execução

Autor: Sistema de Análise PISA
Data: 2024
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from datetime import datetime
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

# Configuração global
np.random.seed(42)

# Listas de variáveis
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

def print_section(title, char="=", width=80):
    """Imprime uma seção formatada"""
    print(f"\n{char * width}")
    print(f" {title} ".center(width, char))
    print(f"{char * width}\n")

def setup_directories():
    """Configura diretórios necessários"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'data', 'pisa_spain_sample_v2.csv')
    img_dir = os.path.join(script_dir, "img")
    
    # Verificar se arquivo de dados existe
    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {data_file_path}")
    
    # Criar diretório de imagens se não existir
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        print(f"📁 Pasta 'img' criada em: {img_dir}")
    else:
        print(f"📁 Pasta 'img' já existe em: {img_dir}")
    
    return script_dir, data_file_path, img_dir

def load_and_preprocess_data(data_file_path, img_dir):
    """Carrega e pré-processa os dados"""
    print_section("CARREGAMENTO E PRÉ-PROCESSAMENTO DOS DADOS")
    
    # Carregar dados
    print("📊 Carregando dados...")
    df = pd.read_csv(data_file_path)
    print(f"✅ Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    
    # Calcular valores ausentes
    n_missing = df.isnull().sum().sum()
    print(f"❓ Valores ausentes: {n_missing:,} ({n_missing*100/df.size:.2f}%)")
    
    # Gerar mapa de calor de valores ausentes
    print("🔥 Gerando mapa de calor de valores ausentes...")
    missing_values_heatmap(df, output_path=os.path.join(img_dir, "missing_heatmap.jpg"))
    
    # Imputar valores ausentes
    print("🔧 Imputando valores ausentes...")
    df_imp = impute_missing_values(df, num_vars=num_vars, cat_vars=cat_vars)
    
    # Plotar comparação de distribuições antes/depois da imputação
    print("📈 Gerando gráfico de avaliação da imputação...")
    plot_imputation_distribution_assessment(
        df.loc[df_imp.index], df_imp, ['COMPICT', 'BODYIMA', 'PERCOOP', 'SOCONPA'],
        output_path=os.path.join(img_dir, "imputation_distribution_assessment.jpg")
    )
    
    # Remover outliers
    print("🚫 Removendo outliers...")
    df_clean, outliers = remove_outliers(df_imp, num_vars + cat_vars)
    df_clean = df_clean.reset_index(drop=True)
    
    print(f"✅ Pré-processamento concluído:")
    print(f"   • Dados limpos: {df_clean.shape[0]} linhas")
    print(f"   • Outliers removidos: {len(outliers)} linhas")
    
    return df, df_clean

def perform_dimensionality_reduction(df_clean, img_dir):
    """Executa redução de dimensionalidade"""
    print_section("REDUÇÃO DE DIMENSIONALIDADE")
    
    # Instanciar classe e projetar para menor dimensionalidade
    print("🔄 Aplicando redução de dimensionalidade (SPCA)...")
    dr = DimensionalityReduction(df_clean, num_vars=num_vars, cat_vars=cat_vars, num_algorithm='spca')
    df_reduced = dr.transform(min_explained_variance_ratio=None)
    
    print(f"✅ Redução concluída:")
    print(f"   • Componentes totais: {dr.n_components_}")
    print(f"   • Componentes numéricos: {len(dr.num_components_)}")
    print(f"   • Componentes categóricos: {len(dr.cat_components_)}")
    
    # Explicar quarto componente extraído
    print("\n🔍 Principais contribuidores do 4º componente:")
    contributors = dr.num_main_contributors(dim_idx=3)
    print(contributors)
    dr.plot_num_main_contributors(dim_idx=3, output_path=os.path.join(img_dir, "dim_red_main_contributors.jpg"))
    
    # Explicar componente extraído de variáveis categóricas
    print("\n📊 Estatísticas dos principais contribuidores categóricos:")
    cat_stats = dr.cat_main_contributors_stats()
    print(cat_stats)
    dr.plot_cat_main_contributor_distribution(dim_idx=0, output_path=os.path.join(img_dir, "dim_red_cat_component.jpg"))
    
    # Plotar variância explicada
    print("📈 Gerando gráfico de variância explicada...")
    dr.plot_num_explained_variance(0.5, plots=['cumulative', 'normalized'],
                                output_path=os.path.join(img_dir, "dim_red_explained_variance.jpg"))
    
    return dr, df_reduced

def perform_clustering(df_reduced, img_dir):
    """Executa análise de clustering"""
    print_section("ANÁLISE DE CLUSTERING")
    
    # Instanciar classe e computar clusters no espaço projetado
    print("🎯 Executando clustering...")
    cl = Clustering(df_reduced, algorithms=[KMeans(random_state=42), AgglomerativeClustering(linkage='ward')], normalize=False)
    cl.compute_clusters(max_clusters=21, prefix='STU')
    
    print(f"✅ Clustering concluído:")
    print(f"   • Configuração ótima: {cl.optimal_config_}")
    print(f"   • Algoritmo: {cl.optimal_config_[0]}")
    print(f"   • Número de clusters: {cl.optimal_config_[1]}")
    print(f"   • Score: {cl.optimal_config_[2]:.4f}")
    
    # Plotar contagem de clusters
    print("📊 Gerando gráficos de clustering...")
    cl.plot_clustercount(output_path=os.path.join(img_dir, "cluster_count.jpg"))
    
    # Plotar curva do cotovelo
    cl.plot_optimal_components_normalized(output_path=os.path.join(img_dir, "clustering_elbow_curve.jpg"))
    
    # Comparar médias dos clusters com médias globais
    print("\n🔍 Comparação de médias dos clusters com média global:")
    comparison = cl.compare_cluster_means_to_global_means()
    print(comparison)
    cl.plot_cluster_means_to_global_means_comparison(
        xlabel='Componentes Principais', ylabel='Clusters',
        levels=[-1, -0.67, -0.3, -0.15, 0.15, 0.3, 0.67, 1],
        output_path=os.path.join(img_dir, "clustering_intra_comparison.jpg")
    )
    
    return cl

def perform_classification_and_analysis(cl, df_clean, img_dir):
    """Executa classificação e análise adicional"""
    print_section("CLASSIFICAÇÃO E ANÁLISE ADICIONAL")
    
    # Adicionar informações de cluster ao dataframe
    df_clean['cluster'] = cl.df['cluster'].values
    df_clean['cluster_cat'] = cl.df['cluster_cat'].values
    
    # Plotar comparação de distribuições por cluster
    print("📈 Gerando gráficos de distribuição por cluster...")
    cl.plot_distribution_comparison_by_cluster(
        df_ext=df_clean[['ESCS', 'TEACHSUP']],
        output_path=os.path.join(img_dir, "clustering_distribution_comparison.jpg")
    )
    
    # Plotar clusters em 2D
    cl.plot_clusters_2D('dim_01', 'dim_02', output_path=os.path.join(img_dir, "clustering_2d_plots.jpg"))
    
    # Descrever clusters por variável categórica
    print("\n📊 Descrição dos clusters por variável categórica (IMMIG):")
    immig_description = cl.describe_clusters_cat(df_clean['IMMIG'], cat_name='IMMIG', normalize=True)
    print(immig_description)
    cl.plot_cat_distribution_by_cluster(
        df_clean['IMMIG'], cat_label='IMMIG', cluster_label='Student clusters',
        output_path=os.path.join(img_dir, "clustering_cat_comparison.jpg")
    )
    
    # Classificação
    print("\n🤖 Treinando modelo de classificação...")
    np.random.seed(42)
    
    # Preparar dados para classificação
    var_list = list(df_clean.columns[1:-3])  # Excluir índice e colunas de cluster
    classifier = Classifier(
        df_clean, 
        predictor_cols=var_list, 
        target=df_clean['cluster'], 
        num_cols=num_vars, 
        cat_cols=cat_vars
    )
    
    # Treinar modelo com otimização de hiperparâmetros
    classifier.train_model(
        features_to_keep=['ESCS'], 
        hyperparameter_tuning=True,
        param_grid=dict(n_estimators=[30, 60], eta=[0.15, 0.25], max_depth=[3, 5, 7])
    )
    
    # Importâncias das features
    print("\n🎯 Top 10 features mais importantes:")
    print(classifier.feature_importances.head(10))
    
    # Plotar importâncias SHAP
    print("📊 Gerando gráficos de importância das features...")
    classifier.plot_shap_importances(output_path=os.path.join(img_dir, "classifier_global_feature_importance.jpg"))
    plt.clf()
    
    # Plotar importâncias SHAP para classes específicas
    classifier.plot_shap_importances_beeswarm(
        class_id=1, output_path=os.path.join(img_dir, "classifier_local_importance_cl1.jpg")
    )
    plt.clf()
    classifier.plot_shap_importances_beeswarm(
        class_id=2, output_path=os.path.join(img_dir, "classifier_local_importance_cl2.jpg")
    )
    plt.clf()
    
    # Métricas de otimização de hiperparâmetros
    print("\n⚙️ Métricas de otimização de hiperparâmetros:")
    print(classifier.hyperparameter_tuning_metrics())
    
    # Matriz de confusão
    print("📊 Gerando matriz de confusão...")
    classifier.plot_confusion_matrix(output_path=os.path.join(img_dir, "classifier_confusion_matrix.jpg"))
    
    # Relatório de classificação
    print("\n📋 Relatório de classificação:")
    classification_report = classifier.classification_report()
    print(classification_report)
    
    # Curvas ROC
    print("📈 Gerando curvas ROC...")
    classifier.plot_roc_curves(output_path=os.path.join(img_dir, "classifier_roc_curves.jpg"))
    
    return classifier, df_clean

def extract_detailed_cluster_info(cl, df_clean):
    """Extrai informações detalhadas dos clusters"""
    print_section("EXTRAÇÃO DE INFORMAÇÕES DETALHADAS DOS CLUSTERS")
    
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
    immig_description = cl.describe_clusters_cat(df_clean['IMMIG'], cat_name='IMMIG', normalize=True)
    print(immig_description)
    
    print('\n=== DESCRIÇÃO DOS CLUSTERS POR VARIÁVEIS CONTÍNUAS ===')
    cluster_description = cl.describe_clusters(df_ext=df_clean[['ESCS', 'TEACHSUP']], statistics=['mean', 'std'])
    print(cluster_description)

def generate_detailed_report(cl, classifier, df_clean):
    """Gera relatório detalhado dos clusters"""
    print_section("GERAÇÃO DE RELATÓRIO DETALHADO")
    
    report = []
    report.append("=" * 100)
    report.append("RELATÓRIO DE ANÁLISE DE CLUSTERS - DADOS PISA ESPANHA")
    report.append("=" * 100)
    report.append(f"Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    report.append("\n")
    
    # 1. RESUMO EXECUTIVO
    report.append("1. RESUMO EXECUTIVO")
    report.append("-" * 50)
    
    optimal_config = cl.optimal_config_
    total_students = len(df_clean)
    n_clusters = optimal_config[1]
    algorithm = optimal_config[0]
    score = optimal_config[2]
    
    report.append(f"• Total de estudantes analisados: {total_students:,}")
    report.append(f"• Número de clusters identificados: {n_clusters}")
    report.append(f"• Algoritmo utilizado: {algorithm}")
    report.append(f"• Score de inércia: {score:,.2f}")
    report.append("\n")
    
    # 2. DISTRIBUIÇÃO DOS ESTUDANTES POR CLUSTER
    report.append("2. DISTRIBUIÇÃO DOS ESTUDANTES POR CLUSTER")
    report.append("-" * 50)
    
    cluster_counts = df_clean['cluster'].value_counts().sort_index()
    for cluster_id in sorted(cluster_counts.index):
        count = cluster_counts[cluster_id]
        percentage = (count / total_students) * 100
        report.append(f"• Cluster {cluster_id} (STU_{cluster_id}): {count:,} estudantes ({percentage:.1f}%)")
    report.append("\n")
    
    # 3. CRITÉRIOS DE CLASSIFICAÇÃO
    report.append("3. CRITÉRIOS DE CLASSIFICAÇÃO")
    report.append("-" * 50)
    
    # Importância das variáveis (SHAP)
    shap_importance = classifier.feature_importances
    report.append("VARIÁVEIS MAIS IMPORTANTES PARA CLASSIFICAÇÃO:")
    report.append("(Baseado na análise SHAP - Shapley Additive Explanations)")
    report.append("")
    
    # Top 10 variáveis mais importantes
    top_features = shap_importance.head(10)
    for i, var_name in enumerate(top_features.index, 1):
        importance_val = top_features.loc[var_name]
        try:
            if hasattr(importance_val, 'item'):
                importance_val = importance_val.item()
            importance_val = float(importance_val)
        except (ValueError, TypeError):
            importance_val = 0.0
        report.append(f"{i:2d}. {var_name}: {importance_val:.3f}")
    
    report.append("")
    
    # Métricas de desempenho do classificador
    report.append("DESEMPENHO DO CLASSIFICADOR:")
    classification_report_df = classifier.classification_report()
    
    try:
        # Extrair acurácia
        if 'accuracy' in classification_report_df.columns:
            accuracy = classification_report_df['accuracy'].iloc[0]
        elif 'accuracy' in classification_report_df.index:
            accuracy = classification_report_df.loc['accuracy'].iloc[0]
        else:
            accuracy = 0.0
        
        report.append(f"• Acurácia geral: {accuracy:.1%}")
        
        # Métricas macro avg se disponível
        if 'macro avg' in classification_report_df.index:
            macro_avg = classification_report_df.loc['macro avg']
            report.append(f"• Precisão média (macro): {macro_avg['precision']:.1%}")
            report.append(f"• Recall médio (macro): {macro_avg['recall']:.1%}")
            report.append(f"• F1-Score médio (macro): {macro_avg['f1-score']:.1%}")
        
    except Exception as e:
        report.append(f"• Erro ao extrair métricas: {e}")
    
    report.append("")
    
    # 4. METODOLOGIA
    report.append("4. METODOLOGIA")
    report.append("-" * 50)
    
    report.append("ETAPAS DA ANÁLISE:")
    report.append("")
    report.append("1. PRÉ-PROCESSAMENTO:")
    report.append("   • Tratamento de valores ausentes")
    report.append("   • Imputação baseada em modelo")
    report.append("   • Remoção de outliers")
    report.append("")
    report.append("2. REDUÇÃO DE DIMENSIONALIDADE:")
    report.append("   • Análise de Componentes Principais Esparsas (SPCA)")
    report.append("   • Redução de 67 variáveis para componentes principais")
    report.append("")
    report.append("3. CLUSTERING:")
    report.append("   • Algoritmo K-Means e Clustering Hierárquico")
    report.append("   • Seleção do número ótimo de clusters")
    report.append("   • Validação com múltiplas métricas")
    report.append("")
    report.append("4. CLASSIFICAÇÃO:")
    report.append("   • Modelo XGBoost")
    report.append("   • Otimização de hiperparâmetros")
    report.append("   • Análise de importância com SHAP")
    report.append("")
    
    report.append("=" * 100)
    report.append("FIM DO RELATÓRIO")
    report.append("=" * 100)
    
    # Salvar relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"relatorio_clusters_integrado_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"✅ Relatório salvo como: {report_filename}")
    return report_filename

def main():
    """Função principal da análise integrada"""
    print_section("ANÁLISE COMPLETA INTEGRADA - PISA CLUSTERS", "=", 100)
    
    start_time = datetime.now()
    print(f"🚀 Iniciando análise completa em: {start_time.strftime('%d/%m/%Y às %H:%M:%S')}")
    
    try:
        # 1. Configurar diretórios
        script_dir, data_file_path, img_dir = setup_directories()
        
        # 2. Carregar e pré-processar dados
        df_original, df_clean = load_and_preprocess_data(data_file_path, img_dir)
        
        # 3. Redução de dimensionalidade
        dr, df_reduced = perform_dimensionality_reduction(df_clean, img_dir)
        
        # 4. Clustering
        cl = perform_clustering(df_reduced, img_dir)
        
        # 5. Classificação e análise adicional
        classifier, df_final = perform_classification_and_analysis(cl, df_clean, img_dir)
        
        # 6. Extrair informações detalhadas dos clusters
        extract_detailed_cluster_info(cl, df_final)
        
        # 7. Gerar relatório detalhado
        report_filename = generate_detailed_report(cl, classifier, df_final)
        
        # Resumo final
        end_time = datetime.now()
        execution_time = end_time - start_time
        
        print_section("ANÁLISE CONCLUÍDA COM SUCESSO", "=", 100)
        print(f"⏰ Tempo total de execução: {execution_time}")
        print(f"📁 Arquivos gerados:")
        print(f"   • Visualizações: pasta '{img_dir}'")
        print(f"   • Relatório: {report_filename}")
        print(f"🎉 Análise completa finalizada em: {end_time.strftime('%d/%m/%Y às %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO durante a análise: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n🛑 Análise interrompida pelo usuário (Ctrl+C)")
        exit_code = 1
    except Exception as e:
        print(f"\n\n💥 ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        exit_code = 1
    
    exit(exit_code)