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

    users_list = client.GetList(id="list_APIUsers")
    print(json.dumps(users_list, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        raise SystemExit(1)
