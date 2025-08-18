# Exemplo detalhado de uso do DICE para análise de explicabilidade de clusters
# Este script demonstra como usar DiCE (Diverse Counterfactual Explanations) 
# para entender quais mudanças são necessárias para mover estudantes entre clusters

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import os

# Verificar se DICE está instalado
try:
    import dice_ml
    from dice_ml import Dice
    print("✓ DiCE está instalado e pronto para uso")
except ImportError:
    print("❌ DiCE não está instalado.")
    print("Para instalar, execute: pip install dice-ml")
    print("Ou se preferir uma versão específica: pip install dice-ml==0.9")
    exit(1)

def load_and_prepare_data(data_path):
    """
    Carrega e prepara os dados para análise DICE
    """
    print("Carregando dados...")
    df = pd.read_csv(data_path)
    
    # Selecionar variáveis numéricas importantes para análise
    important_vars = [
        'ESCS',  # Índice socioeconômico
        'TEACHSUP',  # Suporte do professor
        'JOYREAD',  # Prazer em ler
        'PERCOMP',  # Competição percebida
        'BELONG',  # Sentimento de pertencimento
        'RESILIENCE',  # Resiliência
        'GCSELFEFF',  # Autoeficácia
        'COMPICT',  # Competência em ICT
        'HOMEPOS',  # Posses domésticas
        'WEALTH'  # Riqueza familiar
    ]
    
    # Filtrar apenas as variáveis disponíveis
    available_vars = [var for var in important_vars if var in df.columns]
    print(f"Variáveis disponíveis para análise: {available_vars}")
    
    return df, available_vars

def create_synthetic_clusters(df, features, n_clusters=3):
    """
    Cria clusters sintéticos para demonstração (caso não existam clusters pré-definidos)
    """
    from sklearn.cluster import KMeans
    
    # Preparar dados
    X = df[features].dropna()
    
    # Normalizar dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Aplicar K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Criar dataframe com clusters
    result_df = X.copy()
    result_df['cluster'] = clusters
    
    print(f"Clusters criados: {np.unique(clusters)}")
    print(f"Distribuição dos clusters: {np.bincount(clusters)}")
    
    return result_df, scaler

def train_cluster_classifier(df, features):
    """
    Treina um classificador para predizer clusters
    """
    print("\nTreinando classificador de clusters...")
    
    X = df[features]
    y = df['cluster']
    
    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Treinar modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Avaliar modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Acurácia do classificador: {accuracy:.3f}")
    print("\nRelatório de classificação:")
    print(classification_report(y_test, y_pred))
    
    return model, X_train, X_test, y_train, y_test

def analyze_cluster_characteristics(df, features):
    """
    Analisa as características de cada cluster
    """
    print("\n=== ANÁLISE DAS CARACTERÍSTICAS DOS CLUSTERS ===")
    
    for cluster_id in sorted(df['cluster'].unique()):
        cluster_data = df[df['cluster'] == cluster_id]
        print(f"\n--- Cluster {cluster_id} (n={len(cluster_data)}) ---")
        
        # Estatísticas descritivas
        cluster_stats = cluster_data[features].describe()
        global_stats = df[features].describe()
        
        # Mostrar diferenças significativas
        print("Características distintivas (diferença > 0.2 desvios padrão):")
        for feature in features:
            cluster_mean = cluster_stats.loc['mean', feature]
            global_mean = global_stats.loc['mean', feature]
            global_std = global_stats.loc['std', feature]
            
            if global_std > 0:
                diff_std = (cluster_mean - global_mean) / global_std
                if abs(diff_std) > 0.2:
                    direction = "↑" if diff_std > 0 else "↓"
                    print(f"  {feature}: {cluster_mean:.3f} {direction} (diff: {diff_std:+.2f}σ)")

