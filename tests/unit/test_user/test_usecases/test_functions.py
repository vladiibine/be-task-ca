from unittest import mock

import pytest
from fastapi import HTTPException

from be_task_ca.item.abstract_repository import ItemRepository
from be_task_ca.user.sa_postgres_model import CartItem
from be_task_ca.user.usecases import add_item_to_cart


class TestAddItemToCart:
    """Unit tests should test smaller pieces of code. My definition for that is a single function
    All other functions called by that function should be mocked. In theory this is nice, in
    practice, we don't mock everything everytime, but decide on what's more important. Calls to
    external "systems" are important; builtin functions/methods might not be important;
    """
    @mock.patch('be_task_ca.user.usecases.find_user_by_id', autospec=True)
    @mock.patch('be_task_ca.user.usecases.CartItem', autospec=True)
    @mock.patch('be_task_ca.user.usecases.save_user', autospec=True)
    @mock.patch('be_task_ca.user.usecases.list_items_in_cart', autospec=True)
    def test_returns_expected_cart_items(
        self, mock_list_items_in_cart, mock_save_user, mock_cart_item_cls, mock_find_user_by_id
    ):
        # Some people use mocks, other people use dependency injection
        # I don't have a strong opinion, but I'm very comfortable with mocks
        # In this situation, dependency injection would work as well
        mock_cart_item = mock.MagicMock(
            name='cart-item', spec=CartItem, **{'quantity': 6, 'item_id': 'item-id-3'})
        mock_db_session = mock.MagicMock(name='db-session')
        mock_item_repo = mock.MagicMock(name='item-repo', spec=ItemRepository, **{
            'find_item_by_id.return_value.quantity': 10,

        })

        result = add_item_to_cart(3, mock_cart_item, mock_db_session, mock_item_repo)

        assert result is mock_list_items_in_cart.return_value
        mock_find_user_by_id.assert_called_once_with(3, mock_db_session)
        mock_save_user.assert_called_once_with(mock_find_user_by_id.return_value, mock_db_session)
        user = mock_find_user_by_id.return_value
        mock_cart_item_cls.assert_called_once_with(
            user_id=user.id, item_id=mock_cart_item.item_id, quantity=mock_cart_item.quantity
        )
        mock_list_items_in_cart.assert_called_once_with(user.id, mock_db_session)

    @mock.patch('be_task_ca.user.usecases.find_user_by_id', autospec=True)
    def test_raises_404_if_user_doesnt_exist(self, mock_find_user_by_id):
        mock_find_user_by_id.return_value = None

        mock_cart_item = mock.MagicMock(
            name='cart-item', spec=CartItem, **{'quantity': 6, 'item_id': 'item-id-3'})
        mock_db_session = mock.MagicMock(name='db-session')
        mock_item_repo = mock.MagicMock(name='item-repo', spec=ItemRepository, **{
            'find_item_by_id.return_value.quantity': 10,
        })

        with pytest.raises(HTTPException) as err:
            add_item_to_cart(44, mock_cart_item, mock_db_session, mock_item_repo)
            assert err.status_code == 404
            assert err.detail == "User does not exist"

        mock_find_user_by_id.assert_called_once_with(44, mock_db_session)

    @mock.patch('be_task_ca.user.usecases.find_user_by_id', autospec=True)
    def test_raises_409_if_not_enough_items(self, mock_find_user_by_id):
        mock_cart_item = mock.MagicMock(
            name='cart-item', spec=CartItem, **{'quantity': 60, 'item_id': 'item-id-3'})
        mock_db_session = mock.MagicMock(name='db-session')
        mock_item_repo = mock.MagicMock(name='item-repo', spec=ItemRepository, **{
            'find_item_by_id.return_value.quantity': 10,
        })

        with pytest.raises(HTTPException) as err:
            add_item_to_cart(44, mock_cart_item, mock_db_session, mock_item_repo)
            assert err.status_code == 409
            assert err.detail == "Not enough items in stock"

        mock_find_user_by_id.assert_called_once_with(44, mock_db_session)
