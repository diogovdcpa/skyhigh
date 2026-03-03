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
    print("6) Criar usuario")
    print("7) Atualizar usuario")
    print("8) Deletar usuario")
    print("0) Sair")
    return input("> ").strip()


def read_required_input(prompt: str) -> str:
    value = input(prompt).strip()
    if not value:
        raise RuntimeError("Campo obrigatorio nao informado.")
    return value


def read_optional_bool(prompt: str):
    raw = input(prompt).strip().lower()
    if not raw:
        return None
    if raw in {"s", "sim", "y", "yes", "true", "1"}:
        return True
    if raw in {"n", "nao", "não", "no", "false", "0"}:
        return False
    raise RuntimeError("Valor invalido para booleano. Use sim/nao.")


def read_optional_int_list(prompt: str):
    raw = input(prompt).strip()
    if not raw:
        return None
    values = []
    for token in raw.split(","):
        item = token.strip()
        if not item:
            continue
        try:
            values.append(int(item))
        except ValueError as exc:
            raise RuntimeError(f"Valor invalido na lista de inteiros: {item}") from exc
    if not values:
        return None
    return values


def read_with_default(prompt: str, default_value):
    shown_default = "" if default_value is None else str(default_value)
    raw = input(f"{prompt} [{shown_default}]: ").strip()
    if not raw:
        return default_value
    return raw


def read_bool_with_default(prompt: str, default_value):
    default_label = ""
    if default_value is True:
        default_label = "sim"
    elif default_value is False:
        default_label = "nao"
    raw = input(f"{prompt} [{default_label}]: ").strip().lower()
    if not raw:
        return default_value
    if raw in {"s", "sim", "y", "yes", "true", "1"}:
        return True
    if raw in {"n", "nao", "não", "no", "false", "0"}:
        return False
    raise RuntimeError("Valor invalido para booleano. Use sim/nao.")


def read_int_list_with_default(prompt: str, default_list):
    default_text = ",".join(str(x) for x in (default_list or []))
    raw = input(f"{prompt} [{default_text}]: ").strip()
    if not raw:
        return list(default_list or [])
    values = []
    for token in raw.split(","):
        item = token.strip()
        if not item:
            continue
        try:
            values.append(int(item))
        except ValueError as exc:
            raise RuntimeError(f"Valor invalido na lista de inteiros: {item}") from exc
    return values


