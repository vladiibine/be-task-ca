from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .sa_postgres_repository import SAPostgresItemRepository
from .usecases import create_item, get_all, ItemAlreadyExistsException

from ..common import get_db

from .schema import CreateItemRequest, CreateItemResponse, AllItemsResponse

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest, db: Session = Depends(get_db)
) -> CreateItemResponse:
    db_repo = SAPostgresItemRepository(db)
    try:
        return create_item(item, db_repo)
    
    except ItemAlreadyExistsException:
        raise HTTPException(
            status_code=409, detail="An item with this name already exists"
        )



@item_router.get("/")
async def get_items(db: Session = Depends(get_db)) -> AllItemsResponse:
    db_repo = SAPostgresItemRepository(db)
    return get_all(db_repo)
