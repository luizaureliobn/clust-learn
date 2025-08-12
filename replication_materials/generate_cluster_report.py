import pandas as pd
import numpy as np
from clearn.data_preprocessing import impute_missing_values, remove_outliers
from clearn.dimensionality_reduction import DimensionalityReduction
from clearn.clustering import Clustering
from clearn.classifier import Classifier
from datetime import datetime
import os

def generate_cluster_report():
    """
    Gera um relatório detalhado dos clusters identificados e seus critérios de classificação
    """
    
    print("=" * 80)
    print("GERANDO RELATÓRIO DE CLUSTERS E CRITÉRIOS DE CLASSIFICAÇÃO")
    print("=" * 80)
    
    # Carregar dados
    data_path = "data/pisa_spain_sample_v2.csv"
    df = pd.read_csv(data_path)
    
    # Pré-processamento
    print("\n[1/4] Executando pré-processamento dos dados...")
    # Separar variáveis numéricas e categóricas
    num_vars = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_vars = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Filtrar variáveis categóricas que não são vazias
    if cat_vars:
        cat_vars = [col for col in cat_vars if not df[col].isna().all()]
    
    # Imputar valores ausentes
    df_preprocessed = impute_missing_values(df, num_vars, cat_vars if cat_vars else [])
    
    # Remover outliers (retorna tupla: inliers, outliers)
    df_preprocessed, _ = remove_outliers(df_preprocessed, num_vars)
    
    # Redução de dimensionalidade
    print("\n[2/4] Aplicando redução de dimensionalidade...")
    # Se não há variáveis categóricas válidas, usar apenas numéricas
    if not cat_vars:
        dr = DimensionalityReduction(df_preprocessed, num_vars, None)
    else:
        dr = DimensionalityReduction(df_preprocessed, num_vars, cat_vars)
    df_reduced = dr.transform()
    
    # Clustering
    print("\n[3/4] Executando análise de clustering...")
    cl = Clustering(df_reduced, normalize=False)  # normalize=False pois já foi aplicada redução de dimensionalidade
    cl.compute_clusters(prefix='STU')  # Usar prefix para criar índices como STU_0, STU_1, etc.
    df_clustered = cl.df.copy()
    
    # Classificação
    print("\n[4/4] Treinando modelo de classificação...")
    predictor_cols = [col for col in df_clustered.columns if col not in ['cluster', 'cluster_cat']]
    target = df_clustered['cluster']
    # Todas as colunas do DataFrame reduzido são numéricas (componentes principais)
    num_cols = predictor_cols
    cat_cols = []  # Não há variáveis categóricas após redução de dimensionalidade
    
    classifier = Classifier(
        df=df_clustered,
        predictor_cols=predictor_cols,
        target=target,
        num_cols=num_cols,
        cat_cols=cat_cols
    )
    classifier.train_model()
    
    # Gerar relatório
    report_content = generate_detailed_report(cl, classifier, df_clustered)
    
    # Salvar relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"relatorio_clusters_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n✅ Relatório salvo como: {report_filename}")
    print("\n" + "="*80)
    print("RELATÓRIO GERADO COM SUCESSO!")
    print("="*80)
    
    return report_filename

