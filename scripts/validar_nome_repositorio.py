#!/usr/bin/env python3
"""Valida o nome de um repositório contra as regras em .github/naming-rules.yml."""
import argparse
import os
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = REPO_ROOT / ".github" / "naming-rules.yml"


def carregar_regras(path: Path = RULES_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validar_nome(nome: str, regras: dict) -> list[str]:
    erros = []

    if not (regras["min_length"] <= len(nome) <= regras["max_length"]):
        erros.append(
            f"tamanho inválido ({len(nome)} caracteres); "
            f"esperado entre {regras['min_length']} e {regras['max_length']}"
        )

    if nome != nome.lower():
        erros.append("o nome deve conter apenas letras minúsculas")

    if "--" in nome:
        erros.append("hífens duplicados não são permitidos")

    if nome.startswith("-") or nome.endswith("-"):
        erros.append("o nome não pode começar nem terminar com hífen")

    for palavra in regras["palavras_proibidas"]:
        if re.search(rf"(^|-){re.escape(palavra)}(-|$)", nome.lower()):
            erros.append(f"contém palavra proibida: '{palavra}'")

    if not re.match(regras["pattern"], nome):
        tipos = ", ".join(regras["tipos_validos"])
        erros.append(
            "não segue o formato <projeto>-<tipo>-<objetivo>[-<nome>] "
            f"(tipos válidos: {tipos}; use 'cross' como <projeto> quando o "
            "repositório integrar mais de um projeto)"
        )

    return erros


def extrair_tipo(nome: str, regras: dict) -> str | None:
    """Retorna o <tipo> do nome do repositório, ou None se o nome não casar com o padrão."""
    match = re.match(regras["pattern"], nome)
    return match.group("tipo") if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("nome_repositorio", help="Nome do repositório a validar")
    parser.add_argument(
        "--github-output",
        action="store_true",
        help="Escreve 'valido' e 'tipo' no arquivo apontado por $GITHUB_OUTPUT",
    )
    args = parser.parse_args()

    regras = carregar_regras()
    erros = validar_nome(args.nome_repositorio, regras)
    valido = not erros

    if args.github_output:
        github_output = Path(os.environ["GITHUB_OUTPUT"])
        tipo = extrair_tipo(args.nome_repositorio, regras) or ""
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"valido={'true' if valido else 'false'}\n")
            f.write(f"tipo={tipo}\n")

    if erros:
        print(f"❌ Nome de repositório inválido: '{args.nome_repositorio}'")
        for erro in erros:
            print(f"  - {erro}")
        return 1

    print(f"✅ Nome de repositório válido: '{args.nome_repositorio}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
