# Feature: menu no app.py para lista e usuarios

## Objetivo
Evoluir o `app.py` para exibir um menu simples com duas opcoes de consulta:
1) pegar uma lista; 2) pegar todos os usuarios.

## Contexto
- Problema atual:
  - O `app.py` executava um fluxo unico (busca de usuarios), sem menu para escolher operacoes.
- Motivacao:
  - Permitir que quem roda o script escolha rapidamente entre consultar uma lista especifica ou consultar todos os usuarios.

## Escopo
- Inclui:
  - Implementacao do menu no `app.py`.
  - Implementacao das duas opcoes:
    - Opcao 1: pegar uma lista usando `GetList(id="list_APIUsers")`.
    - Opcao 2: pegar todos os usuarios.
  - Tratamento de entrada invalida e opcao de encerramento.
- Nao inclui:
  - Alteracoes em `skyhigh_api/webclient.py`.
  - Novas dependencias externas.

## Implementação
1. Arquivos a criar/editar:
   - `app.py`
   - `docs/features/03-app-menu-list-and-users/feature.md`
2. Fluxo principal:
   - Exibir menu no terminal com opcoes numeradas.
   - Ler a opcao informada pelo usuario.
   - Encaminhar para fluxo de "pegar uma lista" com id fixo `list_APIUsers`.
   - Encaminhar para fluxo de "pegar todos os usuarios" via `SearchUsers`.
   - Tratar opcao invalida com mensagem clara.
   - Permitir encerramento via opcao `0`.
3. Dependências:
   - Sem novas dependencias; reutiliza `python-dotenv` e `skyhigh_api`.

## Critérios de aceitação
- [x] Feature documentada com titulo, contexto e escopo claros.
- [x] As duas opcoes de menu estao descritas e implementadas no `app.py`.
- [x] A opcao "pegar uma lista" referencia explicitamente `list_APIUsers`.
- [x] O menu trata opcao invalida e possui opcao de saida (`0`).

## Como executar/testar
```bash
source venv/bin/activate
python -m py_compile app.py
python app.py
```

## Riscos e observações
- Risco 1:
  - A lista `list_APIUsers` pode nao existir em alguns tenants.
- Observacao 1:
  - Implementado tratamento de erro orientando validacao via `GetListCollection()` quando `list_APIUsers` nao existir.
