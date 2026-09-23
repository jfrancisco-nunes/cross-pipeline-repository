# cross-pipeline-repository

Repositório central de governança de nomenclatura para todos os repositórios da organização.

## Conteúdo

- [`docs/CONVENCAO_NOMES.md`](docs/CONVENCAO_NOMES.md) — regras oficiais de nomenclatura de repositórios.
- [`.github/naming-rules.yml`](.github/naming-rules.yml) — regras em formato machine-readable, usadas pela validação automática.
- [`scripts/validar_nome_repositorio.py`](scripts/validar_nome_repositorio.py) — script de validação (CLI).
- [`.github/actions/validate-repo-name`](.github/actions/validate-repo-name/action.yml) — action reutilizável para incluir a validação na pipeline de qualquer repositório.
- [`.github/workflows/validar-nome-repositorio.yml`](.github/workflows/validar-nome-repositorio.yml) — workflow reutilizável (`workflow_call`) e auto-validação deste repositório.
- [`.github/workflows/repo-criado.yml`](.github/workflows/repo-criado.yml) — workflow acionado (via `repository_dispatch`) quando um novo repositório é criado na organização; valida o nome, abre uma issue de não conformidade se necessário e bloqueia commit direto na `main`.
- [`docs/GOVERNANCA_BRANCHES.md`](docs/GOVERNANCA_BRANCHES.md) — regra de que nenhum commit pode ser feito direto na `main` (uso obrigatório de pull request).
- [`.github/workflows/proteger-branch-main.yml`](.github/workflows/proteger-branch-main.yml) — workflow reutilizável para aplicar a proteção da `main` em repositórios já existentes.
- [`templates/workflows/lib-release.yml`](templates/workflows/lib-release.yml) — pipeline de release aplicado automaticamente em repositórios do tipo `lib` (versão a partir do `pyproject.toml`, tag e GitHub Release).

## Como usar em um repositório novo

Adicione ao workflow de CI do repositório:

```yaml
jobs:
  validar-nome:
    uses: SEU_ORG/cross-pipeline-repository/.github/workflows/validar-nome-repositorio.yml@main
```

> Substitua `SEU_ORG` pelo nome real da organização/usuário no GitHub em todos os arquivos
> que fazem referência a este repositório (`action.yml`, exemplos de uso, links de issue).

## Testando localmente

```bash
pip install -r requirements.txt
python scripts/validar_nome_repositorio.py svc-payments-api
pytest
```