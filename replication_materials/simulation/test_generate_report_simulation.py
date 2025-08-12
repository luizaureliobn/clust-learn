import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

def create_mock_clustering_object():
    """
    Cria um objeto mock que simula o comportamento do clustering real
    """
    class MockClustering:
        def __init__(self):
            # Criar dados simulados
            np.random.seed(42)
            n_samples = 300
            n_components = 8
            n_clusters = 4
            
            # Dados PCA simulados
            self.X_pca = np.random.randn(n_samples, n_components)
            self.pca_columns = [f'dim_{i:02d}' for i in range(1, n_components + 1)]
            
            # Clusters simulados
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            self.cluster_labels = kmeans.fit_predict(self.X_pca)
            
            # DataFrame com dados PCA e clusters
            self.df_pca = pd.DataFrame(self.X_pca, columns=self.pca_columns)
            self.df_pca['cluster'] = self.cluster_labels
            
            # Classificador simulado
            self.rf = RandomForestClassifier(n_estimators=50, random_state=42)
            self.rf.fit(self.X_pca, self.cluster_labels)
            
            # Importância das features
            self.feature_importance = pd.Series(
                self.rf.feature_importances_, 
                index=self.pca_columns
            ).sort_values(ascending=False)
            
            # Relatório de classificação
            y_pred = self.rf.predict(self.X_pca)
            self.classification_report = classification_report(
                self.cluster_labels, y_pred, output_dict=True
            )
    
    return MockClustering()

def test_generate_cluster_report_logic():
    """
    Testa a lógica do generate_cluster_report.py usando dados simulados
    """
    print("=== TESTE DA LÓGICA DO GENERATE_CLUSTER_REPORT ===")
    
    # Criar objeto mock
    clustering_obj = create_mock_clustering_object()
    
    # Simular a lógica do script original
    report = []
    report.append("RELATÓRIO DE ANÁLISE DE CLUSTERS")
    report.append("=" * 50)
    
    # 1. Informações gerais
    n_samples = len(clustering_obj.df_pca)
    n_clusters = len(clustering_obj.df_pca['cluster'].unique())
    n_features = len(clustering_obj.pca_columns)
    
    report.append(f"\nInformações Gerais:")
    report.append(f"- Total de amostras: {n_samples}")
    report.append(f"- Número de clusters: {n_clusters}")
    report.append(f"- Número de features (PCA): {n_features}")
    
    # 2. Análise por cluster
    report.append(f"\nAnálise por Cluster:")
    
    for cluster_id in sorted(clustering_obj.df_pca['cluster'].unique()):
        cluster_data = clustering_obj.df_pca[clustering_obj.df_pca['cluster'] == cluster_id]
        cluster_size = len(cluster_data)
        cluster_pct = (cluster_size / n_samples) * 100
        
        report.append(f"\nCluster {cluster_id}:")
        report.append(f"  - Tamanho: {cluster_size} amostras ({cluster_pct:.1f}%)")
        
        # Características distintivas
        cluster_means = cluster_data[clustering_obj.pca_columns].mean()
        global_means = clustering_obj.df_pca[clustering_obj.pca_columns].mean()
        differences = abs(cluster_means - global_means)
        top_features = differences.nlargest(3)
        
        report.append(f"  - Características mais distintivas:")
        for i, (feature, diff) in enumerate(top_features.items(), 1):
            cluster_val = cluster_means[feature]
            global_val = global_means[feature]
            direction = "acima" if cluster_val > global_val else "abaixo"
            report.append(f"    {i}. {feature}: {cluster_val:.3f} ({direction} da média global: {global_val:.3f})")
    
    # 3. Importância das features (testando a formatação que estava com problema)
    report.append(f"\nImportância das Features (Top 10):")
    
    try:
        top_features = clustering_obj.feature_importance.head(10)
        for i, (var_name, importance_val) in enumerate(top_features.items(), 1):
            # Lógica robusta para extrair valor escalar
            if hasattr(importance_val, 'item'):
                importance_val = importance_val.item()
            elif hasattr(importance_val, '__len__') and len(importance_val) > 0:
                importance_val = float(importance_val[0])
            else:
                importance_val = float(importance_val)
            
            report.append(f"  {i:2d}. {var_name}: {importance_val:.3f}")
        
        print("✓ Formatação de importância funcionando corretamente")
    except Exception as e:
        print(f"✗ Erro na formatação de importância: {e}")
        return
    
    # 4. Métricas de desempenho (testando acesso que estava com problema)
    report.append(f"\nMétricas de Desempenho do Classificador:")
    
    try:
        # Acesso robusto às métricas
        classification_report = clustering_obj.classification_report
        
        # Verificar se accuracy existe
        if 'accuracy' in classification_report:
            accuracy = classification_report['accuracy']
            report.append(f"  - Acurácia: {accuracy:.3f}")
        else:
            report.append(f"  - Acurácia: N/A")
        
        # Verificar macro avg
        if 'macro avg' in classification_report:
            macro_f1 = classification_report['macro avg'].get('f1-score', 'N/A')
            macro_precision = classification_report['macro avg'].get('precision', 'N/A')
            macro_recall = classification_report['macro avg'].get('recall', 'N/A')
            
            report.append(f"  - Macro F1-score: {macro_f1:.3f}" if macro_f1 != 'N/A' else "  - Macro F1-score: N/A")
            report.append(f"  - Macro Precision: {macro_precision:.3f}" if macro_precision != 'N/A' else "  - Macro Precision: N/A")
            report.append(f"  - Macro Recall: {macro_recall:.3f}" if macro_recall != 'N/A' else "  - Macro Recall: N/A")
        
        # Verificar weighted avg
        if 'weighted avg' in classification_report:
            weighted_f1 = classification_report['weighted avg'].get('f1-score', 'N/A')
            report.append(f"  - Weighted F1-score: {weighted_f1:.3f}" if weighted_f1 != 'N/A' else "  - Weighted F1-score: N/A")
        
        print("✓ Acesso às métricas funcionando corretamente")
    except Exception as e:
        print(f"✗ Erro no acesso às métricas: {e}")
        return
    
    # 5. Exibir relatório completo
    print("\n" + "\n".join(report))
    
    print("\n" + "=" * 50)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("\nTodas as funcionalidades que estavam com problema foram testadas:")
    print("✓ Formatação de valores de importância")
    print("✓ Acesso às métricas de classificação")
    print("✓ Iteração sobre clusters")
    print("✓ Cálculo de características distintivas")
    
    return clustering_obj

