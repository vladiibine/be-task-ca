from typing import Iterable

from be_task_ca.item.entity import ItemEntity


class ItemRepository:
    # def __init__(self, db_session):
    #     self.db_session = db_session

    def find_item_by_name(self, name) -> ItemEntity:
        raise NotImplementedError

    def save_item(self, new_item: ItemEntity):
        raise NotImplementedError

    def get_all_items(self) -> Iterable[ItemEntity]:
        raise NotImplementedError

    def find_item_by_id(self, item_id) -> ItemEntity:
        raise NotImplementedError