def generate_counterfactuals_analysis(df, features, model, output_dir):
    """
    Gera e analisa contrafactuais usando DICE
    """
    print("\n=== ANÁLISE DE CONTRAFACTUAIS COM DICE ===")
    
    # Configurar DICE
    dice_data = dice_ml.Data(
        dataframe=df,
        continuous_features=features,
        outcome_name='cluster'
    )
    
    dice_model = dice_ml.Model(
        model=model,
        backend='sklearn'
    )
    
    # Criar explainer
    explainer = Dice(dice_data, dice_model, method='random')
    
    clusters = sorted(df['cluster'].unique())
    counterfactual_results = {}
    
    # Para cada cluster, gerar contrafactuais para outros clusters
    for source_cluster in clusters:
        print(f"\n--- Analisando transições do Cluster {source_cluster} ---")
        
        # Selecionar amostra representativa do cluster
        cluster_samples = df[df['cluster'] == source_cluster]
        if len(cluster_samples) == 0:
            continue
            
        # Usar a mediana como amostra representativa
        representative_sample = cluster_samples[features].median().to_frame().T
        
        print(f"Amostra representativa do Cluster {source_cluster}:")
        for feature, value in representative_sample.iloc[0].items():
            print(f"  {feature}: {value:.3f}")
        
        for target_cluster in clusters:
            if source_cluster == target_cluster:
                continue
                
            try:
                print(f"\nGerando contrafactuais: Cluster {source_cluster} → Cluster {target_cluster}")
                
                # Gerar contrafactuais
                counterfactuals = explainer.generate_counterfactuals(
                    representative_sample,
                    total_CFs=5,
                    desired_class=target_cluster
                )
                
                cf_examples = counterfactuals.cf_examples_list[0]
                if cf_examples.final_cfs_df is not None and len(cf_examples.final_cfs_df) > 0:
                    cf_df = cf_examples.final_cfs_df
                    
                    # Analisar mudanças necessárias
                    original_values = representative_sample.iloc[0]
                    
                    print(f"Contrafactuais gerados: {len(cf_df)}")
                    
                    # Calcular mudanças médias
                    changes_summary = []
                    for _, cf_row in cf_df.iterrows():
                        changes = cf_row[features] - original_values
                        changes_summary.append(changes)
                    
                    if changes_summary:
                        avg_changes = pd.DataFrame(changes_summary).mean()
                        
                        print("Mudanças médias necessárias:")
                        significant_changes = avg_changes[abs(avg_changes) > 0.1].sort_values(key=abs, ascending=False)
                        
                        for feature, change in significant_changes.head(5).items():
                            direction = "aumentar" if change > 0 else "diminuir"
                            print(f"  {feature}: {direction} em {abs(change):.3f}")
                        
                        # Salvar resultados
                        key = f"cluster_{source_cluster}_to_{target_cluster}"
                        counterfactual_results[key] = {
                            'original': original_values,
                            'counterfactuals': cf_df,
                            'avg_changes': avg_changes,
                            'significant_changes': significant_changes
                        }
                        
                        # Salvar CSV
                        cf_filename = os.path.join(output_dir, f"counterfactuals_{key}.csv")
                        cf_df.to_csv(cf_filename, index=False)
                        
                else:
                    print("  Nenhum contrafactual válido foi gerado")
                    
            except Exception as e:
                print(f"  Erro ao gerar contrafactuais: {str(e)}")
    
    return counterfactual_results

