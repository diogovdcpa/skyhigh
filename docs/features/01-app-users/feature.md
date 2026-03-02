# Feature: app.py para consultar `list_APIUsers`

## Objetivo
Criar um `app.py` na raiz do projeto como ponto principal de execução para buscar a lista `list_APIUsers` usando `WebClient`, lendo credenciais do arquivo `.env` e executando sempre dentro de ambiente virtual.

## Pré-requisitos
1. Sempre ativar o ambiente virtual antes de rodar qualquer comando.
2. Garantir dependências:
   - `requests`
   - `python-dotenv`
   - `schema`

## `.env` esperado
Arquivo `.env` na raiz com:
- `EMAIL`
- `PASSWORD`
- `TENANT_ID`
- `ENVIRONMENT` (opcional; usar `na` por padrão)

## `app.py` (na raiz)
```python
import json
import os
import sys

from dotenv import load_dotenv

from skyhigh_api import WebClient


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variavel obrigatoria ausente: {name}")
    return value


def main() -> int:
    load_dotenv()

    email = required_env("EMAIL")
    password = required_env("PASSWORD")
    tenant_id = required_env("TENANT_ID")
    environment = os.getenv("ENVIRONMENT", "na")

    client = WebClient(
        email=email,
        password=password,
        tenantId=tenant_id,
        environment=environment,
    )

    # Busca a lista pelo id esperado no tenant.
    lista = client.GetList(id="list_APIUsers")
    print(json.dumps(lista, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        raise SystemExit(1)
```

## Execução (sempre com venv ativo)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install requests python-dotenv schema
python app.py
```

## Observações
- Não hardcode credenciais no código.
- Se o id `list_APIUsers` não existir, validar no catálogo com `client.GetListCollection()` e ajustar para o id/nome correto.
