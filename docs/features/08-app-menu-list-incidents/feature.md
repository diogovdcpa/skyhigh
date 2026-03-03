# Feature: opcao no menu para consultar incidentes

## Objetivo
Adicionar uma nova opcao no menu do `app.py` para buscar e exibir incidentes no terminal.
A feature deve permitir consulta simples de incidentes recentes usando o `WebClient`.

## Contexto
- Problema atual:
  - O menu interativo atual cobre listas e CRUD de usuarios, mas nao possui opcao para consultar incidentes.
- Motivacao:
  - Permitir investigacao inicial de eventos de seguranca sem sair do fluxo de terminal do projeto.

## Escopo
- Inclui:
  - Nova opcao `9` no menu do `app.py` para consultar incidentes.
  - Inclusao de metodo no `WebClient` para buscar incidentes na API.
  - Coleta interativa de filtros basicos (ex.: quantidade maxima e periodo).
  - Exibicao do resultado em JSON formatado, mantendo padrao atual da aplicacao.
  - Tratamento de erros de chamada da API com mensagem clara.
- Nao inclui:
  - Tela grafica ou dashboard.
  - Fluxo de triagem/acao sobre incidente (ack, fechar, atribuir).
  - Exportacao para CSV/PDF.

## Implementação
1. Arquivos a criar/editar:
   - `app.py`
   - `skyhigh_api/webclient.py`
   - `docs/features/08-app-menu-list-incidents/feature.md`
2. Fluxo principal:
   - Exibir `9) Consultar incidentes` no menu.
   - Solicitar filtros minimos (ex.: `limit` e `dias retroativos`, com defaults seguros).
   - Montar parametros e chamar metodo dedicado do `WebClient` para incidentes.
   - Imprimir retorno JSON no stdout.
   - Em caso de erro, exibir mensagem no stderr sem quebrar o loop do menu.
3. Dependências:
   - Sem novas dependencias externas.

## Critérios de aceitação
- [x] O menu do `app.py` apresenta a opcao `9` para consultar incidentes.
- [x] O `WebClient` possui metodo dedicado para busca de incidentes.
- [x] O fluxo aceita filtros basicos e aplica valores padrao quando nao informados.
- [x] A resposta da API e exibida em JSON formatado no terminal.
- [x] Erros da API sao tratados com mensagem clara, sem encerrar o programa abruptamente.

## Como executar/testar
```bash
source venv/bin/activate
python -m py_compile app.py skyhigh_api/webclient.py
python app.py
# selecione opcao 9 e teste com e sem filtros
```

## Riscos e observações
- Risco 1:
  - O endpoint/scopes de incidentes pode variar por tenant/ambiente e exigir ajuste na implementacao.
- Risco 2:
  - Consultas sem filtro podem retornar volume alto e degradar a experiencia no terminal.
- Observacao 1:
  - Definir defaults conservadores (ex.: limite baixo e periodo curto) reduz custo e tempo de resposta.
