from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class PickupCase:
    order_id: str
    transaction_reference: str
    customer_name: str
    amount: Decimal
    store_name: str
    store_email: str
