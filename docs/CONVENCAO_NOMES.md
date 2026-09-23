# Convenção de Nomenclatura de Repositórios

Este documento define o padrão oficial de nomes para todos os repositórios da organização.
As regras aqui descritas são a fonte da verdade usada pela pipeline automática de validação
(`.github/workflows/validar-nome-repositorio.yml`), então qualquer alteração de padrão deve
ser feita neste arquivo **e** em [`.github/naming-rules.yml`](../.github/naming-rules.yml).

## Formato geral

```
<projeto>-<tipo>-<objetivo>[-<nome>]
```

- Somente letras minúsculas, números e hífen (`a-z`, `0-9`, `-`).
- Sem espaços, underscores, acentos ou caracteres especiais.
- Sem hífens duplicados (`--`) nem hífen no início/fim.
- Tamanho entre 5 e 60 caracteres.
- Sem palavras reservadas/proibidas (veja abaixo).

## Projeto (`<projeto>`)

Vem sempre primeiro no nome. Identifica a qual projeto/produto o repositório pertence, por
exemplo: `payments`, `checkout`, `platform`, `auth`.

Quando o repositório **atravessa/integra mais de um projeto** (ex.: pipelines, libs ou
infraestrutura compartilhadas entre vários times/projetos), use `cross` no lugar do nome do
projeto específico. Exemplo: este próprio repositório, `cross-pipeline-repository`.

## Tipos de repositório (`<tipo>`)

| Tipo      | Uso                                              | Exemplo                             |
|-----------|-----------------------------------------------------|--------------------------------------|
| `svc`     | Serviço/API/microsserviço                          | `payments-svc-checkout-api`          |
| `lib`     | Biblioteca ou pacote compartilhado                 | `cross-lib-auth-utils`               |
| `infra`   | Infraestrutura como código, Terraform, IaC          | `platform-infra-network-aws`         |
| `data`    | Pipelines de dados, ETL, data lake                  | `orders-data-etl-sync`               |
| `docs`    | Documentação, portais de conhecimento               | `platform-docs-architecture`         |
| `web`     | Aplicações frontend/web                             | `checkout-web-portal-cliente`        |
| `mobile`  | Aplicações mobile (iOS/Android)                     | `checkout-mobile-app-ios`            |
| `tool`    | Ferramentas internas, CLIs, automações              | `cross-tool-release-cli`             |
| `poc`     | Provas de conceito / experimentos (efêmero)         | `payments-poc-recomendador-ia`       |
| `pipeline`| Governança/automação de pipelines entre projetos    | `cross-pipeline-repository`          |

## Objetivo (`<objetivo>`)

Propósito específico do repositório dentro do tipo escolhido, por exemplo: `checkout`,
`network`, `api`, `portal`, `etl`. Deve ser uma única palavra (sem hífen interno).

## Nome (`<nome>`, opcional)

Complemento descritivo adicional, em kebab-case (pode ter múltiplas palavras separadas por
hífen), usado quando `<objetivo>` sozinho não é suficiente para identificar o repositório.

## Palavras proibidas

`test`, `tmp`, `temp`, `foo`, `bar`, `asdf`, `novo`, `new`, `teste`, `xxx`, `sample`.

## Exemplos válidos

- `cross-pipeline-repository`
- `payments-svc-checkout-api`
- `cross-lib-auth-utils`
- `platform-infra-network-aws`
- `orders-data-etl-sync`
- `checkout-web-portal-cliente`

## Exemplos inválidos e motivo

| Nome                             | Problema                                   |
|-----------------------------------|---------------------------------------------|
| `Payments-Svc-Checkout-Api`       | Letras maiúsculas não são permitidas         |
| `payments_svc_checkout_api`       | Underscore não é permitido                   |
| `svc-checkout-api`                | Falta o `<projeto>` (ou `cross`) no início     |
| `payments-svc--checkout-api`      | Hífen duplicado                              |
| `payments-svc-checkout-api-teste` | Contém palavra proibida (`teste`)            |

## Como o padrão é aplicado

1. Toda mudança/push neste repositório dispara a validação das próprias regras.
2. Repositórios da organização podem chamar o workflow reutilizável
   (`workflow_call`) definido em [`.github/workflows/validar-nome-repositorio.yml`](../.github/workflows/validar-nome-repositorio.yml)
   dentro da própria pipeline de CI para validar seu nome a cada push.
3. Quando um novo repositório é criado na organização (via automação/webhook que dispara
   `repository_dispatch`), o workflow [`.github/workflows/repo-criado.yml`](../.github/workflows/repo-criado.yml)
   valida o nome automaticamente e abre uma *issue* no repositório recém-criado caso o nome
   esteja fora do padrão, sugerindo o formato correto.
4. O mesmo workflow também aplica a proteção da branch `main`, bloqueando commit direto e
   exigindo pull request — veja [`docs/GOVERNANCA_BRANCHES.md`](GOVERNANCA_BRANCHES.md).
5. Repositórios com `<tipo>` igual a `lib` recebem automaticamente o workflow de release em
   `.github/workflows/main.yml`, a partir do template
   [`templates/workflows/lib-release.yml`](../templates/workflows/lib-release.yml).
6. O workflow também garante que o repositório seja **privado** por padrão — veja
   [`docs/GOVERNANCA_BRANCHES.md`](GOVERNANCA_BRANCHES.md).
