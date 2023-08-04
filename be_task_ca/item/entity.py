from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class ItemEntity:
    name: str
    description: str
    price: float
    quantity: int
    id: Optional[UUID] = None  # can be argued that one should let postgres generate UUIDs

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
