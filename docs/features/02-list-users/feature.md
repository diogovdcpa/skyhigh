# Feature: listagem de usuarios via `user/search`

## Objetivo
Adicionar suporte no cliente e no `app.py` para listar usuarios via API CASB `POST /shnapi/rest/v1/user/search`, com autenticacao pelo token existente e payload padrao de paginacao/ordenacao.

## Contexto
- Problema atual: o `app.py` busca `list_APIUsers` como lista de policy, nao a lista real de usuarios CASB.
- Motivacao: usar o endpoint oficial de usuarios para obter dados de usuarios e USER ID para fluxos de leitura/edicao/remocao.

## Escopo
- Inclui:
- Novo metodo `SearchUsers` em `skyhigh_api/webclient.py`.
- Uso desse metodo no `app.py`.
- Configuracao opcional por variaveis de ambiente: `USER_SEARCH`, `USER_START_INDEX`, `USER_NUM_RECORDS`.
- Nao inclui:
- Novos comandos CLI.
- Fluxos de delete/edit/get por USER ID.
- Paginacao automatica de todas as paginas.

## Implementacao
1. Arquivos a criar/editar:
- `skyhigh_api/webclient.py`
- `app.py`
2. Fluxo principal:
- Obter token com `_getAuthHeaders(['web.usr.r'])`.
- Resolver `tenantId` legado retornado na autenticacao.
- Fazer `POST` em `https://www.<dominio>/shnapi/rest/v1/user/search`.
- Enviar payload:
  - `pageCriteria`: `startIndex`, `numRecords`
  - `sortCriteria`: `sortColumn=lastLoginDate`, `sortAscending=false`
  - `searchString`
  - `tenantId`
  - `userRole`
- Retornar JSON da API.
3. Dependencias:
- `requests`
- `python-dotenv`
- `schema`

## Criterios de aceitacao
- [x] `WebClient` possui metodo para chamar `user/search`.
- [x] `app.py` deixa de usar `GetList("list_APIUsers")` e passa a usar `SearchUsers`.
- [x] Resultado exibido em JSON formatado no stdout.
- [x] Parametros principais de busca/paginacao podem ser configurados por `.env`.

## Como executar/testar
```bash
source venv/bin/activate
python app.py
```

## Riscos e observacoes
- A API depende de permissao de escopo/role para `web.usr.r`.
- `tenantId` da API e o `legacyTenantId` retornado no fluxo de autenticacao.