def test_specific_error_scenarios():
    """
    Testa cenários específicos que causavam erros no script original
    """
    print("\n=== TESTE DE CENÁRIOS DE ERRO ESPECÍFICOS ===")
    
    # Cenário 1: Importância como Series
    print("\n1. Testando formatação de Series como importância:")
    try:
        importance_series = pd.Series([0.5, 0.3, 0.2], index=['dim_01', 'dim_02', 'dim_03'])
        for var_name, importance in importance_series.items():
            # Conversão robusta
            if hasattr(importance, 'item'):
                importance_val = importance.item()
            else:
                importance_val = float(importance)
            
            formatted = f"{var_name}: {importance_val:.3f}"
            print(f"  ✓ {formatted}")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    # Cenário 2: Classification report sem accuracy
    print("\n2. Testando classification_report sem 'accuracy':")
    try:
        mock_report = {
            'macro avg': {'f1-score': 0.85, 'precision': 0.87, 'recall': 0.83},
            'weighted avg': {'f1-score': 0.86, 'precision': 0.88, 'recall': 0.84}
        }
        
        accuracy = mock_report.get('accuracy', 'N/A')
        macro_f1 = mock_report.get('macro avg', {}).get('f1-score', 'N/A')
        
        print(f"  ✓ Accuracy: {accuracy}")
        print(f"  ✓ Macro F1: {macro_f1}")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    # Cenário 3: Arrays NumPy como importância
    print("\n3. Testando arrays NumPy como importância:")
    try:
        importance_array = np.array([0.4])
        
        if hasattr(importance_array, 'item'):
            importance_val = importance_array.item()
        elif len(importance_array) == 1:
            importance_val = float(importance_array[0])
        else:
            importance_val = float(importance_array)
        
        formatted = f"feature: {importance_val:.3f}"
        print(f"  ✓ {formatted}")
    except Exception as e:
        print(f"  ✗ Erro: {e}")

def main():
    """
    Função principal para executar todos os testes
    """
    print("SIMULADOR DE TESTE PARA GENERATE_CLUSTER_REPORT")
    print("=" * 60)
    
    # Teste principal
    clustering_obj = test_generate_cluster_report_logic()
    
    # Testes de cenários específicos
    test_specific_error_scenarios()
    
    print("\n" + "=" * 60)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("\nEste script permite:")
    print("- Testar rapidamente a lógica de geração de relatórios")
    print("- Verificar formatação de dados")
    print("- Validar acesso a métricas")
    print("- Simular cenários de erro")
    print("\nUse para desenvolver e corrigir o script principal sem")
    print("esperar pela execução completa dos dados reais.")

if __name__ == "__main__":
    main()