# Feature: menu no app.py para lista e usuarios

## Objetivo
Definir a evolucao do `app.py` para exibir um menu simples com duas opcoes de consulta:
1) pegar uma lista; 2) pegar todos os usuarios.
Nesta etapa, apenas especificar a feature, sem alterar implementacao.

## Contexto
- Problema atual:
  - O `app.py` executa um fluxo unico (busca de usuarios), sem menu para escolher operacoes.
- Motivacao:
  - Permitir que quem roda o script escolha rapidamente entre consultar uma lista especifica ou consultar todos os usuarios.

## Escopo
- Inclui:
  - Definicao funcional do menu no `app.py`.
  - Definicao das duas opcoes iniciais:
    - Opcao 1: pegar uma lista usando `GetList(id="list_APIUsers")`.
    - Opcao 2: pegar todos os usuarios.
  - Definicao de comportamento esperado para entrada invalida e encerramento do menu.
- Nao inclui:
  - Implementacao de codigo no `app.py`.
  - Alteracoes em `skyhigh_api/webclient.py`.
  - Novas dependencias externas.

## Implementação
1. Arquivos a criar/editar:
   - `docs/features/03-app-menu-list-and-users/feature.md`
2. Fluxo principal:
   - Exibir menu no terminal com opcoes numeradas.
   - Ler a opcao informada pelo usuario.
   - Encaminhar para fluxo de "pegar uma lista" com id fixo `list_APIUsers` ou "pegar todos os usuarios".
   - Tratar opcao invalida com mensagem clara.
3. Dependências:
   - Nenhuma nova dependencia nesta fase de especificacao.

## Critérios de aceitação
- [ ] Feature documentada com titulo, contexto e escopo claros.
- [ ] As duas opcoes de menu estao descritas de forma objetiva.
- [ ] A opcao "pegar uma lista" referencia explicitamente `list_APIUsers`.
- [ ] Esta explicitado que nao ha implementacao de codigo nesta etapa.

## Como executar/testar
```bash
# somente validacao documental nesta fase
cat docs/features/03-app-menu-list-and-users/feature.md
```

## Riscos e observações
- Risco 1:
  - A lista `list_APIUsers` pode nao existir em alguns tenants.
- Observacao 1:
  - Se `list_APIUsers` nao existir, na implementacao tratar erro com mensagem orientando validacao via `GetListCollection()`.
