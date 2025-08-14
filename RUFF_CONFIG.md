# Configuração do Ruff

Este projeto agora utiliza o [Ruff](https://github.com/astral-sh/ruff) como linter e formatador de código Python.

## O que é o Ruff?

O Ruff é um linter e formatador de código Python extremamente rápido, escrito em Rust. Ele pode substituir várias ferramentas como Flake8, Black, isort, pyupgrade e muitas outras, executando dezenas ou centenas de vezes mais rápido.

## Configuração Implementada

A configuração do Ruff está definida no arquivo `pyproject.toml` na seção `[tool.ruff]` e inclui:

### Configurações Gerais
- **Comprimento de linha**: 88 caracteres (compatível com Black)
- **Indentação**: 4 espaços
- **Versão Python alvo**: 3.9
- **Estilo de aspas**: Aspas duplas
- **Terminação de linha**: Automática

### Regras de Linting
- **Pyflakes (F)**: Detecta erros como imports não utilizados, variáveis indefinidas
- **pycodestyle (E4, E7, E9)**: Subset das regras de estilo de código
- **Correções automáticas**: Habilitadas para todas as regras aplicáveis

### Diretórios Excluídos
O Ruff ignora automaticamente diretórios comuns como:
- `.git`, `.venv`, `__pycache__`
- `build`, `dist`, `node_modules`
- `.ipynb_checkpoints`, `.mypy_cache`
- E muitos outros (ver configuração completa no `pyproject.toml`)

## Como Usar

### Verificar problemas de linting:
```bash
ruff check .
```

### Corrigir problemas automaticamente:
```bash
ruff check --fix .
```

### Formatar código:
```bash
ruff format .
```

### Verificar e formatar em uma única operação:
```bash
ruff check --fix . && ruff format .
```

## Integração com IDEs

Para usar o Ruff no VS Code ou Trae IDE:
1. Instale a extensão do Ruff
2. A configuração será automaticamente detectada do `pyproject.toml`
3. Configure formatação automática ao salvar (opcional)

## Status Atual

Após a implementação:
- ✅ Ruff instalado e configurado
- ✅ 9 problemas corrigidos automaticamente
- ✅ 27 arquivos reformatados
- ⚠️ 139 problemas restantes (principalmente imports em posições incorretas)

Os problemas restantes são principalmente relacionados a:
- Imports de módulos não no topo do arquivo (E402)
- Possíveis variáveis indefinidas de star imports (F405)

Estes podem ser corrigidos manualmente conforme necessário durante o desenvolvimento.