# Relatório de Classificação dos Atributos dos Alunos

## Resumo Executivo

Este relatório apresenta uma análise detalhada dos atributos dos alunos presentes nos datasets do projeto, classificando-os como **mutáveis** ou **imutáveis** com base em sua natureza e possibilidade de modificação através de intervenções educacionais.

---

## 1. Dataset: Alunos de Graduação (alunos_graduacao.csv)

### 1.1 Atributos IMUTÁVEIS

Estes atributos são características fixas que não podem ser alteradas por intervenções educacionais:

| Atributo | Descrição | Justificativa |
|----------|-----------|---------------|
| **alunoid** | Identificador único do aluno | Código de identificação permanente |
| **genero** | Gênero do estudante (M/F) | Característica biológica/identitária fixa |
| **raca** | Raça/etnia declarada | Característica étnica imutável |
| **idade** | Idade do estudante | Característica temporal fixa no momento da coleta |
| **anoingresso** | Ano de ingresso na universidade | Data histórica imutável |
| **periodoingresso** | Período de ingresso (1º ou 2º semestre) | Informação histórica fixa |
| **dataconclusao** | Data de conclusão do curso | Data histórica (quando aplicável) |
| **forma_acesso_seletivo** | Forma de acesso (COT, CON, etc.) | Processo seletivo já realizado |
| **campus** | Campus de estudo | Localização física fixa |
| **curso** | Curso de graduação | Escolha acadêmica registrada |
| **modalidade** | Modalidade do curso (Licenciatura/Bacharelado) | Tipo de curso escolhido |

### 1.2 Atributos MUTÁVEIS

Estes atributos podem ser influenciados por políticas educacionais, intervenções sociais ou mudanças comportamentais:

| Atributo | Descrição | Tipo de Intervenção Possível |
|----------|-----------|------------------------------|
| **rendabruta** | Renda bruta familiar | Políticas socioeconômicas, programas de assistência |
| **ira** | Índice de Rendimento Acadêmico | Intervenções pedagógicas, tutoria, suporte acadêmico |
| **ficou_tempo_sem_estudar** | Interrupção nos estudos | Políticas de permanência estudantil |
| **razao_ausencia_educacional** | Motivo da ausência educacional | Programas de apoio específicos |
| **quantidade_computadores** | Número de computadores em casa | Programas de inclusão digital |
| **exclusivo_rede_publica** | Estudou apenas em escola pública | Histórico educacional (parcialmente mutável) |
| **companhia_domiciliar** | Com quem mora | Situação familiar (pode mudar) |
| **mae_nivel_escolaridade** | Escolaridade da mãe | Programas de educação de adultos |
| **pai_nivel_escolaridade** | Escolaridade do pai | Programas de educação de adultos |
| **quantidade_notebooks** | Número de notebooks | Programas de inclusão digital |
| **estado_civil** | Estado civil do estudante | Situação pessoal mutável |
| **qtd_filhos** | Quantidade de filhos | Situação familiar mutável |
| **tipo_area_residencial** | Área de residência (Rural/Urbano) | Mobilidade geográfica |
| **trabalha** | Situação de trabalho | Políticas de emprego e renda |
| **situacao** | Situação acadêmica atual | Intervenções de permanência |
| **pontuacao_seletivo** | Pontuação no processo seletivo | Fixa, mas reflexo de preparação prévia |
| **percentual_frequencia** | Percentual de frequência às aulas | Políticas de engajamento estudantil |
| **reprovacoes** | Número de reprovações | Intervenções pedagógicas |
| **idioma** | Conhecimento de idiomas | Programas de ensino de línguas |

---

## 2. Dataset: PISA Espanha (pisa_spain_sample_v2.csv)

### 2.1 Atributos IMUTÁVEIS

