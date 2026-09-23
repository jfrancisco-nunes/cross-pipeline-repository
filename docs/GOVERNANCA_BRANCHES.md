# Governança de Branches

Regra obrigatória para todos os repositórios da organização: **nenhum commit pode ser feito
diretamente na branch `main`**. Toda mudança deve ser feita em uma branch separada e integrada
via *pull request*.

## Regras aplicadas

- Push direto na `main` é bloqueado (branch protection).
- Pull requests exigem no mínimo 1 aprovação antes do merge.
- A branch precisa estar atualizada com a `main` antes do merge (`required status checks`).
- A verificação de nome de repositório (`validar-nome-repositorio`) é um *status check*
  obrigatório quando configurada no repositório.
- Regra aplicada inclusive para administradores (`enforce_admins`).
- Branches de trabalho devem seguir o padrão `tipo/descricao-curta`, por exemplo:
  `feature/checkout-pix`, `fix/timeout-gateway`, `chore/atualiza-dependencias`.

## Quando é aplicada

A proteção da branch `main` é configurada automaticamente pelo workflow
[`repo-criado.yml`](../.github/workflows/repo-criado.yml) no momento em que o repositório é
criado na organização, usando um token com permissão de administração (`secrets.ORG_ADMIN_TOKEN`).

Repositórios já existentes podem aplicar a mesma configuração manualmente disparando o
workflow reutilizável [`.github/workflows/proteger-branch-main.yml`](../.github/workflows/proteger-branch-main.yml)
via `workflow_dispatch`.
