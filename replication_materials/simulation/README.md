# Scripts de Simulação para Desenvolvimento Rápido

Este diretório contém scripts de simulação que permitem testar e desenvolver as funcionalidades de clustering sem precisar executar o pipeline completo com dados reais, que pode levar vários minutos.

## Scripts Disponíveis

### 1. `test_cluster_simulation.py`
**Propósito**: Simula todo o pipeline de clustering com dados sintéticos

**Funcionalidades**:
- Gera dados simulados com estrutura de clusters conhecida
- Executa padronização, PCA, clustering e classificação
- Testa formatação de resultados
- Valida acesso a métricas
- **Tempo de execução**: ~5-10 segundos

**Como usar**:
```bash
python test_cluster_simulation.py
```

**Saída esperada**:
- Análise completa de clusters simulados
- Métricas de desempenho
- Validação de formatação
- Confirmação de que todas as funcionalidades estão funcionando

### 2. `test_generate_report_simulation.py`
**Propósito**: Testa especificamente a lógica do `generate_cluster_report.py`

**Funcionalidades**:
- Simula objetos de clustering com dados mock
- Testa formatação de importância de features
- Valida acesso às métricas de classificação
- Testa cenários de erro específicos que causavam problemas
- **Tempo de execução**: ~2-5 segundos

**Como usar**:
```bash
python test_generate_report_simulation.py
```

**Saída esperada**:
- Relatório completo de clusters simulado
- Validação de formatação de dados
- Testes de cenários de erro específicos
- Confirmação de correções implementadas

## Vantagens dos Scripts de Simulação

### ⚡ **Velocidade**
- **Script original**: 5-15 minutos
- **Scripts de simulação**: 2-10 segundos
- **Aceleração**: ~100x mais rápido

### 🔧 **Desenvolvimento**
- Teste rápido de alterações no código
- Validação de correções de bugs
- Experimentação com diferentes parâmetros
- Depuração eficiente

### 🎯 **Foco**
- Testa funcionalidades específicas isoladamente
- Simula cenários de erro conhecidos
- Valida formatação e acesso a dados
- Permite iteração rápida no desenvolvimento

## Fluxo de Desenvolvimento Recomendado

### 1. **Desenvolvimento Inicial**
```bash
# Teste rápido da lógica geral
python test_cluster_simulation.py

# Teste específico do generate_cluster_report
python test_generate_report_simulation.py
```

### 2. **Implementação de Correções**
- Faça alterações no código
- Execute os scripts de simulação para validar
- Itere rapidamente até resolver os problemas

### 3. **Validação Final**
```bash
# Após confirmar que a simulação funciona, teste com dados reais
python generate_cluster_report.py
```

## Problemas Resolvidos pelos Scripts de Simulação

### ❌ **Problemas Identificados e Corrigidos**:

1. **TypeError na formatação de importância**
   - Problema: `Series.__format__` não suporta formatação float
   - Solução: Conversão robusta para valores escalares
   - Teste: `test_generate_report_simulation.py` valida a correção

2. **KeyError no classification_report**
   - Problema: Chave 'accuracy' nem sempre existe
   - Solução: Acesso seguro com `.get()` e valores padrão
   - Teste: Simula cenários sem 'accuracy'

3. **Problemas com arrays NumPy**
   - Problema: Arrays não podem ser formatados diretamente
   - Solução: Extração de valores escalares com `.item()`
   - Teste: Simula diferentes tipos de dados

### ✅ **Funcionalidades Validadas**:
- Formatação de valores de importância
- Acesso às métricas de classificação
- Iteração sobre clusters
- Cálculo de características distintivas
- Geração de relatórios completos

## Estrutura dos Dados Simulados

### `test_cluster_simulation.py`
- **Amostras**: 500 (configurável)
- **Features originais**: 15 (configurável)
- **Componentes PCA**: 8 (configurável)
- **Clusters**: 4 (configurável)
- **Estrutura**: Dados com clusters bem definidos

### `test_generate_report_simulation.py`
- **Amostras**: 300
- **Componentes PCA**: 8
- **Clusters**: 4
- **Foco**: Testa lógica de relatório especificamente

## Personalização

### Modificar Parâmetros de Simulação
```python
# Em test_cluster_simulation.py
df = create_simulated_data(
    n_samples=1000,    # Número de amostras
    n_features=20,     # Número de features
    n_clusters=5       # Número de clusters
)

results = simulate_clustering_pipeline(
    df, 
    n_components=12,   # Componentes PCA
    n_clusters=5       # Clusters para K-means
)
```

### Adicionar Novos Testes
```python
def test_new_functionality():
    """
    Adicione novos testes específicos aqui
    """
    # Seu código de teste
    pass
```

## Quando Usar Cada Script

| Situação | Script Recomendado | Tempo |
|----------|-------------------|-------|
| Desenvolvimento inicial | `test_cluster_simulation.py` | ~10s |
| Correção de bugs específicos | `test_generate_report_simulation.py` | ~5s |
| Teste de novos parâmetros | `test_cluster_simulation.py` | ~10s |
| Validação de formatação | `test_generate_report_simulation.py` | ~5s |
| Teste final | `generate_cluster_report.py` | ~10min |

## Conclusão

Os scripts de simulação permitem:
- **Desenvolvimento 100x mais rápido**
- **Teste isolado de funcionalidades**
- **Validação rápida de correções**
- **Experimentação eficiente**

Use estes scripts durante o desenvolvimento e reserve o script original apenas para validação final com dados reais.