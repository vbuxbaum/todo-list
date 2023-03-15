from app.core import board_service
from unittest.mock import Mock
import pytest


def test_get_user_by_id_not_found():
    mock_repo = Mock()
    mock_repo.get_by_id = Mock(return_value=None)

    fake_id = 5
    fake_owner_id = 3

    with pytest.raises(LookupError, match="Board not found"):
        board_service.get_board_by_id(mock_repo, fake_id, fake_owner_id)
    mock_repo.get_by_id.assert_called_once_with(fake_id)


def test_get_user_by_id_wrong_owner():
    fake_id = 5
    fake_owner_id = 3
    mock_board = Mock(id=fake_id, owner_id=99999)
    mock_repo = Mock(get_by_id=Mock(return_value=mock_board))

    with pytest.raises(LookupError, match="Board not found"):
        board_service.get_board_by_id(mock_repo, fake_id, fake_owner_id)

    mock_repo.get_by_id.assert_called_once_with(fake_id)


def test_get_user_by_id():
    fake_id = 5
    fake_owner_id = 3
    mock_board = Mock(id=fake_id, owner_id=fake_owner_id)
    mock_repo = Mock(get_by_id=Mock(return_value=mock_board))

    result = board_service.get_board_by_id(mock_repo, fake_id, fake_owner_id)
    assert result == mock_board

    mock_repo.get_by_id.assert_called_once_with(fake_id)
