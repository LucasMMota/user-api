import pytest
from unittest.mock import Mock
from app.core.services.user_service import UserService
from app.core.models.user_model import UserModel


# A fake user model to simulate a UserModel with a to_dict() method.
class FakeUserModel:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


@pytest.fixture
def mock_user_repository():
    return Mock()


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(user_repository=mock_user_repository)


def test_list_all_users(user_service, mock_user_repository):
    fake_users = [
        FakeUserModel(1, "Joao", "joao@gmail.com"),
        FakeUserModel(2, "Maria", "maria@gmail.com")
    ]
    mock_user_repository.fetch_all_users.return_value = fake_users

    result = user_service.list_all()
    expected = [user.to_dict() for user in fake_users]
    assert result == expected


def test_get_user_found(user_service, mock_user_repository):
    fake_user = FakeUserModel(3, "Joao A", "ja@gmail.com")
    mock_user_repository.get_user_by_id.return_value = fake_user

    result = user_service.get_user(3)
    assert result == fake_user.to_dict()


def test_get_user_not_found(user_service, mock_user_repository):
    mock_user_repository.get_user_by_id.return_value = None

    result = user_service.get_user(999)
    assert result is None


def test_create_user_valid(user_service, mock_user_repository):
    name = "Davi"
    email = "davi@gmail.com"
    mock_user_repository.get_user_by_email.return_value = None
    fake_user = FakeUserModel(4, name, email)
    mock_user_repository.create_user.return_value = fake_user

    result = user_service.create_user(name, email)
    assert result == fake_user.to_dict()

    created_arg = mock_user_repository.create_user.call_args[0][0]
    assert created_arg.name == name
    assert created_arg.email == email


def test_create_user_invalid_name(user_service, mock_user_repository):
    result = user_service.create_user("D", "d@example.com")
    assert result is None


def test_create_user_invalid_email(user_service, mock_user_repository):
    result = user_service.create_user("Pedro", "invalid-email")
    assert result is None


def test_create_user_duplicate_email(user_service, mock_user_repository):
    fake_existing = FakeUserModel(5, "Lucas", "lucas@yahoo.com")
    mock_user_repository.get_user_by_email.return_value = fake_existing

    result = user_service.create_user("Lucas", "lucas@yahoo.com")
    assert result is None
    user_service.user_repository.get_user_by_email.assert_called_once_with("lucas@yahoo.com")
    user_service.user_repository.assert_not_called()


def test_update_user_valid(user_service, mock_user_repository):
    name = "Douglas"
    email = "dg@gmail.com"
    fake_user = FakeUserModel(6, name, email)
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.update_user.return_value = fake_user

    result = user_service.update_user(6, name, email)
    assert result == fake_user.to_dict()

    updated_arg = mock_user_repository.update_user.call_args[0][0]
    assert updated_arg.id == 6
    assert updated_arg.name == name
    assert updated_arg.email == email


def test_update_user_invalid_input(user_service, mock_user_repository):
    result = user_service.update_user(7, "E", "e@g.com")
    assert result is None


def test_update_user_duplicate_email(user_service, mock_user_repository):
    fake_existing = FakeUserModel(8, "User 1", "a@gmail.com")
    mock_user_repository.get_user_by_email.return_value = fake_existing

    result = user_service.update_user(8, "User 2", "a@gmail.com")
    assert result is None


def test_delete_user_success(user_service, mock_user_repository):
    mock_user_repository.delete_user.return_value = True
    result = user_service.delete_user(9)
    assert result is True


def test_delete_user_not_found(user_service, mock_user_repository):
    mock_user_repository.delete_user.return_value = False
    result = user_service.delete_user(999)
    assert result is False


def test_is_name_valid():
    from app.core.services.user_service import UserService
    assert UserService._is_name_valid("Maria") is True
    assert UserService._is_name_valid("Maria-Julia Santos") is True
    assert UserService._is_name_valid("A") is False
    assert UserService._is_name_valid("123") is False


def test_is_email_valid():
    from app.core.services.user_service import UserService
    assert UserService.is_email_valid("nome@mail.com") is True
    assert UserService.is_email_valid("user_name+tag@sub.domain.com") is True
    assert UserService.is_email_valid("user1@com") is False
    assert UserService.is_email_valid("email-invalido") is False
