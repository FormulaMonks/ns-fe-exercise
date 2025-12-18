def test_grid_endpoint_returns_transactions_with_tags(test_client, db_session):
    """
    Test the /api/v1/transactions/grid endpoint returns transactions with tags and category.
    """
    from app.models.tag import Tag
    from app.models.transaction_tag import TransactionTag
    from app.models.transaction import Transaction
    from app.models.category import Category

    # Create category and tags
    category = Category(name="GridCat")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    tag1 = Tag(name="Work")
    tag2 = Tag(name="Travel")
    db_session.add(tag1)
    db_session.add(tag2)
    db_session.commit()
    db_session.refresh(tag1)
    db_session.refresh(tag2)

    # Create transaction and associate tags
    transaction = Transaction(description="GridTest", amount=123.45, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    assoc1 = TransactionTag(transaction_id=transaction.id, tag_id=tag1.id)
    assoc2 = TransactionTag(transaction_id=transaction.id, tag_id=tag2.id)
    db_session.add(assoc1)
    db_session.add(assoc2)
    db_session.commit()

    response = test_client.get("/api/v1/transactions/grid?page=1&size=10&sort_by=amount&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    found = False
    for item in data["items"]:
        if item["description"] == "GridTest":
            found = True
            assert item["category"]["name"] == "GridCat"
            tag_names = [tag["name"] for tag in item["tags"]]
            assert "Work" in tag_names
            assert "Travel" in tag_names
    assert found, "GridTest transaction not found in grid response"

def test_grid_endpoint_pagination_and_sorting(test_client, db_session):
    """
    Test pagination and sorting on /api/v1/transactions/grid endpoint.
    """
    from app.models.tag import Tag
    from app.models.transaction_tag import TransactionTag
    from app.models.transaction import Transaction
    from app.models.category import Category

    category = Category(name="SortCat")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    tag = Tag(name="Recurring")
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)

    # Create multiple transactions
    for i in range(15):
        transaction = Transaction(description=f"SortTest{i}", amount=100+i, type="debit", category_id=category.id, user_id=1)
        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)
        assoc = TransactionTag(transaction_id=transaction.id, tag_id=tag.id)
        db_session.add(assoc)
        db_session.commit()

    # Page 2, size 10, sorted by amount ascending
    response = test_client.get("/api/v1/transactions/grid?page=2&size=10&sort_by=amount&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 5
    amounts = [item["amount"] for item in data["items"]]
    assert amounts == sorted(amounts)
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.models.transaction import Transaction
from app.models.category import Category
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session for a test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Create a test client that uses the test database.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    del app.dependency_overrides[get_db]

def test_health_endpoint(test_client):
    """
    Test that the health endpoint returns 200 OK.
    """
    response = test_client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_read_transactions(test_client, db_session):
    """
    Integration test for the read_transactions API endpoint.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction1 = Transaction(description="Test 1", amount=100, type="debit", category_id=category.id, user_id=1)
    transaction2 = Transaction(description="Test 2", amount=200, type="credit", category_id=category.id, user_id=1)
    db_session.add(transaction1)
    db_session.add(transaction2)
    db_session.commit()
    db_session.refresh(transaction1)
    db_session.refresh(transaction2)

    response = test_client.get("/api/v1/transactions/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Test 1"
    assert data[1]["description"] == "Test 2"
    assert "category_rel" in data[0]
    assert data[0]["category_rel"]["name"] == "Test Category"

def test_read_transactions_without_trailing_slash(test_client, db_session):
    """
    Test that the endpoint works without trailing slash.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction1 = Transaction(description="Test 1", amount=100, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction1)
    db_session.commit()

    response = test_client.get("/api/v1/transactions")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_pagination(test_client, db_session):
    """
    Test pagination with skip and limit parameters.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    for i in range(10):
        transaction = Transaction(description=f"Test {i}", amount=100, type="debit", category_id=category.id, user_id=1)
        db_session.add(transaction)
    db_session.commit()

    response = test_client.get("/api/v1/transactions/?skip=2&limit=5")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

def test_amount_serialized_as_number(test_client, db_session):
    """
    Test that amount is serialized as a number (not string) in JSON.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction = Transaction(description="Test", amount=50.25, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    response = test_client.get("/api/v1/transactions/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert isinstance(data[0]["amount"], (int, float)), "amount must be a number, not a string"
    assert data[0]["amount"] == 50.25

def test_get_single_transaction(test_client, db_session):
    """
    Test getting a single transaction by ID.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction = Transaction(description="Single Test", amount=100.00, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)
    transaction_id = transaction.id

    response = test_client.get(f"/api/v1/transactions/{transaction_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["description"] == "Single Test"
    assert data["amount"] == 100.00
    assert "category_rel" in data

def test_create_transaction(test_client, db_session):
    """
    Test creating a new transaction.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    payload = {
        "description": "New Transaction",
        "amount": 75.50,
        "type": "credit",
        "category_id": category.id,
        "user_id": 1
    }

    response = test_client.post("/api/v1/transactions/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "New Transaction"
    assert data["amount"] == 75.50
    assert isinstance(data["amount"], (int, float))
    assert "category_rel" in data

def test_create_transaction_invalid(test_client, db_session):
    """
    Test creating an invalid transaction returns 422.
    """
    payload = {
        "description": "",
        "amount": 50.0,
        "type": "debit"
    }

    response = test_client.post("/api/v1/transactions/", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_update_transaction(test_client, db_session):
    """
    Test updating an existing transaction.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction = Transaction(description="Original", amount=100.00, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)
    transaction_id = transaction.id

    payload = {
        "description": "Updated",
        "amount": 150.00,
        "type": "credit",
        "category_id": category.id,
        "user_id": 1
    }

    response = test_client.put(f"/api/v1/transactions/{transaction_id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated"
    assert data["amount"] == 150.00
    assert "category_rel" in data

def test_update_nonexistent_transaction(test_client, db_session):
    """
    Test updating a non-existent transaction returns 404 with detail.
    """
    payload = {
        "description": "Won't work",
        "amount": 100.00,
        "type": "debit",
        "category_id": 1,
        "user_id": 1
    }

    response = test_client.put("/api/v1/transactions/99999", json=payload)

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Transaction not found" in data["detail"]

def test_delete_returns_full_object(test_client, db_session):
    """
    Test that DELETE endpoint returns the deleted transaction object.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction = Transaction(description="To Delete", amount=100.00, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)
    transaction_id = transaction.id

    response = test_client.delete(f"/api/v1/transactions/{transaction_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["description"] == "To Delete"
    assert data["amount"] == 100.00
    assert "category_rel" in data
    assert isinstance(data["amount"], (int, float))

def test_not_found_error_format(test_client, db_session):
    """
    Test that 404 errors use consistent format: {"detail": "..."}
    """
    response = test_client.get("/api/v1/transactions/99999")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data, "Error response must have 'detail' key"
    assert "Transaction not found" in data["detail"]

def test_delete_not_found_error_format(test_client, db_session):
    """
    Test that DELETE 404 errors use consistent format.
    """
    response = test_client.delete("/api/v1/transactions/99999")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data, "Error response must have 'detail' key"
    assert "Transaction not found" in data["detail"]

def test_decimal_precision(test_client, db_session):
    """
    Test that decimal amounts maintain precision (e.g., 50.25).
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction = Transaction(description="Precision Test", amount=50.25, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    response = test_client.get(f"/api/v1/transactions/{transaction.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 50.25

def test_category_rel_included(test_client, db_session):
    """
    Test that category_rel is included in all transaction responses.
    """
    category = Category(name="Food")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction = Transaction(description="Test", amount=100, type="debit", category_id=category.id, user_id=1)
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    response = test_client.get(f"/api/v1/transactions/{transaction.id}")

    assert response.status_code == 200
    data = response.json()
    assert "category_rel" in data
    assert data["category_rel"]["name"] == "Food"
    assert "id" in data["category_rel"]

def test_cors_headers(test_client):
    """
    Test that CORS headers are present in OPTIONS requests.
    """
    response = test_client.options(
        "/api/v1/transactions",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )

    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"
