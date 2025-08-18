# Comparativo: paper_script.py vs paper_script_dice.py

## Resumo Executivo

Este relatório compara a execução do script original (`paper_script.py`) com a nova versão que integra DICE (`paper_script_dice.py`) para análise de explicabilidade de clusters.

## Resultados da Execução

### ✅ Script Original (paper_script.py)
- **Status**: Executado com sucesso
- **Tempo de execução**: ~2 minutos
- **Saída**: Diretório `img/` com 15 visualizações
- **Funcionalidades**: Pipeline completo de ML (preprocessamento, redução dimensional, clustering, classificação)

### ⚠️ Script DICE (paper_script_dice.py)
- **Status**: Executado com problemas na seção DICE
- **Tempo de execução**: ~2 minutos
- **Saída**: Diretório `img_dice/` com 15 visualizações + diretório `dice_results/`
- **Funcionalidades**: Pipeline completo + tentativa de análise DICE

## Análise Detalhada

### Funcionalidades Comuns (Funcionando Identicamente)

Ambos os scripts executaram com sucesso as seguintes etapas:

1. **Preprocessamento de Dados**
   - Tratamento de valores ausentes
   - Imputação de dados
   - Remoção de outliers

2. **Redução de Dimensionalidade**
   - Análise de componentes principais
   - Explicação de componentes
   - Visualização da variância explicada

3. **Clustering**
   - KMeans e Agglomerative Clustering
   - Análise do número ótimo de clusters
   - Visualizações 2D dos clusters
   - Comparação de distribuições

4. **Classificação**
   - Treinamento com XGBoost
   - Análise SHAP de importância das features
   - Matriz de confusão
   - Curvas ROC
   - Acurácia: **83.1%** (idêntica em ambos)

### Diferenças Principais

#### Estrutura de Diretórios
- **Original**: Salva em `img/`
- **DICE**: Salva em `img_dice/` + `dice_results/`

#### Nova Funcionalidade DICE

O script DICE adiciona uma seção de análise de contrafactuais:

**✅ Aspectos que Funcionaram:**
- Preparação dos dados para DICE (4.256 amostras, 77 features)
- Treinamento do modelo Random Forest para DICE
- Configuração da interface DICE
- Identificação de 3 clusters para análise

**❌ Problemas Encontrados:**
- **Erro Principal**: "The target class for [X] could not be identified"
- **Impacto**: Nenhum contrafactual foi gerado com sucesso
- **Tentativas**: 6 transições entre clusters (0→1, 0→2, 1→0, 1→2, 2→0, 2→1)
- **Resultado**: 0 análises de contrafactuais realizadas

## Resultados Quantitativos

### Métricas de Performance (Idênticas)
| Métrica | Valor |
|---------|-------|
| Acurácia | 83.1% |
| Precision (macro avg) | 84.4% |
| Recall (macro avg) | 82.0% |
| F1-score (macro avg) | 82.8% |

### Features Mais Importantes (Idênticas)
1. **ESCS**: 0.853 (Status socioeconômico)
2. **HOMEPOS**: 0.275 (Recursos domésticos)
3. **TEACHSUP**: 0.170 (Apoio do professor)
4. **JOYREAD**: 0.169 (Prazer na leitura)
5. **BFMJ2**: 0.166 (Ocupação do pai)

### Clusters Identificados
- **Cluster 0**: 179 amostras
- **Cluster 1**: 139 amostras  
- **Cluster 2**: 114 amostras
- **Clusters 3-5**: 133, 173, 114 amostras respectivamente

## Análise dos Problemas DICE

### Possíveis Causas do Erro
1. **Incompatibilidade de versão**: DiCE pode ter problemas com a versão atual do scikit-learn
2. **Configuração de dados**: O formato dos dados pode não estar adequado para DICE
3. **Modelo de classificação**: O Random Forest pode não estar sendo interpretado corretamente pelo DICE
4. **Mapeamento de classes**: Problema na identificação das classes de destino

### Evidências do Problema
- Mensagem de erro consistente: "target class could not be identified"
- Erro ocorre em todas as tentativas de transição entre clusters
- O modelo Random Forest funciona corretamente (acurácia de 83.1%)
- Os dados estão bem formatados (4.256 amostras válidas)

## Recomendações

### Correções Imediatas
1. **Verificar versão do DiCE**: Atualizar para versão mais recente
2. **Simplificar dados**: Testar com menos features inicialmente
3. **Modelo alternativo**: Testar com outros algoritmos (Logistic Regression)
4. **Debugging**: Adicionar logs detalhados na seção DICE

### Melhorias Futuras
1. **Tratamento de erros**: Implementar fallbacks quando DICE falha
2. **Validação de dados**: Verificar compatibilidade antes da análise DICE
3. **Documentação**: Adicionar guia de troubleshooting para DICE
4. **Testes unitários**: Criar testes específicos para a funcionalidade DICE

## Conclusão

O script `paper_script_dice.py` mantém **100% da funcionalidade** do script original, gerando resultados idênticos para todo o pipeline de machine learning. A adição da funcionalidade DICE representa uma **extensão valiosa** para explicabilidade, mas atualmente enfrenta problemas técnicos que impedem a geração de contrafactuais.

**Status Geral**: ✅ **Funcional** (pipeline principal) + ⚠️ **Necessita correção** (seção DICE)

**Impacto**: O script pode ser usado normalmente para análise de clusters, com a funcionalidade DICE como um bônus futuro quando os problemas forem resolvidos.

---
*Relatório gerado em: 17/08/2025 23:15*
*Versão do Python: 3.10.10*
*Ambiente: Windows com venv ativo*