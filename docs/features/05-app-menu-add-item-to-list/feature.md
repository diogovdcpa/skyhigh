# Feature: opcao no menu para adicionar item na lista

## Objetivo
Adicionar uma nova opcao no `app.py` para inserir um novo item na `list_APIUsers`, enviando a atualizacao para a API via `UpdateList`.

## Contexto
- Problema atual:
  - O menu permitia apenas consulta de lista/usuarios e listagem de valores, sem acao de escrita para adicionar itens.
- Motivação:
  - Permitir manutencao rapida da lista diretamente pelo script, sem editar payload manualmente.

## Escopo
- Inclui:
  - Nova opcao `4` no menu.
  - Leitura interativa de `value` e `comment`.
  - Busca da lista atual (`GetList`) e adicao do novo item em `entries`.
  - Persistencia da mudanca com `UpdateList`.
- Nao inclui:
  - Remocao/edicao de itens ja existentes.
  - Validacao avancada por tipo de lista alem do fluxo atual.

## Implementação
1. Arquivos a criar/editar:
   - `app.py`
   - `docs/features/05-app-menu-add-item-to-list/feature.md`
2. Fluxo principal:
   - Exibir `4) Adicionar novo item na lista (list_APIUsers)`.
   - Solicitar `value` (obrigatorio) e `comment` (opcional).
   - Buscar `list_APIUsers` com `GetList`.
   - Acrescentar `{"value": value, "comment": comment}` em `entries`.
   - Enviar lista atualizada com `UpdateList(id="list_APIUsers", entries=entries)`.
3. Dependências:
   - Sem novas dependencias.

## Critérios de aceitação
- [x] O menu apresenta a opcao `4`.
- [x] A opcao `4` solicita dados do novo item e exige `value`.
- [x] O fluxo de adicao usa `GetList` + `UpdateList` para persistir o item.

## Como executar/testar
```bash
source venv/bin/activate
python -m py_compile app.py
python app.py
# selecione opcao 4 e informe value/comment
```

## Riscos e observações
- Risco 1:
  - Adicao sem checagem de duplicidade pode inserir valores repetidos.
- Observacao 1:
  - Alguns tipos de lista podem exigir formato de `value` diferente de string; o fluxo atual assume entrada textual.
