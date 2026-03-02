# BASE: o que este código faz (first principles)

## 1) Problema fundamental que o projeto resolve
Do ponto de vista mais básico, este projeto tenta resolver:
- "Como um script Python pode autenticar em uma conta Skyhigh/SSE e modificar recursos de política Web de um tenant de forma programática?"

Ou seja, ele transforma chamadas HTTP autenticadas em uma API Python para:
- ler estado de política;
- criar/atualizar/apagar listas;
- criar/apagar locations;
- baixar backup de política;
- consultar regras e configurações auxiliares (SAML, etc.).

## 2) Princípios do design usado aqui
O código segue um modelo de camadas:
- `validation.py`: define contratos de dados (schemas) para validar entradas/formatos.
- `_baseclient.py`: resolve autenticação, sessão HTTP, ambiente (NA/EU/GOV) e headers de autorização.
- `webclient.py`: implementa operações de domínio "Web Policy" em cima da base autenticada.
- `__init__.py`: expõe a API pública do pacote.

Em termos de first principles:
- sem identidade válida, não existe operação de API;
- sem validação de estrutura, payload inválido quebra o fluxo;
- sem controle de revisão/etag, updates de política podem sobrescrever estado incorretamente.

## 3) Como a autenticação funciona (mecânica mínima)
No `_baseClient`:
1. Usuário instancia cliente com `email`, `password`, `tenantId` e `environment`.
2. O cliente valida tipos/formato e monta uma `requests.Session`.
3. `_getAuthHeaders(scopes)`:
   - reutiliza token em cache se não expirou e se scopes pedidos já são subconjunto dos scopes atuais;
   - se necessário, pede novo IAM token (`grant_type=password`);
   - troca IAM token por token de autorização de APIs;
   - retorna headers com `authorization`, `x-access-token`, `x-refresh-token`.

Resultado: toda operação de negócio herda esse mecanismo e não precisa reimplementar login.

## 4) Como o domínio Web é modelado
No `WebClient`, o foco é "policy as data":
- política raiz e nós de ruleset são texto/JSON versionados;
- listas são objetos separados + referência na raiz da policy;
- updates são enviados como "changes" (operações com `op`, `path`, `content`, `hash`).

Fluxo típico de mutação:
1. buscar estado atual (`_getObject`);
2. validar unicidade/referências;
3. montar lista de changes;
4. commitar (`_commit`) com permissões/scopes adequados.

Isso implementa uma forma de "transação lógica" no nível da API.

## 5) O que cada módulo entrega

### `validation.py`
- Centraliza schemas com regex e estruturas para:
  - tenant IDs, IP/CIDR, MIME, certificados;
  - formatos de listas de policy;
  - objeto de location.
- Objetivo: falhar cedo quando entrada não bate o contrato esperado.

### `_baseclient.py`
- Guarda catálogo de scopes (`allScopes`) e fabrics (`na`, `eu`, `gov`).
- Inicializa sessão HTTP com `timeout`, `proxies`, `verify`.
- Gerencia ciclo de token e entrega headers auth reutilizáveis.
- Fornece `GetCurrentTenant()`.

### `webclient.py`
- Herda `_baseClient`.
- Resolve URLs específicas de política Web por ambiente.
- Expõe operações principais:
  - leitura: `GetList`, `GetListCollection`, `GetLocations`, `GetRuleSet`, `GetSAMLConfigs`;
  - escrita: `CreateList`, `UpdateList`, `DeleteList`, `CreateLocation`, `DeleteLocation`;
  - utilitário: `DownloadPolicyBackup`.
- Helpers internos:
  - `_addRef` / `_removeRef`: adiciona/remove referência textual na raiz da policy;
  - `_findRef`: busca referência em rulesets (com recursão opcional);
  - `_getRev`, `_getObject`, `_commit`.

### `__init__.py`
- Exporta `schemas`, `_baseClient`, `allScopes`, `WebClient`.

## 6) Visão sistêmica (entrada -> processamento -> saída)
- Entrada: credenciais + tenant + payloads de domínio (listas, locations, paths de ruleset).
- Processamento:
  - validação de formato;
  - autenticação e autorização por scope;
  - fetch do estado remoto;
  - cálculo de mudanças;
  - commit para API Skyhigh.
- Saída:
  - dicionários Python (objetos remotos);
  - efeitos persistidos no tenant (quando mutações são commitadas);
  - exceções quando validação/autorização/HTTP falham.

## 7) Limitações observáveis no código atual
- Forte dependência de `assert` para validação em runtime (pode ser inadequado em produção).
- Tratamento de erro é heterogêneo (às vezes `assert`, às vezes `Exception`, alguns `except:` amplos).
- Há importações/variáveis pouco usadas e algumas mensagens que podem confundir diagnóstico.
- Não há testes automatizados no repositório para blindar regressões.

## 8) Resumo em uma frase
Este codebase é um SDK Python focado em administrar política Web do Skyhigh SSE via API: autentica, valida payloads e aplica mudanças versionadas (listas, locations e regras) no tenant.
