# TODO List - Projeto ML e XAI para Previsão de Desempenho Acadêmico no Moodle

## Visão Geral

Este documento contém a lista de tarefas para implementação completa do
projeto de Machine Learning e Explainable AI (XAI) para previsão de
desempenho acadêmico utilizando dados do Moodle.

## Status das Tarefas

- ⏳ **Pendente**: Tarefa não iniciada
- 🔄 **Em Progresso**: Tarefa em desenvolvimento
- ✅ **Concluída**: Tarefa finalizada

---

## 🔴 Prioridade Alta

### 1. ⏳ Definir o Problema e Objetivos

**ID**: `define_problem`

**Descrição**: Estabelecer variável alvo (aprovação/reprovação),
público-alvo (educadores/administradores), critérios de sucesso (métricas
como acurácia, precisão, recall) e considerações éticas.

**Entregáveis**:

- [ ] Documento de definição do problema
- [ ] Especificação da variável alvo
- [ ] Definição de métricas de sucesso
- [ ] Análise de considerações éticas

---

### 2. ⏳ Configurar Acesso ao Banco PostgreSQL do Moodle

**ID**: `setup_database`

**Descrição**: Estabelecer conexão segura, credenciais de leitura, e
compreender o esquema das tabelas principais (mdl_user, mdl_course,
mdl_grade_grades, mdl_logstore_standard_log).

**Entregáveis**:

- [ ] Configuração de conexão segura com PostgreSQL
- [ ] Documentação do esquema das tabelas
- [ ] Script de teste de conectividade
- [ ] Mapeamento das tabelas relevantes

---

### 3. ⏳ Extrair Dados Usando Consultas SQL

**ID**: `extract_data`

**Descrição**: Implementar queries para logs de atividade, notas dos
alunos, participação em fóruns, e dados demográficos, combinando múltiplas
tabelas.

**Entregáveis**:

- [ ] Queries SQL para extração de logs (mdl_logstore_standard_log)
- [ ] Queries SQL para extração de notas (mdl_grade_grades)
- [ ] Queries SQL para dados de fóruns (mdl_forum_posts)
- [ ] Script de extração automatizada
- [ ] Validação da qualidade dos dados extraídos

---

## 🟡 Prioridade Média

### 4. ⏳ Implementar Pipeline de Preparação de Dados

**ID**: `data_preprocessing`

**Descrição**: Limpeza (valores ausentes, outliers), transformação de
variáveis, engenharia de features (métricas de engajamento, comportamento
temporal).

**Entregáveis**:

- [ ] Módulo de limpeza de dados
- [ ] Tratamento de valores ausentes
- [ ] Detecção e tratamento de outliers
- [ ] Engenharia de features comportamentais
- [ ] Pipeline automatizado de pré-processamento

---

### 5. ⏳ Desenvolver e Treinar Modelo de ML

**ID**: `train_model`

**Descrição**: Seleção de algoritmos, divisão treino/teste, otimização de
hiperparâmetros, validação cruzada para classificação aprovação/reprovação.

**Entregáveis**:

- [ ] Comparação de algoritmos de classificação
- [ ] Pipeline de treinamento
- [ ] Otimização de hiperparâmetros
- [ ] Validação cruzada
- [ ] Avaliação de métricas de performance

---

### 6. ⏳ Implementar Técnicas de XAI

**ID**: `implement_xai`

**Descrição**: Integrar SHAP, LIME ou métodos similares para
explicabilidade, gerar explicações locais e globais das predições do modelo.

**Entregáveis**:

- [ ] Integração do SHAP
- [ ] Integração do LIME
- [ ] Geração de explicações locais
- [ ] Geração de explicações globais
- [ ] Visualizações de explicabilidade

---

### 7. ⏳ Implementar Framework FACT

**ID**: `implement_fact`

**Descrição**: Clusterização dos alunos, geração de explicações
contrafactuais (CFEs), mapeamento de fronteiras acionáveis entre clusters.

**Entregáveis**:

- [ ] Pipeline de clusterização
- [ ] Módulo de geração de CFEs
- [ ] Análise de fronteiras acionáveis
- [ ] Classificação de variáveis (acionáveis vs imutáveis)
- [ ] Módulo de análise agregada

---

### 8. ⏳ Validar Hipóteses e Gerar Insights

