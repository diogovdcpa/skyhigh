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


def choose_menu_option() -> str:
    print("Selecione uma opcao:")
    print("1) Pegar uma lista (list_APIUsers)")
    print("2) Pegar todos usuarios")
    print("0) Sair")
    return input("> ").strip()


def main() -> int:
    load_dotenv()

    email = required_env("EMAIL")
    password = required_env("PASSWORD")
    tenant_id = required_env("TENANT_ID")
    environment = os.getenv("ENVIRONMENT", "na")
    search_string = os.getenv("USER_SEARCH", "")
    start_index = int(os.getenv("USER_START_INDEX", "0"))
    num_records = int(os.getenv("USER_NUM_RECORDS", "2500"))

    client = WebClient(
        email=email,
        password=password,
        tenantId=tenant_id,
        environment=environment,
    )

    option = choose_menu_option()

    if option == "0":
        print("Encerrado.")
        return 0

    if option == "1":
        try:
            result = client.GetList(id="list_APIUsers")
        except Exception as exc:
            raise RuntimeError(
                "Falha ao buscar list_APIUsers. "
                "Valide se a lista existe no tenant (GetListCollection)."
            ) from exc
    elif option == "2":
        result = client.SearchUsers(
            searchString=search_string,
            startIndex=start_index,
            numRecords=num_records,
            sortColumn="lastLoginDate",
            sortAscending=False,
            userRole=None,
        )
    else:
        print("Opcao invalida. Use 1, 2 ou 0.", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        raise SystemExit(1)
