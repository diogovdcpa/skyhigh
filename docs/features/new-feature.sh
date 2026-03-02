#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_FILE="$BASE_DIR/feature.template.md"

usage() {
  cat <<'EOF'
Uso:
  ./docs/features/new-feature.sh <nome-curto>

Exemplos:
  ./docs/features/new-feature.sh export-policy
  ./docs/features/new-feature.sh app-users-v2
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -ne 1 ]]; then
  usage
  exit 0
fi

NAME="$1"

if [[ ! "$NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Erro: use apenas minusculas, numeros e hifen (ex: app-users)." >&2
  exit 1
fi

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Erro: template nao encontrado em $TEMPLATE_FILE" >&2
  exit 1
fi

LAST_NUM="$(
  find "$BASE_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' \
    | sed -n 's/^\([0-9][0-9]\)-.*$/\1/p' \
    | sort -n \
    | tail -n 1
)"

if [[ -z "${LAST_NUM:-}" ]]; then
  NEXT_NUM="01"
else
  NEXT_NUM="$(printf '%02d' $((10#$LAST_NUM + 1)))"
fi

FEATURE_DIR="$BASE_DIR/$NEXT_NUM-$NAME"
FEATURE_FILE="$FEATURE_DIR/feature.md"

if [[ -e "$FEATURE_DIR" ]]; then
  echo "Erro: diretorio ja existe: $FEATURE_DIR" >&2
  exit 1
fi

mkdir -p "$FEATURE_DIR"
cp "$TEMPLATE_FILE" "$FEATURE_FILE"

echo "Feature criada: $FEATURE_DIR"
echo "Arquivo: $FEATURE_FILE"
