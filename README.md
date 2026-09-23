# cross-pipeline-repository

Repositório central de governança de nomenclatura para todos os repositórios da organização.

## Conteúdo

- [`docs/CONVENCAO_NOMES.md`](docs/CONVENCAO_NOMES.md) — regras oficiais de nomenclatura de repositórios.
- [`.github/naming-rules.yml`](.github/naming-rules.yml) — regras em formato machine-readable, usadas pela validação automática.
- [`scripts/validar_nome_repositorio.py`](scripts/validar_nome_repositorio.py) — script de validação (CLI).
- [`.github/actions/validate-repo-name`](.github/actions/validate-repo-name/action.yml) — action reutilizável para incluir a validação na pipeline de qualquer repositório.
- [`.github/workflows/validar-nome-repositorio.yml`](.github/workflows/validar-nome-repositorio.yml) — workflow reutilizável (`workflow_call`) e auto-validação deste repositório.
- [`.github/workflows/repo-criado.yml`](.github/workflows/repo-criado.yml) — workflow acionado (via `repository_dispatch`) quando um novo repositório é criado na organização; valida o nome, abre uma issue de não conformidade se necessário, garante visibilidade **privada** e bloqueia commit direto na `main`.
- [`docs/GOVERNANCA_BRANCHES.md`](docs/GOVERNANCA_BRANCHES.md) — regra de que nenhum commit pode ser feito direto na `main` (uso obrigatório de pull request).
- [`.github/workflows/proteger-branch-main.yml`](.github/workflows/proteger-branch-main.yml) — workflow reutilizável para aplicar a proteção da `main` em repositórios já existentes.
- [`templates/workflows/lib-release.yml`](templates/workflows/lib-release.yml) — pipeline de release aplicado automaticamente em repositórios do tipo `lib` (versão a partir do `pyproject.toml`, tag e GitHub Release).
- [`.github/actions/build-repo-name`](.github/actions/build-repo-name/action.yml) — action reutilizável que monta o nome final a partir de `projeto`, `tipo`, `objetivo` e `nome` e já valida o resultado.
- [`.github/workflows/montar-nome-repositorio.yml`](.github/workflows/montar-nome-repositorio.yml) — dispare manualmente (`workflow_dispatch`) informando os parâmetros para obter o nome final validado.

## Como usar em um repositório novo

Adicione ao workflow de CI do repositório:

```yaml
jobs:
  validar-nome:
    uses: jfrancisco-nunes/cross-pipeline-repository/.github/workflows/validar-nome-repositorio.yml@main
```

## Exemplos de uso das pipelines

### Validar o nome do próprio repositório em cada push/PR

```yaml
# .github/workflows/ci.yml de qualquer repositório
name: CI

on:
  push:
  pull_request:

jobs:
  validar-nome:
    uses: jfrancisco-nunes/cross-pipeline-repository/.github/workflows/validar-nome-repositorio.yml@main
    # opcional: valida um nome diferente do repositório atual
    with:
      nome-repositorio: payments-svc-checkout-api
```

### Usar a action diretamente (sem workflow reutilizável)

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: jfrancisco-nunes/cross-pipeline-repository/.github/actions/validate-repo-name@main
```

### Montar o nome final a partir de projeto/tipo/objetivo/nome

Disparo manual (Actions → "Montar nome de repositório" → Run workflow), informando os
campos `projeto`, `tipo`, `objetivo` e `nome`. O resultado aparece no resumo da execução.

Marque `criar-repositorio` como `true` (e informe `dono`, se diferente do padrão) para que o
próprio workflow, após validar o nome, crie o repositório (`gh repo create ... --private`) e
dispare automaticamente a governança de pós-criação
([`repo-criado.yml`](.github/workflows/repo-criado.yml)): proteção da `main` e, se `<tipo>`
for `lib`, o template de release. Requer o secret `ORG_ADMIN_TOKEN`.

Ou use a action dentro de outra pipeline:

```yaml
steps:
  - uses: actions/checkout@v4
  - id: nome
    uses: jfrancisco-nunes/cross-pipeline-repository/.github/actions/build-repo-name@main
    with:
      projeto: payments
      tipo: svc
      objetivo: checkout
      nome: api
  - run: echo "Nome final -> ${{ steps.nome.outputs.nome-repositorio }}"
```

### Aplicar proteção da branch `main` em um repositório já existente

Actions → "Proteger branch main" → Run workflow, informando `repo-owner` e `repo-name`.
Também pode ser chamado por outro workflow:

```yaml
jobs:
  proteger-main:
    uses: jfrancisco-nunes/cross-pipeline-repository/.github/workflows/proteger-branch-main.yml@main
    with:
      repo-owner: jfrancisco-nunes
      repo-name: payments-svc-checkout-api
    secrets: inherit
```

### Disparar a governança de repositório recém-criado

O workflow [`repo-criado.yml`](.github/workflows/repo-criado.yml) escuta `repository_dispatch`.
Uma automação de organização (ex.: GitHub App na criação do repositório) deve chamá-lo assim:

```bash
gh api \
  --method POST \
  /repos/jfrancisco-nunes/cross-pipeline-repository/dispatches \
  -f event_type=repo-criado \
  -f 'client_payload[repo_owner]=jfrancisco-nunes' \
  -f 'client_payload[repo_name]=payments-svc-checkout-api'
```

Isso valida o nome, garante visibilidade privada, bloqueia commit direto na `main` e, se o
`<tipo>` for `lib`, adiciona automaticamente o pipeline de release
([`templates/workflows/lib-release.yml`](templates/workflows/lib-release.yml)).

## Testando localmente

```bash
pip install -r requirements.txt
python scripts/validar_nome_repositorio.py svc-payments-api
pytest
```