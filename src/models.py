from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Customer:
    customer_id: int
    name: str
    phone: str
    address: str
    password: str = ""


@dataclass
class MenuItem:
    item_id: int
    name: str
    price: float
    available: bool = True


@dataclass
class Order:
    order_id: int
    customer_id: int
    items: dict
    subtotal: float
    state_tax: float
    local_tax: float
    total: float
    status: str = "Accepted"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))


@dataclass
class Payment:
    payment_id: str
    order_id: int
    method: str
    amount: float
    status: str
    transaction_id: str
    paid_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))