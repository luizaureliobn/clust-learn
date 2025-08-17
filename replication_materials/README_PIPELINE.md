# Pipeline de Análise de Clusters PISA

Este documento explica as diferentes opções para executar a análise completa de clusters dos dados PISA.

## 📋 Resumo dos Scripts

Os scripts `extract_cluster_info.py` e `generate_cluster_report.py` **NÃO são executados automaticamente** pelo `paper_script.py`. Cada um tem funcionalidades específicas e deve ser executado individualmente ou através dos pipelines criados.

### Scripts Individuais

1. **`paper_script.py`** - Script principal do artigo
   - Executa análise completa com visualizações
   - Gera gráficos na pasta `img/`
   - Foco em replicação do artigo científico

2. **`extract_cluster_info.py`** - Extração de informações dos clusters
   - Mostra estatísticas detalhadas dos clusters no console
   - Análise de características distintivas
   - Comparações entre clusters

3. **`generate_cluster_report.py`** - Geração de relatório completo
   - Cria arquivo `.txt` com relatório detalhado
   - Inclui interpretação e insights
   - Análise de critérios de classificação

### Scripts de Pipeline (Pasta additional_scripts/)

4. **`additional_scripts/pipeline_completo.py`** - Pipeline sequencial
   - Executa os 3 scripts individuais em sequência
   - Controle de erros e continuidade
   - Relatório de execução

5. **`additional_scripts/analise_completa_integrada.py`** - Análise integrada
   - Todas as funcionalidades em um único script
   - Melhor performance (reutiliza dados processados)
   - Controle unificado do fluxo

6. **`additional_scripts/alunos_clusters_explicaveis.py`** - Análise específica de clusters de alunos
   - Script adicional para análise detalhada
   - Foco em interpretabilidade dos clusters

## 🚀 Como Executar

### Opção 1: Scripts Individuais (Método Original)

```bash
# Executar cada script separadamente
python paper_script.py
python extract_cluster_info.py
python generate_cluster_report.py
```

**Vantagens:**
- Controle granular de cada etapa
- Possibilidade de executar apenas partes específicas
- Fácil depuração individual

**Desvantagens:**
- Reprocessamento de dados em cada script
- Execução manual de múltiplos comandos
- Maior tempo total de execução

### Opção 2: Pipeline Sequencial (Recomendado para Automação)

```bash
# Executa todos os scripts em sequência
python additional_scripts/pipeline_completo.py

# Ver ajuda
python additional_scripts/pipeline_completo.py --help
```

**Vantagens:**
- Automação completa do processo
- Controle de erros e relatório de execução
- Possibilidade de continuar após falhas
- Mantém a modularidade dos scripts originais

**Desvantagens:**
- Ainda há reprocessamento entre scripts
- Dependência de múltiplos arquivos

### Opção 3: Análise Integrada (Recomendado para Performance)

```bash
# Executa análise completa integrada
python additional_scripts/analise_completa_integrada.py
```

**Vantagens:**
- Melhor performance (sem reprocessamento)
- Controle unificado do fluxo
- Reutilização de objetos e dados
- Arquivo único e autocontido

**Desvantagens:**
- Menos modular
- Arquivo maior e mais complexo

## 📊 Saídas Geradas

Todas as opções geram:

### Visualizações (pasta `img/`)
- `missing_heatmap.jpg` - Mapa de calor de valores ausentes
- `imputation_distribution_assessment.jpg` - Avaliação da imputação
- `dim_red_*.jpg` - Gráficos de redução de dimensionalidade
- `cluster_*.jpg` - Gráficos de clustering
- `classifier_*.jpg` - Gráficos de classificação

### Relatórios
- Arquivo `.txt` com timestamp contendo análise detalhada
- Informações no console sobre clusters e métricas

### Dados Processados
- Objetos de clustering e classificação em memória
- DataFrames com informações de cluster

## ⚙️ Configurações

### Variáveis Utilizadas

**Numéricas (67 variáveis):**
- Demográficas: `AGE`, `PAREDINT`, etc.
- Socioeconômicas: `ESCS`, `WEALTH`, `HOMEPOS`, etc.
- Educacionais: `TEACHSUP`, `DIRINS`, `PERFEED`, etc.
- Tecnológicas: `ICTHOME`, `ICTSCH`, `COMPICT`, etc.

**Categóricas (3 variáveis):**
- `ST004D01T` - Gênero
- `IMMIG` - Status migratório
- `REPEAT` - Repetência

### Algoritmos

- **Redução de dimensionalidade:** SPCA (Sparse Principal Component Analysis)
- **Clustering:** K-Means e Clustering Hierárquico (Ward)
- **Classificação:** XGBoost com otimização de hiperparâmetros
- **Interpretabilidade:** SHAP (Shapley Additive Explanations)

## 🔧 Requisitos

### Dependências
- `pandas`
- `numpy`
- `matplotlib`
- `sklearn`
- `clearn` (pacote personalizado)

### Estrutura de Arquivos
```
replication_materials/
├── data/
│   └── pisa_spain_sample_v2.csv
├── img/                          # Criado automaticamente
├── simulation/                   # Scripts de simulação
├── additional_scripts/           # Scripts adicionais criados posteriormente
│   ├── pipeline_completo.py     # Pipeline sequencial
│   ├── analise_completa_integrada.py # Análise integrada
│   └── alunos_clusters_explicaveis.py # Análise específica de clusters
├── paper_script.py              # Script original do artigo
├── extract_cluster_info.py      # Extração de informações
├── generate_cluster_report.py   # Geração de relatório
└── README_PIPELINE.md           # Este arquivo
```

## 🎯 Recomendações de Uso

### Para Desenvolvimento e Depuração
- Use scripts individuais
- Use scripts de simulação na pasta `simulation/`

### Para Execução de Produção
- Use `additional_scripts/analise_completa_integrada.py` (melhor performance)
- Use `additional_scripts/pipeline_completo.py` (se precisar de modularidade)

### Para Replicação do Artigo
- Use `paper_script.py` seguido dos outros scripts conforme necessário

## 🚨 Notas Importantes

1. **Tempo de Execução:** A análise completa pode levar vários minutos dependendo do hardware

2. **Memória:** Certifique-se de ter RAM suficiente para processar os dados

3. **Reprodutibilidade:** Todos os scripts usam `np.random.seed(42)` para resultados consistentes

4. **Arquivos de Saída:** Os relatórios incluem timestamp para evitar sobrescrita

5. **Tratamento de Erros:** Os pipelines incluem tratamento robusto de erros e logs detalhados

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se todos os arquivos de dados estão presentes
2. Confirme que as dependências estão instaladas
3. Use os scripts de simulação para testes rápidos
4. Consulte os logs de erro para diagnóstico