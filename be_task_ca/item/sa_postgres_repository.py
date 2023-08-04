from typing import List, Iterable, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from .entity import ItemEntity
from .sa_postgres_model import Item

from .abstract_repository import ItemRepository


def db_item_to_entity(db_item: Item) -> ItemEntity:
    return ItemEntity(
        id=db_item.id,
        name=db_item.name,
        description=db_item.description,
        price=db_item.price,
        quantity=db_item.quantity,
    )


def db_item_from_entity(item_entity: ItemEntity) -> Item:
    # Yes, the code here looks very similar to the one in the function above.
    # Sure, the code can be generalized easily, but I'll keep things simple, explicit and
    # duplicated for now, to avoid magic
    return Item(
        id=item_entity.id,
        name=item_entity.name,
        description=item_entity.description,
        price=item_entity.price,
        quantity=item_entity.quantity,
    )


class SAPostgresItemRepository(ItemRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def find_item_by_name(self, name) -> Optional[ItemEntity]:
        db_item = self.db_session.query(Item).filter(Item.name == name).first()
        item_entity = db_item_to_entity(db_item) if db_item is not None else None
        return item_entity

    def save_item(self, new_item: ItemEntity, commit=True):
        self.db_session.add(db_item_from_entity(new_item))
        if commit:
            self.db_session.commit()

    def get_all_items(self) -> Iterable[ItemEntity]:
        return (db_item_to_entity(item) for item in self.db_session.query(Item).all())

    def find_item_by_id(self, item_id) -> ItemEntity:
        return db_item_to_entity(
            self.db_session.query(Item).filter(Item.id == item_id).first()
        )