| Atributo | Descrição | Justificativa |
|----------|-----------|---------------|
| **ST004D01T** | Gênero do estudante | Característica identitária fixa |
| **AGE** | Idade do estudante | Característica temporal fixa |
| **IMMIG** | Status migratório | Origem familiar imutável |
| **PAREDINT** | Nível educacional dos pais | Histórico familiar fixo |
| **BMMJ1** | Ocupação da mãe | Situação profissional dos pais |
| **BFMJ2** | Ocupação do pai | Situação profissional dos pais |
| **HISEI** | Índice socioeconômico familiar | Baseado em características familiares |

### 2.2 Atributos MUTÁVEIS

#### 2.2.1 Fatores Socioeconômicos e Familiares
| Atributo | Descrição | Tipo de Intervenção |
|----------|-----------|--------------------|
| **ESCS** | Índice socioeconômico e cultural | Políticas socioeconômicas de longo prazo |
| **WEALTH** | Riqueza familiar | Programas de redistribuição de renda |
| **HOMEPOS** | Posses domésticas | Programas de assistência social |
| **CULTPOSS** | Posses culturais | Programas de acesso à cultura |
| **HEDRES** | Recursos educacionais em casa | Programas de apoio educacional |

#### 2.2.2 Fatores Tecnológicos
| Atributo | Descrição | Tipo de Intervenção |
|----------|-----------|--------------------|
| **ICTHOME** | Acesso a TIC em casa | Programas de inclusão digital |
| **ICTSCH** | Acesso a TIC na escola | Investimento em infraestrutura escolar |
| **COMPICT** | Competência em TIC | Programas de letramento digital |
| **AUTICT** | Autonomia no uso de TIC | Educação tecnológica |
| **SOIAICT** | Uso social de TIC | Programas de cidadania digital |
| **ICTCLASS** | Uso de TIC em sala de aula | Formação de professores |
| **ICTOUTSIDE** | Uso de TIC fora da escola | Acesso comunitário à tecnologia |

#### 2.2.3 Fatores Educacionais e Pedagógicos
| Atributo | Descrição | Tipo de Intervenção |
|----------|-----------|--------------------|
| **TEACHSUP** | Suporte do professor | Formação docente, políticas pedagógicas |
| **DIRINS** | Instrução direta | Metodologias de ensino |
| **PERFEED** | Feedback personalizado | Práticas de avaliação formativa |
| **EMOSUPS** | Suporte emocional | Programas de bem-estar estudantil |
| **STIMREAD** | Estímulo à leitura | Programas de incentivo à leitura |
| **ADAPTIVITY** | Adaptabilidade | Desenvolvimento de competências |
| **TEACHINT** | Interesse do professor | Formação e motivação docente |

#### 2.2.4 Fatores Psicológicos e Comportamentais
| Atributo | Descrição | Tipo de Intervenção |
|----------|-----------|--------------------|
| **JOYREAD** | Prazer em ler | Programas de incentivo à leitura |
| **RESILIENCE** | Resiliência | Programas de desenvolvimento socioemocional |
| **GCSELFEFF** | Autoeficácia | Programas de autoestima e confiança |
| **BELONG** | Sentimento de pertencimento | Políticas de inclusão escolar |
| **PERCOMP** | Competição percebida | Ambiente escolar colaborativo |
| **PERCOOP** | Cooperação percebida | Metodologias colaborativas |
| **MASTGOAL** | Objetivos de maestria | Orientação educacional |
| **WORKMAST** | Maestria no trabalho | Desenvolvimento de competências |
| **BODYIMA** | Imagem corporal | Programas de saúde e bem-estar |
| **SOCONPA** | Consciência social dos pais | Programas de educação parental |

#### 2.2.5 Fatores de Clima Escolar
| Atributo | Descrição | Tipo de Intervenção |
|----------|-----------|--------------------|
| **DISCLIMA** | Clima disciplinar | Políticas de gestão escolar |
| **BEINGBULLIED** | Experiência de bullying | Programas anti-bullying |
| **REPEAT** | Repetência | Políticas de progressão escolar |

