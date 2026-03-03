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
    print("3) Listar todos os valores da lista (list_APIUsers)")
    print("4) Adicionar novo item na lista (list_APIUsers)")
    print("5) Apagar item da lista (list_APIUsers)")
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
    elif option == "3":
        try:
            list_result = client.GetList(id="list_APIUsers")
        except Exception as exc:
            raise RuntimeError(
                "Falha ao buscar list_APIUsers. "
                "Valide se a lista existe no tenant (GetListCollection)."
            ) from exc
        result = [entry.get("value") for entry in list_result.get("entries", [])]
    elif option == "4":
        value = input("Digite o valor do novo item: ").strip()
        if not value:
            print("Valor obrigatorio para adicionar item.", file=sys.stderr)
            return 1
        comment = input("Digite o comentario (opcional): ").strip()
        try:
            list_result = client.GetList(id="list_APIUsers")
        except Exception as exc:
            raise RuntimeError(
                "Falha ao buscar list_APIUsers. "
                "Valide se a lista existe no tenant (GetListCollection)."
            ) from exc
        entries = list_result.get("entries", [])
        if not isinstance(entries, list):
            raise RuntimeError("Formato invalido: 'entries' nao e uma lista.")
        new_entry = {"value": value, "comment": comment}
        entries.append(new_entry)
        client.UpdateList(id="list_APIUsers", entries=entries)
        result = {
            "message": "Item adicionado com sucesso.",
            "entry": new_entry,
            "total_entries": len(entries),
        }
    elif option == "5":
        try:
            list_result = client.GetList(id="list_APIUsers")
        except Exception as exc:
            raise RuntimeError(
                "Falha ao buscar list_APIUsers. "
                "Valide se a lista existe no tenant (GetListCollection)."
            ) from exc

        entries = list_result.get("entries", [])
        if not isinstance(entries, list):
            raise RuntimeError("Formato invalido: 'entries' nao e uma lista.")
        if not entries:
            result = {
                "message": "A lista esta vazia. Nenhum item para remover.",
                "total_entries": 0,
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0

        print("Itens atuais da lista:")
        for index, entry in enumerate(entries):
            value = entry.get("value")
            comment = entry.get("comment", "")
            print(f"{index}) value={value!r} comment={comment!r}")

        selected = input("Digite o indice do item a remover: ").strip()
        try:
            selected_index = int(selected)
        except ValueError:
            print("Indice invalido. Informe um numero inteiro.", file=sys.stderr)
            return 1
        if selected_index < 0 or selected_index >= len(entries):
            print(
                f"Indice invalido. Escolha entre 0 e {len(entries) - 1}.",
                file=sys.stderr,
            )
            return 1

        removed_entry = entries.pop(selected_index)
        updated_list = dict(list_result)
        updated_list["entries"] = entries
        client.UpdateList(updatedList=updated_list)
        result = {
            "message": "Item removido com sucesso.",
            "removed_entry": removed_entry,
            "removed_index": selected_index,
            "total_entries": len(entries),
        }
    else:
        print("Opcao invalida. Use 1, 2, 3, 4, 5 ou 0.", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        raise SystemExit(1)
