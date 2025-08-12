import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

def create_simulated_data(n_samples=1000, n_features=20, n_clusters=4):
    """
    Cria dados simulados para testar o processo de clustering
    """
    np.random.seed(42)
    
    # Gerar dados com estrutura de clusters
    data = []
    labels = []
    
    for cluster_id in range(n_clusters):
        # Cada cluster tem características diferentes
        cluster_center = np.random.randn(n_features) * 2
        cluster_data = np.random.randn(n_samples // n_clusters, n_features) + cluster_center
        
        data.append(cluster_data)
        labels.extend([cluster_id] * (n_samples // n_clusters))
    
    # Combinar todos os dados
    X = np.vstack(data)
    y = np.array(labels)
    
    # Criar DataFrame com nomes de colunas similares aos dados reais
    feature_names = [f'feature_{i:02d}' for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['true_cluster'] = y
    
    return df

def simulate_clustering_pipeline(df, n_components=10, n_clusters=4):
    """
    Simula o pipeline completo de clustering
    """
    print("=== MODO SIMULAÇÃO - TESTE RÁPIDO ===")
    print(f"Dados simulados: {df.shape[0]} amostras, {df.shape[1]-1} features")
    
    # Separar features e target
    X = df.drop('true_cluster', axis=1)
    y_true = df['true_cluster']
    
    # 1. Padronização
    print("\n1. Padronizando dados...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Redução de dimensionalidade
    print(f"\n2. Aplicando PCA ({n_components} componentes)...")
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    # Criar DataFrame com componentes principais
    pca_columns = [f'dim_{i:02d}' for i in range(1, n_components + 1)]
    df_pca = pd.DataFrame(X_pca, columns=pca_columns)
    
    print(f"Variância explicada: {pca.explained_variance_ratio_.sum():.3f}")
    
    # 3. Clustering
    print(f"\n3. Aplicando K-Means ({n_clusters} clusters)...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_pca)
    
    # Adicionar labels de cluster ao DataFrame
    df_pca['cluster'] = cluster_labels
    
    # 4. Análise dos clusters
    print("\n4. Analisando clusters...")
    cluster_summary = df_pca.groupby('cluster').agg({
        **{col: ['mean', 'std'] for col in pca_columns}
    }).round(3)
    
    print("\nResumo dos clusters (médias dos componentes principais):")
    for cluster_id in range(n_clusters):
        cluster_data = df_pca[df_pca['cluster'] == cluster_id]
        print(f"\nCluster {cluster_id}: {len(cluster_data)} amostras")
        
        # Mostrar os 3 componentes mais distintivos
        cluster_means = cluster_data[pca_columns].mean()
        global_means = df_pca[pca_columns].mean()
        differences = abs(cluster_means - global_means)
        top_components = differences.nlargest(3)
        
        print("Componentes mais distintivos:")
        for i, (component, diff) in enumerate(top_components.items(), 1):
            cluster_val = cluster_means[component]
            global_val = global_means[component]
            print(f"  {i}. {component}: {cluster_val:.3f} (global: {global_val:.3f}, diff: {diff:.3f})")
    
    # 5. Classificação para validação
    print("\n5. Testando classificação...")
    rf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
    rf.fit(X_pca, cluster_labels)
    
    # Importância das features
    feature_importance = pd.Series(rf.feature_importances_, index=pca_columns)
    feature_importance = feature_importance.sort_values(ascending=False)
    
    print("\nImportância das features (top 5):")
    for i, (feature, importance) in enumerate(feature_importance.head(5).items(), 1):
        print(f"  {i}. {feature}: {importance:.3f}")
    
    # Métricas de classificação (usando clusters como target)
    y_pred = rf.predict(X_pca)
    report = classification_report(cluster_labels, y_pred, output_dict=True)
    
    print("\n6. Métricas de classificação:")
    print(f"Acurácia: {report['accuracy']:.3f}")
    print(f"Macro F1-score: {report['macro avg']['f1-score']:.3f}")
    print(f"Weighted F1-score: {report['weighted avg']['f1-score']:.3f}")
    
    # Retornar resultados para testes adicionais
    results = {
        'df_original': df,
        'df_pca': df_pca,
        'pca_model': pca,
        'kmeans_model': kmeans,
        'scaler': scaler,
        'classifier': rf,
        'feature_importance': feature_importance,
        'classification_report': report
    }
    
    return results

def test_cluster_description_logic(results):
    """
    Testa especificamente a lógica de descrição de clusters
    que estava causando problemas no script original
    """
    print("\n=== TESTE DA LÓGICA DE DESCRIÇÃO ===")
    
    df_pca = results['df_pca']
    feature_importance = results['feature_importance']
    classification_report = results['classification_report']
    
    # Testar a formatação que estava causando erro
    print("\nTestando formatação de importância:")
    try:
        for i, (var_name, importance_val) in enumerate(feature_importance.head(5).items(), 1):
            # Garantir que importance_val é um número
            if hasattr(importance_val, 'item'):
                importance_val = importance_val.item()
            elif hasattr(importance_val, '__len__') and len(importance_val) > 0:
                importance_val = float(importance_val[0])
            else:
                importance_val = float(importance_val)
            
            formatted_line = f"{i:2d}. {var_name}: {importance_val:.3f}"
            print(f"  {formatted_line}")
        print("✓ Formatação de importância funcionando")
    except Exception as e:
        print(f"✗ Erro na formatação: {e}")
    
    # Testar acesso às métricas de classificação
    print("\nTestando acesso às métricas:")
    try:
        accuracy = classification_report.get('accuracy', 'N/A')
        macro_f1 = classification_report.get('macro avg', {}).get('f1-score', 'N/A')
        weighted_f1 = classification_report.get('weighted avg', {}).get('f1-score', 'N/A')
        
        print(f"  Acurácia: {accuracy}")
        print(f"  Macro F1: {macro_f1}")
        print(f"  Weighted F1: {weighted_f1}")
        print("✓ Acesso às métricas funcionando")
    except Exception as e:
        print(f"✗ Erro no acesso às métricas: {e}")

def main():
    """
    Função principal para executar a simulação
    """
    print("SIMULADOR DE CLUSTERING - TESTE RÁPIDO")
    print("=" * 50)
    
    # Criar dados simulados
    print("Criando dados simulados...")
    df = create_simulated_data(n_samples=500, n_features=15, n_clusters=4)
    
    # Executar pipeline simulado
    results = simulate_clustering_pipeline(df, n_components=8, n_clusters=4)
    
    # Testar lógica específica que estava com problemas
    test_cluster_description_logic(results)
    
    print("\n" + "=" * 50)
    print("SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print("\nEste modo simulado permite testar rapidamente:")
    print("- Lógica de clustering")
    print("- Formatação de resultados")
    print("- Acesso a métricas")
    print("- Descrição de clusters")
    print("\nUse este script para testar alterações antes de")
    print("executar o script completo com dados reais.")

if __name__ == "__main__":
    main()