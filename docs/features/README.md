# Padrão de Features

## Estrutura obrigatória
- Pasta base: `docs/features`
- Cada nova feature deve ter pasta própria:
  - `NN-nome-curto-da-feature`
  - Exemplo: `01-app-users`, `02-export-policy`
- Dentro da pasta da feature, criar sempre:
  - `feature.md`

## Nomeação
- `NN`: número sequencial com 2 dígitos (`01`, `02`, `03`...)
- `nome-curto`: minúsculo, com `-`, sem espaços

## Como criar uma nova feature
1. Descobrir o próximo número.
2. Criar a pasta:
   - `mkdir -p docs/features/NN-nome-curto`
3. Copiar o template:
   - `cp docs/features/feature.template.md docs/features/NN-nome-curto/feature.md`
4. Preencher o conteúdo da feature.

## Criação automática (recomendado)
Use o script:

```bash
./docs/features/new-feature.sh nome-curto
```

Exemplo:

```bash
./docs/features/new-feature.sh export-policy
```

Saída esperada:
- cria `docs/features/NN-nome-curto/`
- cria `docs/features/NN-nome-curto/feature.md` com base no template

## Exemplo rápido
```bash
mkdir -p docs/features/02-minha-feature
cp docs/features/feature.template.md docs/features/02-minha-feature/feature.md
```
