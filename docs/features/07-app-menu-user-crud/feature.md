# Feature: menu no app.py para criar, atualizar e deletar usuario

## Objetivo
Adicionar no `app.py` um fluxo de CRUD de usuario com foco em tres operacoes: criacao, atualizacao e exclusao.
A feature deve permitir executar essas acoes via menu interativo usando `WebClient`.

## Contexto
- Problema atual:
  - O menu atual permite apenas consultas e manutencao de itens de lista (`list_APIUsers`), sem operacoes diretas de ciclo de vida de usuario.
- Motivacao:
  - Viabilizar gestao basica de usuarios pelo terminal, reduzindo dependencia de operacoes manuais fora do projeto.

## Escopo
- Inclui:
  - Novas opcoes de menu para:
    - criar usuario
    - atualizar usuario
    - deletar usuario
  - Inclusao de metodos no `WebClient` para operacoes de escrita em usuario (escopo `web.usr.x`).
  - Coleta interativa dos campos minimos para cada operacao.
  - Validacoes basicas de entrada (campos obrigatorios, id de usuario).
  - Exibicao do resultado em JSON, mantendo o padrao do `app.py`.
- Nao inclui:
  - Interface grafica.
  - Atualizacao em lote de usuarios.
  - Workflow de aprovacao/confirmacao multipla para delete.
  - Alteracoes de permissao/role fora do payload das APIs de usuario.

## Implementação
1. Arquivos a criar/editar:
   - `app.py`
   - `skyhigh_api/webclient.py`
   - `docs/features/07-app-menu-user-crud/feature.md`
2. Fluxo principal:
   - Exibir novas opcoes no menu para `create`, `update` e `delete` de usuario.
   - Criacao:
     - Coletar campos obrigatorios (ex.: email/login, nome, role conforme API).
     - Chamar metodo dedicado no `WebClient`.
   - Atualizacao:
     - Solicitar `userId` e campos a alterar.
     - Chamar metodo dedicado no `WebClient` com payload parcial ou completo.
   - Delete:
     - Solicitar `userId`.
     - Executar exclusao e retornar confirmacao.
   - Em todas as operacoes:
     - Tratar erros de API com mensagem clara no stderr.
     - Imprimir resposta JSON formatada no stdout.
3. Dependências:
   - Sem novas dependencias externas.

## Critérios de aceitação
- [x] O menu do `app.py` contem opcoes separadas para criar, atualizar e deletar usuario.
- [x] `WebClient` possui metodos dedicados para create, update e delete de usuario com escopo `web.usr.x`.
- [x] O fluxo de criacao valida campos obrigatorios antes da chamada da API.
- [x] O fluxo de atualizacao exige `userId` e aplica atualizacao somente dos campos informados.
- [x] O fluxo de delete exige `userId` valido e retorna confirmacao de exclusao.
- [x] Entradas invalidas e falhas da API sao tratadas sem quebrar o processo.

## Como executar/testar
```bash
source venv/bin/activate
python -m py_compile app.py skyhigh_api/webclient.py
python app.py
# testar as opcoes de create, update e delete com um usuario de homologacao
```

## Riscos e observações
- Risco 1:
  - Divergencias no payload esperado pelos endpoints de usuario podem causar erro 4xx.
- Risco 2:
  - Exclusao sem confirmacao extra pode remover usuario incorreto se `userId` for informado errado.
- Observacao 1:
  - Recomenda-se validar primeiro o `userId` via busca de usuario antes de update/delete.
