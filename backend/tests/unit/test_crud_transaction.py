from unittest.mock import Mock
from app.crud.crud_transaction import get_transaction
from app.models.transaction import Transaction

def test_get_transaction():
    """
    Unit test for the get_transaction CRUD function.
    """
    db = Mock()

    mock_transaction = Transaction(
        id=1,
        description="Test Transaction",
        amount=100.0,
        type="debit",
        category_id=1,
        user_id=1
    )

    db.query.return_value.options.return_value.filter.return_value.first.return_value = mock_transaction

    result = get_transaction(db=db, transaction_id=1)

    db.query.assert_called_once_with(Transaction)
    db.query.return_value.options.assert_called_once()

    assert result == mock_transaction
    assert result.id == 1
    assert result.description == "Test Transaction"
