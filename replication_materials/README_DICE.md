# Análise DICE para Explicabilidade de Clusters

Este diretório contém scripts que utilizam **DiCE (Diverse Counterfactual Explanations)** para análise de explicabilidade de clusters, baseados no script original `paper_script.py`.

## 📋 Arquivos Criados

### 1. `paper_script_dice.py`
- **Descrição**: Versão estendida do script original que integra análise DICE
- **Funcionalidades**:
  - Todo o pipeline original (pré-processamento, redução de dimensionalidade, clustering, classificação)
  - Análise de contrafactuais usando DICE
  - Geração de explicações sobre como mover estudantes entre clusters
  - Salvamento de resultados em CSV e relatórios

### 2. `dice_analysis_example.py`
- **Descrição**: Script detalhado e educativo para análise DICE
- **Funcionalidades**:
  - Exemplo passo-a-passo de uso do DICE
  - Análise das características de cada cluster
  - Geração de contrafactuais para todas as transições possíveis
  - Visualizações (heatmaps, gráficos de barras)
  - Relatórios detalhados

## 🚀 Instalação e Configuração

### Pré-requisitos
```bash
# Instalar DiCE
pip install dice-ml

# Ou versão específica (recomendado)
pip install dice-ml==0.9

# Dependências adicionais se necessário
pip install scikit-learn pandas numpy matplotlib seaborn
```

### Verificação da Instalação
```python
import dice_ml
print(f"DiCE versão: {dice_ml.__version__}")
```

## 📊 Como Usar

### Opção 1: Script Integrado (Recomendado para análise completa)
```bash
cd replication_materials
python paper_script_dice.py
```

**Saídas geradas**:
- `img_dice/`: Todas as visualizações do pipeline + DICE
- `dice_results/`: Contrafactuais em CSV + relatório

### Opção 2: Script Educativo (Recomendado para aprendizado)
```bash
cd replication_materials
python dice_analysis_example.py
```

**Saídas geradas**:
- `dice_detailed_results/`: Análise detalhada com visualizações
- Heatmaps de mudanças necessárias
- Gráficos das principais transições

## 🔍 O que é DICE?

**DiCE (Diverse Counterfactual Explanations)** é uma ferramenta de explicabilidade que responde à pergunta:

> *"O que precisa mudar nos dados de entrada para obter uma predição diferente?"*

### Exemplo Prático
Se um estudante está no **Cluster 1** (baixo desempenho), DICE pode mostrar:
- Quais variáveis precisam mudar
- Em quanto precisam mudar
- Para mover o estudante para o **Cluster 2** (alto desempenho)

## 📈 Interpretação dos Resultados

### 1. Contrafactuais Individuais
```
Amostra original (Cluster 1):
  ESCS: -0.5 (status socioeconômico baixo)
  TEACHSUP: 0.2 (suporte moderado do professor)
  JOYREAD: -0.3 (baixo prazer em ler)

Contrafactual para Cluster 2:
  ESCS: 0.1 (+0.6) ← Melhorar status socioeconômico
  TEACHSUP: 0.8 (+0.6) ← Aumentar suporte do professor
  JOYREAD: 0.4 (+0.7) ← Aumentar prazer em ler
```

### 2. Análise Agregada
- **Heatmap**: Mostra padrões de mudanças entre todos os clusters
- **Gráfico de Barras**: Destaca as mudanças mais importantes
- **Relatórios**: Resumem insights principais

## 🎯 Casos de Uso

### 1. **Intervenções Educacionais**
- Identificar quais fatores mudar para melhorar o desempenho dos estudantes
- Priorizar intervenções baseadas na magnitude das mudanças necessárias

### 2. **Análise de Políticas**
- Entender quais políticas educacionais teriam maior impacto
- Simular efeitos de mudanças em variáveis específicas

### 3. **Pesquisa Educacional**
- Descobrir relações causais entre variáveis
- Validar teorias sobre fatores de sucesso acadêmico

## 📁 Estrutura de Saídas

```
replication_materials/
├── img_dice/                    # Visualizações do pipeline completo
│   ├── missing_heatmap.jpg
│   ├── clustering_*.jpg
│   └── classifier_*.jpg
├── dice_results/                # Resultados DICE básicos
│   ├── counterfactuals_cluster_1_to_2.csv
│   ├── counterfactuals_cluster_2_to_3.csv
│   └── dice_analysis_report.txt
└── dice_detailed_results/       # Análise DICE detalhada
    ├── counterfactual_changes_heatmap.png
    ├── top_counterfactual_changes.png
    ├── counterfactuals_*.csv
    └── dice_detailed_report.txt
```

## ⚙️ Configurações Avançadas

### Personalizar Variáveis Analisadas
```python
# No script, modifique a lista de variáveis:
important_vars = [
    'ESCS',      # Índice socioeconômico
    'TEACHSUP',  # Suporte do professor
    'JOYREAD',   # Prazer em ler
    # Adicione suas variáveis de interesse
]
```

### Ajustar Parâmetros DICE
```python
counterfactuals = dice_explainer.generate_counterfactuals(
    query_instance,
    total_CFs=5,           # Número de contrafactuais
    desired_class=target,  # Cluster alvo
    proximity_weight=0.5,  # Peso para proximidade
    diversity_weight=1.0   # Peso para diversidade
)
```

## 🔧 Solução de Problemas

### Erro: "DiCE não está instalado"
```bash
pip install dice-ml
# ou
conda install -c conda-forge dice-ml
```

### Erro: "Nenhum contrafactual válido foi gerado"
- **Causa**: Clusters muito similares ou modelo muito complexo
- **Solução**: 
  - Ajustar parâmetros do DICE
  - Usar menos variáveis
  - Verificar qualidade dos clusters

### Erro de Memória

- **Causa**: Dataset muito grande
- **Solução**:
  - Reduzir número de amostras
  - Usar menos variáveis
  - Processar clusters individualmente

## 📚 Referências

1. **DiCE Paper**: Mothilal, R. K., Sharma, A., & Tan, C. (2020).
   Explaining machine learning classifiers through diverse counterfactual
   explanations.
2. **DiCE Documentation**: <https://github.com/interpretml/DiCE>
3. **Tutorial**: <https://dice-ml.readthedocs.io/>

## 🤝 Contribuições

Para melhorar estes scripts:

1. Adicione novos métodos de geração de contrafactuais
2. Implemente visualizações mais avançadas
3. Crie análises estatísticas dos contrafactuais
4. Adicione validação cruzada dos resultados

---

**Nota**: Estes scripts são baseados no `paper_script.py` original e mantêm
toda a funcionalidade existente, adicionando capacidades de explicabilidade
com DICE.