import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validar_nome_repositorio import carregar_regras, validar_nome  # noqa: E402


def test_nomes_validos():
    regras = carregar_regras()
    for nome in [
        "cross-pipeline-repository",
        "payments-svc-checkout-api",
        "cross-lib-auth-utils",
        "platform-infra-network-aws",
        "orders-data-etl-sync",
        "checkout-web-portal-cliente",
    ]:
        assert validar_nome(nome, regras) == [], nome


def test_nomes_invalidos():
    regras = carregar_regras()
    for nome in [
        "Payments-Svc-Checkout-Api",
        "payments_svc_checkout_api",
        "svc-checkout-api",
        "payments-svc--checkout-api",
        "payments-svc-checkout-api-teste",
    ]:
        assert validar_nome(nome, regras) != [], nome
