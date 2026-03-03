# Feature: opcao no menu para apagar item da lista

## Objetivo
Adicionar uma nova opcao no menu do `app.py` para remover um item existente da `list_APIUsers`.
Antes da remocao, o fluxo deve listar os itens atuais e aguardar a escolha do item que sera apagado.

## Contexto
- Problema atual:
  - O menu atual possui leitura e inclusao de itens, mas ainda nao oferece acao para remover um item ja cadastrado na lista.
- Motivacao:
  - Permitir manutencao completa da `list_APIUsers` direto no menu interativo, sem edicao manual de payload.

## Escopo
- Inclui:
  - Nova opcao `5` no menu.
  - Consulta da lista atual com `GetList(id="list_APIUsers")`.
  - Exibicao dos itens com indice para facilitar selecao.
  - Leitura interativa da escolha do usuario (indice do item).
  - Remocao do item selecionado em `entries`.
  - Persistencia com `UpdateList(id="list_APIUsers", entries=entries_atualizado)`.
- Nao inclui:
  - Exclusao por lote (mais de um item por vez).
  - Confirmacao dupla da exclusao.
  - Alteracoes no contrato da API.

## Implementação
1. Arquivos a criar/editar:
   - `app.py`
   - `docs/features/06-app-menu-delete-item-from-list/feature.md`
2. Fluxo principal:
   - Exibir no menu a opcao `5) Apagar item da lista (list_APIUsers)`.
   - Executar `GetList(id="list_APIUsers")` para carregar os itens atuais.
   - Listar os itens no terminal com indice, `value` e `comment` (quando existir).
   - Aguardar entrada do usuario com o indice do item a deletar.
   - Validar se o indice informado existe.
   - Remover o item da lista local e enviar `UpdateList` com os `entries` atualizados.
   - Exibir mensagem de sucesso com o item removido.
3. Dependências:
   - Sem novas dependencias.

## Critérios de aceitação
- [ ] O menu apresenta a nova opcao `5` para apagar item da lista.
- [ ] Ao escolher a opcao `5`, o sistema lista os itens atuais antes de pedir a exclusao.
- [ ] O sistema aguarda a selecao do item a ser deletado e valida indice invalido.
- [ ] O item selecionado e removido via `GetList` + `UpdateList`.

## Como executar/testar
```bash
source venv/bin/activate
python -m py_compile app.py
python app.py
# selecione opcao 5, escolha um indice valido e confirme que o item saiu da lista
```

## Riscos e observações
- Risco 1:
  - Escolha por indice pode remover item errado se a pessoa nao revisar a lista exibida.
- Observacao 1:
  - Se a lista estiver vazia, o fluxo deve encerrar com mensagem informativa sem chamar `UpdateList`.