def iter_dicts(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from iter_dicts(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_dicts(value)


def find_users_by_id(search_result, user_id: str):
    matches = []
    for item in iter_dicts(search_result):
        candidate_id = item.get("userId") or item.get("id") or item.get("userid")
        if candidate_id is not None and str(candidate_id) == user_id:
            matches.append(
                {
                    "userId": candidate_id,
                    "email": item.get("email") or item.get("userEmail") or item.get("login"),
                    "name": item.get("name") or item.get("displayName"),
                    "raw": item,
                }
            )
    return matches


def find_users_by_email(search_result, email: str):
    target = email.strip().lower()
    matches = []
    for item in iter_dicts(search_result):
        candidate_email = item.get("email") or item.get("userEmail") or item.get("login")
        if isinstance(candidate_email, str) and candidate_email.strip().lower() == target:
            matches.append(item)
    return matches


def extract_role_catalog(search_result):
    role_by_id = {}
    for item in iter_dicts(search_result):
        roles_info = item.get("rolesInfo")
        if isinstance(roles_info, list):
            for role in roles_info:
                if not isinstance(role, dict):
                    continue
                role_id = role.get("id")
                role_name = role.get("name") or role.get("desc")
                if isinstance(role_id, int):
                    role_by_id[role_id] = str(role_name) if role_name else f"ROLE_{role_id}"
    return role_by_id


def load_role_catalog(client: WebClient):
    try:
        result = client.SearchUsers(
            searchString="",
            startIndex=0,
            numRecords=2500,
            sortColumn="lastLoginDate",
            sortAscending=False,
            userRole=None,
        )
    except Exception:
        return {}
    return extract_role_catalog(result)


def list_users_for_selection(client: WebClient, max_records: int = 200):
    result = client.SearchUsers(
        searchString="",
        startIndex=0,
        numRecords=max_records,
        sortColumn="lastLoginDate",
        sortAscending=False,
        userRole=None,
    )
    users = []
    seen = set()
    for item in iter_dicts(result):
        email = item.get("email") or item.get("userEmail") or item.get("login")
        user_id = item.get("id") or item.get("userId") or item.get("userid")
        first_name = item.get("firstName")
        last_name = item.get("lastName")
        active = item.get("active")
        if email is None and user_id is None:
            continue
        dedupe_key = (str(user_id), str(email).lower() if isinstance(email, str) else "")
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        users.append(
            {
                "id": user_id,
                "email": email,
                "firstName": first_name,
                "lastName": last_name,
                "active": active,
                "raw": item,
            }
        )
    return users


def validate_user_id(client: WebClient, user_id: str):
    try:
        user_obj = client.GetUser(user_id)
        if isinstance(user_obj, dict):
            user_id_value = user_obj.get("id", user_id)
            return {
                "ok": True,
                "matches": [
                    {
                        "userId": user_id_value,
                        "email": user_obj.get("email") or user_obj.get("userEmail"),
                        "name": (
                            f"{user_obj.get('firstName', '')} {user_obj.get('lastName', '')}"
                        ).strip()
                        or user_obj.get("name")
                        or user_obj.get("displayName"),
                        "raw": user_obj,
                    }
                ],
                "source": "get_user",
            }
    except Exception:
        # Fallback para SearchUsers quando GetUser nao estiver disponivel no tenant.
        pass

    try:
        search_result = client.SearchUsers(
            searchString=user_id,
            startIndex=0,
            numRecords=50,
            sortColumn="lastLoginDate",
            sortAscending=False,
            userRole=None,
        )
    except Exception as exc:
        return {"ok": False, "error": str(exc), "matches": [], "source": "search_users"}

    matches = find_users_by_id(search_result, user_id)
    return {"ok": True, "matches": matches, "source": "search_users"}

def load_full_user_payload(client: WebClient, user_obj: dict, fallback_user_id: str = ""):
    if not isinstance(user_obj, dict):
        return None
    email = user_obj.get("email") or user_obj.get("userEmail") or user_obj.get("login")
    if isinstance(email, str) and email.strip():
        try:
            full_by_email = client.GetUser(email.strip())
            if isinstance(full_by_email, dict):
                return full_by_email
        except Exception:
            pass
    user_id = user_obj.get("id") or user_obj.get("userId") or user_obj.get("userid") or fallback_user_id
    if user_id is not None and str(user_id).strip():
        try:
            full_by_id = client.GetUser(str(user_id).strip())
            if isinstance(full_by_id, dict):
                return full_by_id
        except Exception:
            pass
    return None


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
    elif option == "6":
        user_email = read_required_input("Email/login do novo usuario: ")
        first_name = read_required_input("Primeiro nome (obrigatorio): ")
        last_name = read_required_input("Sobrenome (obrigatorio): ")
        role_ids = read_optional_int_list(
            "Roles IDs (csv, ex: 105,104) (opcional, padrao 102): "
        )
        if not role_ids:
            role_ids = [102]

        # Pre-check: evita erro de duplicidade mascarado como 422.
        try:
            email_search = client.SearchUsers(
                searchString=user_email,
                startIndex=0,
                numRecords=50,
                sortColumn="lastLoginDate",
                sortAscending=False,
                userRole=None,
            )
            existing_by_email = find_users_by_email(email_search, user_email)
            if existing_by_email:
                print(
                    "Ja existe usuario com esse email. Use opcao 7 (atualizar) ou informe outro email.",
                    file=sys.stderr,
                )
                return 1
        except Exception:
            pass

        role_catalog = load_role_catalog(client)
        if role_catalog:
            unknown_roles = [role_id for role_id in role_ids if role_id not in role_catalog]
            if unknown_roles:
                known_roles_text = ", ".join(
                    f"{rid}:{name}" for rid, name in sorted(role_catalog.items())
                )
                print(
                    "Role ID nao encontrado no tenant: {}. Roles detectados: {}".format(
                        unknown_roles, known_roles_text
                    ),
                    file=sys.stderr,
                )
                return 1

        active = read_optional_bool("Usuario ativo? [sim/nao] (opcional, padrao sim): ")
        admin = read_optional_bool("Usuario admin? [sim/nao] (opcional, padrao nao): ")
        resend_activation = read_optional_bool(
            "Reenviar link de ativacao? [sim/nao] (opcional, padrao nao): "
        )

        if admin is None:
            admin_role_ids = set()
            for rid, role_name in role_catalog.items():
                upper_name = role_name.upper()
                if "ADMIN" in upper_name:
                    admin_role_ids.add(rid)
            admin = any(rid in admin_role_ids or rid == 105 for rid in role_ids)

        new_user = {
            "email": user_email,
            "id": -1,
        }
        new_user["firstName"] = first_name
        new_user["lastName"] = last_name
        if role_ids is not None:
            new_user["roles"] = role_ids
        if active is not None:
            new_user["active"] = active
        new_user["admin"] = bool(admin)
        if resend_activation is not None:
            new_user["resendActivationLink"] = resend_activation

        api_result = client.CreateUser(new_user)
        result = {
            "message": "Requisicao de criacao enviada.",
            "request_user": new_user,
            "api_result": api_result,
        }
    elif option == "7":
        try:
            users = list_users_for_selection(client, max_records=200)
        except Exception as exc:
            print(
                "Falha ao listar usuarios para selecao. "
                f"Detalhe: {exc}",
                file=sys.stderr,
            )
            return 1

        if not users:
            print("Nenhum usuario encontrado para atualizacao.", file=sys.stderr)
            return 1

        print("Usuarios disponiveis para atualizacao:")
        for index, user in enumerate(users):
            full_name = f"{user.get('firstName') or ''} {user.get('lastName') or ''}".strip()
            print(
                f"{index}) id={user.get('id')!r} "
                f"email={user.get('email')!r} "
                f"name={full_name!r} active={user.get('active')!r}"
            )

        selected = input(
            "Digite o indice do usuario a atualizar (ou ENTER para informar userId manualmente): "
        ).strip()

        selected_user = None
        user_id = None
        current_user_payload = None
        if not selected:
            user_id = read_required_input("Digite o userId a atualizar: ")
            validation = validate_user_id(client, user_id)
            if not validation["ok"]:
                print(
                    "Aviso: nao foi possivel validar o userId automaticamente. "
                    f"Detalhe: {validation['error']}",
                    file=sys.stderr,
                )
            elif not validation["matches"]:
                print(
                    "Aviso: userId nao encontrado por validacao automatica. Revise antes de atualizar.",
                    file=sys.stderr,
                )
            else:
                print("Usuario(s) encontrado(s) para o userId informado:")
                for match in validation["matches"]:
                    print(
                        f"- userId={match['userId']!r} "
                        f"email={match['email']!r} name={match['name']!r}"
                    )
                current_user_payload = validation["matches"][0]["raw"]
                full_payload = load_full_user_payload(
                    client,
                    current_user_payload,
                    fallback_user_id=user_id,
                )
                if isinstance(full_payload, dict):
                    current_user_payload = full_payload
        else:
            try:
                selected_index = int(selected)
            except ValueError:
                print("Indice invalido. Informe um numero inteiro.", file=sys.stderr)
                return 1
            if selected_index < 0 or selected_index >= len(users):
                print(f"Indice invalido. Escolha entre 0 e {len(users) - 1}.", file=sys.stderr)
                return 1
            selected_user = users[selected_index]
            user_id = str(selected_user.get("id") or "").strip()
            if not user_id:
                print("Usuario selecionado sem id valido para atualizacao.", file=sys.stderr)
                return 1
            print("Informacoes do usuario alvo:")
            print(json.dumps(selected_user["raw"], indent=2, ensure_ascii=False))
            current_user_payload = selected_user["raw"]
            full_payload = load_full_user_payload(
                client,
                selected_user["raw"],
                fallback_user_id=user_id,
            )
            if isinstance(full_payload, dict):
                current_user_payload = full_payload

        must_continue = input("Deseja continuar com a atualizacao? [sim/nao]: ").strip().lower()
        if must_continue not in {"s", "sim", "y", "yes"}:
            print("Atualizacao cancelada.")
            return 0

        if not isinstance(current_user_payload, dict):
            print(
                "Nao foi possivel carregar dados atuais do usuario para edicao com defaults.",
                file=sys.stderr,
            )
            return 1

        current_email = current_user_payload.get("email") or current_user_payload.get("userEmail")
        current_first_name = current_user_payload.get("firstName")
        current_last_name = current_user_payload.get("lastName")
        current_roles = current_user_payload.get("roles") if isinstance(current_user_payload.get("roles"), list) else []
        current_active = current_user_payload.get("active")
        current_admin = current_user_payload.get("admin")
        current_read_only = current_user_payload.get("readOnly")
        current_resend = current_user_payload.get("resendActivationLink")

        new_email = read_with_default("Novo email/login", current_email)
        new_first_name = read_with_default("Novo primeiro nome", current_first_name)
        new_last_name = read_with_default("Novo sobrenome", current_last_name)
        new_roles = read_int_list_with_default("Novos roles IDs (csv)", current_roles)
        new_active = read_bool_with_default("Alterar ativo? [sim/nao]", current_active)
        new_admin = read_bool_with_default("Alterar admin? [sim/nao]", current_admin)
        new_read_only = read_bool_with_default("Alterar readOnly? [sim/nao]", current_read_only)
        new_resend = read_bool_with_default("Alterar resendActivationLink? [sim/nao]", current_resend)

        updates = {}
        update_warnings = []
        if new_email != current_email:
            update_warnings.append(
                "Alteracao de email/login ignorada: este tenant aparenta nao permitir update de email pelo endpoint PUT /user."
            )
        if new_first_name != current_first_name:
            updates["firstName"] = new_first_name
        if new_last_name != current_last_name:
            updates["lastName"] = new_last_name
        if new_roles != current_roles:
            updates["roles"] = new_roles
        if new_active != current_active:
            updates["active"] = new_active
        if new_admin != current_admin:
            updates["admin"] = new_admin
        if new_read_only != current_read_only:
            updates["readOnly"] = new_read_only
        if new_resend != current_resend:
            updates["resendActivationLink"] = new_resend

        if not updates:
            if update_warnings:
                print(update_warnings[0], file=sys.stderr)
            print("Nenhuma alteracao detectada/aplicavel. Atualizacao cancelada.")
            return 0

        api_result = client.UpdateUser(user_id, updates, currentUser=current_user_payload)
        verification = {}
        verification_warnings = []
        verify_candidates = []
        if user_id:
            verify_candidates.append(str(user_id))
        if current_email:
            verify_candidates.append(str(current_email))
        if new_email:
            verify_candidates.append(str(new_email))

        seen_candidates = set()
        for candidate in verify_candidates:
            if candidate in seen_candidates:
                continue
            seen_candidates.add(candidate)
            try:
                verify_user = client.GetUser(candidate)
            except Exception:
                continue
            if isinstance(verify_user, dict) and verify_user.get("id") is not None:
                verification = {
                    "verified_by": candidate,
                    "verified_id": verify_user.get("id"),
                    "verified_email": verify_user.get("email") or verify_user.get("userEmail"),
                    "verified_firstName": verify_user.get("firstName"),
                    "verified_lastName": verify_user.get("lastName"),
                }
                break

        if not verification:
            verification = {"warning": "Nao foi possivel verificar pos-update por GetUser."}

        # Alguns tenants nao permitem alterar email/login via PUT /user, mesmo com saved=true.
        if update_warnings:
            verification_warnings.extend(update_warnings)
        if verification_warnings:
            verification["warnings"] = verification_warnings
        result = {
            "message": "Requisicao de atualizacao enviada.",
            "userId": user_id,
            "selected_user_email": selected_user.get("email") if selected_user else None,
            "updates": updates,
            "api_result": api_result,
            "verification": verification,
        }
    elif option == "8":
        try:
            users = list_users_for_selection(client, max_records=200)
        except Exception as exc:
            print(
                "Falha ao listar usuarios para selecao. "
                f"Detalhe: {exc}",
                file=sys.stderr,
            )
            return 1

        if not users:
            print("Nenhum usuario encontrado para exclusao.", file=sys.stderr)
            return 1

        print("Usuarios disponiveis para exclusao:")
        for index, user in enumerate(users):
            full_name = f"{user.get('firstName') or ''} {user.get('lastName') or ''}".strip()
            print(
                f"{index}) id={user.get('id')!r} "
                f"email={user.get('email')!r} "
                f"name={full_name!r} active={user.get('active')!r}"
            )

        selected = input(
            "Digite o indice do usuario a deletar (ou ENTER para informar userId/email manualmente): "
        ).strip()

        selected_user = None
        delete_identifier = None
        if not selected:
            delete_identifier = read_required_input("Informe userId ou email para excluir: ")
        else:
            try:
                selected_index = int(selected)
            except ValueError:
                print("Indice invalido. Informe um numero inteiro.", file=sys.stderr)
                return 1
            if selected_index < 0 or selected_index >= len(users):
                print(f"Indice invalido. Escolha entre 0 e {len(users) - 1}.", file=sys.stderr)
                return 1
            selected_user = users[selected_index]
            print("Informacoes do usuario alvo:")
            print(json.dumps(selected_user["raw"], indent=2, ensure_ascii=False))
            delete_identifier = selected_user.get("email") or str(selected_user.get("id"))
            if not delete_identifier:
                print("Usuario selecionado sem id/email valido para exclusao.", file=sys.stderr)
                return 1

        confirmation_text = input(
            f"Para confirmar, digite exatamente o identificador ({delete_identifier}): "
        ).strip()
        if confirmation_text != delete_identifier:
            print("Confirmacao invalida. Exclusao cancelada.", file=sys.stderr)
            return 1

        final_confirm = input("Confirma deletar este usuario? [sim/nao]: ").strip().lower()
        if final_confirm not in {"s", "sim", "y", "yes"}:
            print("Exclusao cancelada.")
            return 0

        api_result = client.DeleteUser(delete_identifier)
        result = {
            "message": "Requisicao de exclusao enviada.",
            "delete_identifier": delete_identifier,
            "selected_user_id": selected_user.get("id") if selected_user else None,
            "selected_user_email": selected_user.get("email") if selected_user else None,
            "api_result": api_result,
        }
    else:
        print("Opcao invalida. Use 1, 2, 3, 4, 5, 6, 7, 8 ou 0.", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        raise SystemExit(1)
