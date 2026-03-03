# Skyhigh CLI (PoC)

PoC em Python para operar recursos do Skyhigh via API, com foco em:
- listas de policy (`list_APIUsers`);
- usuarios (criar, atualizar, deletar, listar);
- consulta de incidentes.

O projeto usa um menu interativo em terminal (`app.py`) e um cliente SDK local em `skyhigh_api/`.

## Estrutura principal

- `app.py`: interface CLI com menu agrupado (Lista, Usuario, Incidentes).
- `skyhigh_api/_baseclient.py`: autenticacao e sessao HTTP.
- `skyhigh_api/webclient.py`: operacoes de dominio (listas, usuarios, incidentes/policy).
- `skyhigh_api/validation.py`: validacoes de payload e formatos.
- `PROJECT.md`: arquitetura detalhada e guia tecnico.

## Pre-requisitos

- Python 3.10+ (recomendado)
- acesso de rede aos endpoints Skyhigh do seu ambiente (`na`, `eu` ou `gov`)
- credenciais validas do tenant

Dependencias Python:
- `requests`
- `python-dotenv`
- `schema`

## Configuracao

Crie um arquivo `.env` na raiz do projeto:

```env
EMAIL=seu-email@empresa.com
PASSWORD=sua-senha
TENANT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

# Opcional (padrao: na)
ENVIRONMENT=na

# Opcionais para listagem de usuarios (opcao 9)
USER_SEARCH=
USER_START_INDEX=0
USER_NUM_RECORDS=2500

# Opcional para incidentes (opcao 8)
INCIDENTS_ENDPOINT=
```

Variaveis obrigatorias:
- `EMAIL`
- `PASSWORD`
- `TENANT_ID`

## Como rodar

1. Criar e ativar ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Executar a aplicacao:

```bash
python app.py
```

## Opcoes do menu

- `1`: Validar lista `list_APIUsers`
- `2`: Listar valores da `list_APIUsers`
- `3`: Adicionar item na lista
- `4`: Remover item da lista
- `5`: Criar usuario
- `6`: Deletar usuario
- `7`: Atualizar usuario
- `8`: Listar incidentes
- `9`: Listar usuarios
- `0`: Sair

## Observacoes

- O script falha na inicializacao se faltar alguma variavel obrigatoria no `.env`.
- O `TENANT_ID` deve estar no formato UUID.
- Em operacoes de usuario/lista/incidentes, respostas da API sao exibidas em JSON no terminal.
