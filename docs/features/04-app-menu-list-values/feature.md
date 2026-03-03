# Feature: opcao no menu para listar valores do GetList

## Objetivo
Adicionar uma nova opcao no menu do `app.py` para listar apenas os valores (`value`) de todos os itens retornados em `entries` por `GetList(id="list_APIUsers")`.

## Contexto
- Problema atual:
  - O menu permitia consultar a lista completa (`opcao 1`) ou usuarios (`opcao 2`), mas nao havia uma opcao dedicada para exibir somente os valores da lista.
- Motivação:
  - Facilitar a visualizacao direta dos valores da `list_APIUsers` sem precisar interpretar toda a estrutura JSON da lista.

## Escopo
- Inclui:
  - Nova opcao `3` no menu do `app.py`.
  - Chamada de `GetList(id="list_APIUsers")` para obter a lista.
  - Extracao dos valores via `entries[*].value`.
  - Mensagem de validacao de opcao invalida atualizada para incluir `3`.
- Nao inclui:
  - Alteracoes no cliente `skyhigh_api/webclient.py`.
  - Mudancas no contrato da API Skyhigh.

## Implementação
1. Arquivos a criar/editar:
   - `app.py`
   - `docs/features/04-app-menu-list-values/feature.md`
2. Fluxo principal:
   - Exibir no menu a opcao `3) Listar todos os valores da lista (list_APIUsers)`.
   - Ao escolher `3`, executar `GetList(id="list_APIUsers")`.
   - Montar o resultado como lista simples com `entry.get("value")` para cada item de `entries`.
   - Imprimir resultado em JSON formatado.
3. Dependências:
   - Sem novas dependencias.

## Critérios de aceitação
- [x] O menu exibe a nova opcao `3` para listar os valores da lista.
- [x] A opcao `3` consulta `list_APIUsers` via `GetList`.
- [x] A saida da opcao `3` retorna apenas os valores dos itens de `entries`.

## Como executar/testar
```bash
source venv/bin/activate
python -m py_compile app.py
python app.py
```

## Riscos e observações
- Risco 1:
  - Se `list_APIUsers` nao existir no tenant, a opcao `3` falha com orientacao para validar via `GetListCollection()`.
- Observacao 1:
  - A extracao usa `entry.get("value")`, entao entradas sem campo `value` resultam em `null` no JSON de saida.