#### 2.2.6 Fatores de Orientação e Informação
| Atributo | Descrição | Tipo de Intervenção |
|----------|-----------|--------------------|
| **INFOCAR** | Informação sobre carreiras | Programas de orientação profissional |
| **INFOJOB1** | Informação sobre empregos | Orientação vocacional |
| **INFOJOB2** | Informação adicional sobre empregos | Orientação vocacional |

---

## 3. Análise Comparativa

### 3.1 Distribuição por Mutabilidade

**Dataset Alunos de Graduação:**
- Atributos Imutáveis: 11 (36.7%)
- Atributos Mutáveis: 19 (63.3%)

**Dataset PISA:**
- Atributos Imutáveis: 7 (9.3%)
- Atributos Mutáveis: 68 (90.7%)

### 3.2 Implicações para Políticas Educacionais

#### 3.2.1 Foco em Atributos Mutáveis de Alto Impacto

Os atributos mutáveis identificados oferecem oportunidades concretas para intervenções:

1. **Suporte Pedagógico**: TEACHSUP, DIRINS, PERFEED
2. **Inclusão Digital**: COMPICT, ICTHOME, ICTSCH
3. **Desenvolvimento Socioemocional**: RESILIENCE, BELONG, GCSELFEFF
4. **Ambiente Escolar**: DISCLIMA, prevenção de BEINGBULLIED

#### 3.2.2 Estratégias de Intervenção por Categoria

**Curto Prazo (1-2 anos):**
- Formação docente (TEACHSUP, TEACHINT)
- Programas de tutoria (IRA, percentual_frequencia)
- Acesso à tecnologia (COMPICT, quantidade_computadores)

**Médio Prazo (3-5 anos):**
- Programas de desenvolvimento socioemocional (RESILIENCE, BELONG)
- Melhoria do clima escolar (DISCLIMA)
- Programas de orientação profissional (INFOCAR)

**Longo Prazo (5+ anos):**
- Políticas socioeconômicas (ESCS, WEALTH)
- Educação parental (mae_nivel_escolaridade, pai_nivel_escolaridade)
- Transformação cultural (CULTPOSS)

---

## 4. Recomendações

### 4.1 Para Gestores Educacionais

1. **Priorizar intervenções** nos atributos mutáveis de maior impacto
2. **Desenvolver indicadores** para monitorar mudanças nos atributos mutáveis
3. **Implementar programas integrados** que abordem múltiplos fatores simultaneamente

### 4.2 Para Pesquisadores

1. **Focar estudos longitudinais** nos atributos mutáveis
2. **Investigar relações causais** entre intervenções e mudanças nos atributos
3. **Desenvolver instrumentos** para medir efetividade das intervenções

### 4.3 Para Formuladores de Políticas

1. **Investir em formação docente** (impacto direto em TEACHSUP, DIRINS)
2. **Promover inclusão digital** (COMPICT, ICTHOME)
3. **Desenvolver programas socioemocionales** (RESILIENCE, BELONG)
4. **Implementar políticas de permanência** (situacao, percentual_frequencia)

---

## 5. Conclusões

A análise revela que a maioria dos atributos dos estudantes (especialmente no dataset PISA) são mutáveis, oferecendo amplas oportunidades para intervenções educacionais efetivas. O foco deve estar em:

1. **Fatores pedagógicos**: Qualidade do ensino e suporte docente
2. **Inclusão digital**: Acesso e competência tecnológica
3. **Desenvolvimento socioemocional**: Resiliência e pertencimento
4. **Ambiente escolar**: Clima positivo e inclusivo

Esta classificação fornece uma base sólida para o desenvolvimento de políticas educacionais baseadas em evidências, priorizando intervenções nos fatores que podem ser efetivamente modificados para melhorar os resultados educacionais dos estudantes.

---

**Data de geração**: $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")
**Datasets analisados**: 
- alunos_graduacao.csv (9.900 registros)
- pisa_spain_sample_v2.csv (5.001 registros)
**Total de atributos analisados**: 105 atributos únicos