def create_counterfactual_visualization(counterfactual_results, output_dir):
    """
    Cria visualizações dos resultados dos contrafactuais
    """
    print("\n=== CRIANDO VISUALIZAÇÕES ===")
    
    if not counterfactual_results:
        print("Nenhum resultado de contrafactual para visualizar")
        return
    
    # Compilar todas as mudanças significativas
    all_changes = []
    for key, result in counterfactual_results.items():
        source, target = key.replace('cluster_', '').replace('_to_', ' ').split()
        for feature, change in result['significant_changes'].items():
            all_changes.append({
                'transition': f"C{source}→C{target}",
                'feature': feature,
                'change': change,
                'abs_change': abs(change)
            })
    
    if all_changes:
        changes_df = pd.DataFrame(all_changes)
        
        # Criar heatmap das mudanças
        plt.figure(figsize=(12, 8))
        pivot_df = changes_df.pivot(index='feature', columns='transition', values='change')
        
        sns.heatmap(pivot_df, annot=True, cmap='RdBu_r', center=0, 
                   fmt='.2f', cbar_kws={'label': 'Mudança Necessária'})
        plt.title('Mudanças Necessárias para Transições entre Clusters')
        plt.xlabel('Transição')
        plt.ylabel('Variável')
        plt.tight_layout()
        
        heatmap_path = os.path.join(output_dir, 'counterfactual_changes_heatmap.png')
        plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Heatmap salvo em: {heatmap_path}")
        
        # Criar gráfico de barras das mudanças mais importantes
        plt.figure(figsize=(10, 6))
        top_changes = changes_df.nlargest(15, 'abs_change')
        
        colors = ['red' if x < 0 else 'blue' for x in top_changes['change']]
        plt.barh(range(len(top_changes)), top_changes['change'], color=colors, alpha=0.7)
        plt.yticks(range(len(top_changes)), 
                  [f"{row['feature']} ({row['transition']})" for _, row in top_changes.iterrows()])
        plt.xlabel('Magnitude da Mudança')
        plt.title('Top 15 Mudanças Mais Significativas')
        plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        plt.tight_layout()
        
        barplot_path = os.path.join(output_dir, 'top_counterfactual_changes.png')
        plt.savefig(barplot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Gráfico de barras salvo em: {barplot_path}")

def main():
    """
    Função principal
    """
    print("=== ANÁLISE DICE PARA EXPLICABILIDADE DE CLUSTERS ===")
    
    # Configurar caminhos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', 'pisa_spain_sample_v2.csv')
    output_dir = os.path.join(script_dir, 'dice_detailed_results')
    
    # Criar diretório de saída
    os.makedirs(output_dir, exist_ok=True)
    
    # Verificar se arquivo de dados existe
    if not os.path.exists(data_path):
        print(f"❌ Arquivo de dados não encontrado: {data_path}")
        print("Certifique-se de que o arquivo pisa_spain_sample_v2.csv está na pasta 'data'")
        return
    
    try:
        # 1. Carregar e preparar dados
        df, features = load_and_prepare_data(data_path)
        
        # 2. Criar clusters (ou usar clusters existentes)
        df_clustered, scaler = create_synthetic_clusters(df, features, n_clusters=3)
        
        # 3. Treinar classificador
        model, X_train, X_test, y_train, y_test = train_cluster_classifier(df_clustered, features)
        
        # 4. Analisar características dos clusters
        analyze_cluster_characteristics(df_clustered, features)
        
        # 5. Gerar análise de contrafactuais
        counterfactual_results = generate_counterfactuals_analysis(
            df_clustered, features, model, output_dir
        )
        
        # 6. Criar visualizações
        create_counterfactual_visualization(counterfactual_results, output_dir)
        
        # 7. Criar relatório final
        report_path = os.path.join(output_dir, 'dice_detailed_report.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DETALHADO - ANÁLISE DICE\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Dataset: {len(df_clustered)} amostras\n")
            f.write(f"Features analisadas: {len(features)}\n")
            f.write(f"Clusters: {sorted(df_clustered['cluster'].unique())}\n")
            f.write(f"Transições analisadas: {len(counterfactual_results)}\n\n")
            
            f.write("FEATURES UTILIZADAS:\n")
            for i, feature in enumerate(features, 1):
                f.write(f"{i:2d}. {feature}\n")
            
            f.write("\nTRANSIÇÕES ANALISADAS:\n")
            for key in counterfactual_results.keys():
                f.write(f"- {key}\n")
        
        print(f"\n✓ Análise completa! Resultados salvos em: {output_dir}")
        print(f"✓ Relatório detalhado: {report_path}")
        
    except Exception as e:
        print(f"❌ Erro durante a análise: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()