**ID**: `validate_hypothesis`

**Descrição**: Executar experimento preliminar com 50 alunos, analisar
frequência de características alteradas, criar visualizações para validar H1.

**Entregáveis**:

- [ ] Experimento preliminar (50 alunos)
- [ ] Análise de frequência de características
- [ ] Gráfico de barras de frequência
- [ ] Box plot de magnitude das mudanças
- [ ] Relatório de validação da Hipótese 1

---

## 🟢 Prioridade Baixa

### 9. ⏳ Desenvolver Sistema de Alertas e Interface

**ID**: `develop_interface`

**Descrição**: Criar dashboard para educadores, sistema de notificações
para alunos em risco, integração com Moodle.

**Entregáveis**:

- [ ] Dashboard web para educadores
- [ ] Sistema de alertas automáticos
- [ ] Interface de visualização de explicações
- [ ] Integração com API do Moodle
- [ ] Documentação de uso

---

### 10. ⏳ Automatizar Pipeline e Deploy

**ID**: `automate_deploy`

**Descrição**: Containerização, agendamento de retreinamento,
monitoramento de performance, documentação técnica e guia de uso.

**Entregáveis**:

- [ ] Containerização com Docker
- [ ] Pipeline CI/CD
- [ ] Agendamento de retreinamento
- [ ] Sistema de monitoramento
- [ ] Documentação técnica completa
- [ ] Guia de instalação e uso

---

## 🔵 Processo Atual - Fase de Teste da Metodologia

### 🔄 Teste com Dataset PISA Spain

**ID**: `test_methodology_pisa`

**Descrição**: Atualmente estamos testando e validando a metodologia
completa de ML e XAI utilizando o dataset PISA Spain como prova de conceito
antes da implementação com dados reais do Moodle.

**Dataset em Uso**:

- **Arquivo**: `/replication_materials/data/pisa_spain_sample_v2.csv`
- **Descrição**: Dataset educacional com características similares aos
  dados que serão extraídos do Moodle
- **Objetivo**: Validar pipeline completo de ML/XAI e framework FACT

**Status Atual**: 🔄 **Em Progresso**

**Atividades em Desenvolvimento**:

- [x] Análise exploratória do dataset PISA Spain
- [x] Implementação do pipeline de pré-processamento
- [x] Desenvolvimento de modelos de classificação
- [x] Integração de técnicas XAI (SHAP, LIME)
- [x] Implementação do framework FACT
- [ ] Validação completa da metodologia
- [ ] Documentação dos resultados e lições aprendidas
- [ ] Preparação para transição ao dataset Moodle

**Próximos Passos**:

1. **Finalizar validação da metodologia** com dataset PISA Spain
2. **Documentar pipeline completo** e melhores práticas identificadas
3. **Adaptar metodologia** para estrutura de dados do Moodle
4. **Implementar conexão PostgreSQL** e extração de dados reais

---

### 🎯 Transição para Dataset Moodle Real

**ID**: `transition_to_moodle`

**Descrição**: Após validação completa da metodologia com dataset PISA Spain,
implementaremos a solução com dados reais extraídos do banco PostgreSQL do
Moodle.

**Pré-requisitos**:

- ✅ Metodologia validada com dataset PISA Spain
- ⏳ Acesso configurado ao banco PostgreSQL do Moodle
- ⏳ Mapeamento completo das tabelas relevantes
- ⏳ Queries SQL otimizadas para extração

**Benefícios da Abordagem Atual**:

- **Validação de Conceito**: Teste da metodologia sem dependência de
  infraestrutura
- **Otimização de Pipeline**: Refinamento de algoritmos e parâmetros
- **Identificação de Desafios**: Antecipação de problemas antes da
  implementação real
- **Documentação**: Criação de guias e melhores práticas

---

## Referências

- Guia ML XAI Moodle Completo
- Framework FACT (Framework for Actionable Cluster Transitions)
- Documentação oficial do Moodle
- Bibliotecas: SHAP, LIME, DiCE, Scikit-learn, Pandas

- Dataset PISA Spain: `/replication_materials/data/pisa_spain_sample_v2.csv`

---

**Última atualização**: Janeiro 2025  
**Responsável**: Equipe de Desenvolvimento ML/XAI  
**Status Geral**: 🔄 Em Progresso - Fase de Teste com Dataset PISA Spain
