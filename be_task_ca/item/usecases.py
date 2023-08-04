from .abstract_repository import ItemRepository
from .entity import ItemEntity

from .schema import AllItemsResponse, CreateItemRequest, CreateItemResponse


class ItemAlreadyExistsException(Exception):
    pass


def create_item(item: CreateItemRequest, db_repo: ItemRepository) -> CreateItemResponse:
    search_result = db_repo.find_item_by_name(item.name)
    if search_result is not None:
        raise ItemAlreadyExistsException

    new_item = ItemEntity(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    db_repo.save_item(new_item)
    return entity_to_schema(new_item)


def get_all(db_repo: ItemRepository):
    item_iter = db_repo.get_all_items()

    return AllItemsResponse(items=[entity_to_schema(item) for item in item_iter])


def entity_to_schema(item: ItemEntity) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