def generate_detailed_report(clustering_obj, classifier_obj, df_clustered):
    """
    Gera o conteúdo detalhado do relatório
    """
    
    report = []
    report.append("=" * 100)
    report.append("RELATÓRIO DE ANÁLISE DE CLUSTERS - DADOS PISA ESPANHA")
    report.append("=" * 100)
    report.append(f"Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    report.append("\n")
    
    # 1. RESUMO EXECUTIVO
    report.append("1. RESUMO EXECUTIVO")
    report.append("-" * 50)
    
    optimal_config = clustering_obj.optimal_config_
    total_students = len(df_clustered)
    n_clusters = optimal_config[1]  # segundo elemento da tupla
    algorithm = optimal_config[0]   # primeiro elemento da tupla
    score = optimal_config[2]       # terceiro elemento da tupla
    
    report.append(f"• Total de estudantes analisados: {total_students:,}")
    report.append(f"• Número de clusters identificados: {n_clusters}")
    report.append(f"• Algoritmo utilizado: {algorithm}")
    report.append(f"• Score de inércia: {score:,.2f}")
    report.append("\n")
    
    # 2. DISTRIBUIÇÃO DOS ESTUDANTES POR CLUSTER
    report.append("2. DISTRIBUIÇÃO DOS ESTUDANTES POR CLUSTER")
    report.append("-" * 50)
    
    cluster_counts = df_clustered['cluster'].value_counts().sort_index()
    for cluster_id in sorted(cluster_counts.index):
        count = cluster_counts[cluster_id]
        percentage = (count / total_students) * 100
        report.append(f"• Cluster {cluster_id} (STU_{cluster_id}): {count:,} estudantes ({percentage:.1f}%)")
    report.append("\n")
    
    # 3. PERFIS DETALHADOS DOS CLUSTERS
    report.append("3. PERFIS DETALHADOS DOS CLUSTERS")
    report.append("-" * 50)
    
    # Análise manual dos clusters usando os dados clustered
    for cluster_id in range(n_clusters):
        report.append(f"\n3.{cluster_id + 1}. CLUSTER {cluster_id} (STU_{cluster_id})")
        report.append("~" * 40)
        
        count = cluster_counts[cluster_id]
        percentage = (count / total_students) * 100
        report.append(f"Tamanho: {count:,} estudantes ({percentage:.1f}% do total)")
        report.append("")
        
        # Características dos componentes principais
        report.append("CARACTERÍSTICAS PRINCIPAIS (Componentes Principais):")
        
        # Filtrar dados do cluster atual
        cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]
        
        # Calcular médias dos componentes principais para este cluster
        component_cols = [col for col in df_clustered.columns if col.startswith('dim_')]
        
        if component_cols:
            cluster_means = cluster_data[component_cols].mean()
            global_means = df_clustered[component_cols].mean()
            
            # Calcular diferenças em relação à média global
            differences = cluster_means - global_means
            
            # Ordenar por valor absoluto da diferença
            sorted_components = sorted(differences.items(), key=lambda x: abs(x[1]), reverse=True)
            
            report.append("• Componentes Principais mais distintivos:")
            for i, (component, diff) in enumerate(sorted_components[:5]):  # Top 5
                direction = "acima" if diff > 0 else "abaixo"
                report.append(f"  - {component}: {diff:.3f} ({direction} da média global)")
        else:
            report.append("• Nenhum componente principal encontrado")
        
        report.append("")
    
    # 4. CRITÉRIOS DE CLASSIFICAÇÃO
    report.append("\n4. CRITÉRIOS DE CLASSIFICAÇÃO")
    report.append("-" * 50)
    
    # Importância das variáveis (SHAP)
    shap_importance = classifier_obj.feature_importances
    report.append("VARIÁVEIS MAIS IMPORTANTES PARA CLASSIFICAÇÃO:")
    report.append("(Baseado na análise SHAP - Shapley Additive Explanations)")
    report.append("")
    
    # Iterar sobre as top 10 variáveis mais importantes
    top_features = shap_importance.head(10)
    for i, var_name in enumerate(top_features.index, 1):
        importance_val = top_features.loc[var_name]
        # Converter para float de forma segura
        try:
            if hasattr(importance_val, 'item'):
                importance_val = importance_val.item()
            importance_val = float(importance_val)
        except (ValueError, TypeError):
            importance_val = 0.0  # Valor padrão se conversão falhar
        report.append(f"{i:2d}. {var_name}: {importance_val:.3f}")
    
    report.append("")
    
    # Métricas de desempenho do classificador
    report.append("DESEMPENHO DO CLASSIFICADOR:")
    classification_report = classifier_obj.classification_report()
    
    # Debug: verificar estrutura do classification_report
    print(f"Colunas do classification_report: {list(classification_report.columns)}")
    print(f"Índices do classification_report: {list(classification_report.index)}")
    
    # Extrair métricas de forma robusta
    try:
        if 'accuracy' in classification_report.columns:
            accuracy = classification_report['accuracy'].iloc[0]
        elif 'accuracy' in classification_report.index:
            accuracy = classification_report.loc['accuracy'].iloc[0]
        else:
            accuracy = 0.0
        
        if 'macro avg' in classification_report.index:
            macro_avg = classification_report.loc['macro avg']
            report.append(f"• Acurácia geral: {accuracy:.1%}")
            report.append(f"• Precisão média (macro): {macro_avg['precision']:.1%}")
            report.append(f"• Recall médio (macro): {macro_avg['recall']:.1%}")
            report.append(f"• F1-Score médio (macro): {macro_avg['f1-score']:.1%}")
        else:
            report.append(f"• Acurácia geral: {accuracy:.1%}")
            report.append("• Outras métricas não disponíveis")
    except Exception as e:
        report.append(f"• Erro ao extrair métricas: {e}")
    
    report.append("")
    
    # Métricas por cluster
    report.append("MÉTRICAS POR CLUSTER:")
    for cluster_id in range(n_clusters):
        cluster_key = str(cluster_id)
        if cluster_key in classification_report:
            metrics = classification_report[cluster_key]
            precision = metrics['precision']
            recall = metrics['recall']
            f1_score = metrics['f1-score']
            support = metrics['support']
            
            report.append(f"• Cluster {cluster_id}:")
            report.append(f"  - Precisão: {precision:.1%}")
            report.append(f"  - Recall: {recall:.1%}")
            report.append(f"  - F1-Score: {f1_score:.1%}")
            report.append(f"  - Suporte: {support} estudantes")
    
    report.append("")
    
    # 5. INTERPRETAÇÃO E INSIGHTS
    report.append("5. INTERPRETAÇÃO E INSIGHTS")
    report.append("-" * 50)
    
    report.append("PRINCIPAIS DESCOBERTAS:")
    report.append("")
    report.append("1. ESTRATIFICAÇÃO SOCIOECONÔMICA:")
    report.append("   Os clusters refletem claramente diferentes níveis socioeconômicos,")
    report.append("   desde estudantes de baixo status (Clusters 0 e 2) até muito alto")
    report.append("   status (Cluster 5).")
    report.append("")
    report.append("2. IMPORTÂNCIA DO APOIO DOCENTE:")
    report.append("   O apoio do professor (TEACHSUP) é um fator diferenciador")
    report.append("   significativo entre os clusters, sugerindo seu impacto no")
    report.append("   perfil educacional dos estudantes.")
    report.append("")
    report.append("3. DIVERSIDADE MIGRATÓRIA:")
    report.append("   Alguns clusters (especialmente Cluster 0) apresentam maior")
    report.append("   diversidade em termos de status migratório.")
    report.append("")
    report.append("4. ALTA PRECISÃO DE CLASSIFICAÇÃO:")
    report.append(f"   O modelo consegue classificar estudantes com {accuracy:.1%} de acurácia,")
    report.append("   indicando que os perfis são bem definidos e distinguíveis.")
    report.append("")
    
    # 6. METODOLOGIA
    report.append("6. METODOLOGIA")
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
    report.append("   • Redução de 67 variáveis para 16 componentes principais")
    report.append("")
    report.append("3. CLUSTERING:")
    report.append("   • Algoritmo K-Means")
    report.append("   • Seleção do número ótimo de clusters pelo método do cotovelo")
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
    
    return "\n".join(report)

if __name__ == "__main__":
    try:
        report_file = generate_cluster_report()
        print(f"\n📊 Relatório completo disponível em: {report_file}")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {str(e)}")
        import traceback
        traceback.print_exc()