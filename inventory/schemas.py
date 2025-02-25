
from ninja import Schema
from datetime import datetime
from decimal import Decimal

class ProductIn(Schema):
    name: str
    quantity: int
    price: Decimal

class ProductOut(Schema):
    id: int
    name: str
    quantity: int
    price: Decimal
    created_at: datetime
    updated_at: datetime