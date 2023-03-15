from app.core import user_service
from unittest.mock import Mock, patch
import pytest


def test_get_user_by_id_not_found():
    mock_repo = Mock()
    mock_repo.get_by_id = Mock(return_value=None)

    fake_id = 5
    with pytest.raises(LookupError, match="User not found"):
        user_service.get_user_by_id(mock_repo, fake_id)
    mock_repo.get_by_id.assert_called_once_with(fake_id)


def test_get_user_by_id():
    fake_id = 5
    mock_user = Mock(email="teste@teste.com", id=fake_id)

    mock_repo = Mock()
    mock_repo.get_by_id = Mock(return_value=mock_user)

    result = user_service.get_user_by_id(mock_repo, fake_id)

    assert result == mock_user


def test_create_new_user_existing_email():
    mock_user = Mock(email="teste@teste.com")

    mock_repo = Mock()
    mock_repo.get_by_email = Mock(return_value=mock_user)
    mock_repo.create = Mock()

    with pytest.raises(ValueError, match="already exists"):
        user_service.create_new_user(mock_repo, mock_user)

    mock_repo.get_by_email.assert_called_once_with(mock_user.email)
    mock_repo.create.assert_not_called()


def test_create_new_user():
    mock_user = Mock(email="teste@teste.com", password="password")
    mock_user.dict = Mock(return_value=mock_user.__dict__)

    mock_repo = Mock()
    mock_repo.get_by_email = Mock(return_value=None)
    mock_repo.create = Mock()

    with patch("app.core.user_service.encrypt_str", lambda s: s):
        user_service.create_new_user(mock_repo, mock_user)

    mock_repo.get_by_email.assert_called_once_with(mock_user.email)
    assert 'password' not in mock_user.__dict__
    assert 'hashed_password' in mock_user.__dict__
    mock_repo.create.assert_called_with(mock_user.dict())
