import pytest

from fastapi.testclient import TestClient

from be_task_ca.app import app
from be_task_ca.database import SessionLocal
from be_task_ca.item.sa_postgres_model import Item
from be_task_ca.item.sa_postgres_repository import SAPostgresItemRepository
from be_task_ca.item.schema import CreateItemRequest


@pytest.fixture(autouse=True)
def drop_db_items():
    db = SessionLocal()
    db.query(Item).delete()
    db.commit()
    yield
    db.query(Item).delete()
    db.commit()


class TestGetItems:
    """These functional tests should do more complex actions than unit tests, and also touch more
    parts of the system (like a database)
    """
    def test_create_then_get_the_same_item(self):
        # TODO - prepare a TEST database while in test mode, so we don't touch the production DB by accident
        #  env vars should be helpful in be-task-ca/be_task_ca/database.py for this
        #  ...this implementation is clearly bad, and it will erase everything in the database
        with TestClient(app=app) as client:
            req = CreateItemRequest(name='test-3n5', description='desc 93mtnr', price=33, quantity=2)
            client.post('/items', json=req.dict())

            resp = client.get(f"/items")

            assert resp.json()['items'][0]['name'] == 'test-3n5'
            assert resp.json()['items'][0]['description'] == 'desc 93mtnr'
            assert resp.json()['items'][0]['price'] == 33
            assert resp.json()['items'][0]['quantity'] == 2

            assert len(resp.json()) == 1
            assert len(resp.json()['items']) == 1
