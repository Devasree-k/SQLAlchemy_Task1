
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CollectionTotals:
    total_trips: int
    total_collection: Decimal
    total_expense: Decimal
    net_collection: Decimal
