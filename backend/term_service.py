from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from html import escape

from .models import PickupCase

def _money(value) -> Decimal:
    try:
        return Decimal(str(value).replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return Decimal("0.00")

def build_case(row: dict) -> PickupCase:
    required = ["order_id", "transaction_reference", "customer_name", "store_name", "store_email"]
    missing = [key for key in required if not str(row.get(key) or "").strip()]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    return PickupCase(
        order_id=str(row["order_id"]).strip(),
        transaction_reference=str(row["transaction_reference"]).strip(),
        customer_name=str(row["customer_name"]).strip(),
        amount=_money(row.get("amount")),
        store_name=str(row["store_name"]).strip(),
        store_email=str(row["store_email"]).strip(),
    )

def render_pickup_term(case: PickupCase) -> str:
    amount = f"R$ {case.amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"""<html><body style="font-family:Arial,sans-serif;line-height:1.55">
      <h1>Termo de retirada</h1>
      <p>Documento gerado para acompanhamento do pedido <strong>{escape(case.order_id)}</strong>.</p>
      <table>
        <tr><td>Cliente</td><td>{escape(case.customer_name)}</td></tr>
        <tr><td>Referência</td><td>{escape(case.transaction_reference)}</td></tr>
        <tr><td>Valor</td><td>{amount}</td></tr>
        <tr><td>Unidade</td><td>{escape(case.store_name)}</td></tr>
        <tr><td>Data</td><td>{date.today().strftime('%d/%m/%Y')}</td></tr>
      </table>
      <p>Esta edição pública usa dados demonstrativos e exige validação operacional antes do envio.</p>
    </body></html>"""
