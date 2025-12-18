from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.schemas.transaction_grid import TransactionGridResponse, TransactionGridItem
from app.schemas.category import Category
from app.schemas.tag import Tag

from app.crud import crud_transaction
from app.db.session import get_db
from app.schemas.transaction import TransactionCreate, TransactionInDB, TransactionUpdate


router = APIRouter()
@router.get("/transactions/grid", response_model=TransactionGridResponse)
def transaction_grid(
    page: int = 1,
    size: int = 10,
    sort_by: str = "date",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
):
    # Validate sort_by and sort_order
    allowed_sort = {"date", "amount", "description", "type"}
    if sort_by not in allowed_sort:
        sort_by = "date"
    if sort_order not in {"asc", "desc"}:
        sort_order = "desc"

    offset = (page - 1) * size

    # Raw SQL for join across transactions, categories, tags
    sql = text(f"""
        SELECT t.id, t.description, t.amount, t.type, t.category_id, t.user_id, t.date,
               c.id as category_id, c.name as category_name,
               tg.id as tag_id, tg.name as tag_name
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        LEFT JOIN transaction_tags tt ON t.id = tt.transaction_id
        LEFT JOIN tags tg ON tt.tag_id = tg.id
        ORDER BY t.{sort_by} {sort_order}
        OFFSET :offset LIMIT :limit
    """)
    result = db.execute(sql, {"offset": offset, "limit": size})
    rows = result.fetchall()

    # Aggregate tags per transaction
    transactions = {}
    for row in rows:
        tid = row.id
        if tid not in transactions:
            transactions[tid] = {
                "id": row.id,
                "description": row.description,
                "amount": row.amount,
                "type": row.type,
                "category": Category(id=row.category_id, name=row.category_name),
                "user_id": row.user_id,
                "date": row.date,
                "tags": []
            }
        if row.tag_id:
            transactions[tid]["tags"].append(Tag(id=row.tag_id, name=row.tag_name))

    # Get total count
    total = db.execute(text("SELECT COUNT(*) FROM transactions")).scalar()

    items = [TransactionGridItem(**tx) for tx in transactions.values()]
    return TransactionGridResponse(items=items, total=total)


@router.post("/transactions/", response_model=TransactionInDB)
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return crud_transaction.create_transaction(db=db, transaction=transaction, user_id=1)


@router.get("/transactions/", response_model=List[TransactionInDB])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud_transaction.get_transactions(db, skip=skip, limit=limit)
    return transactions


@router.get("/transactions/{transaction_id}", response_model=TransactionInDB)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/transactions/{transaction_id}", response_model=TransactionInDB)
def update_existing_transaction(
    transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)
):
    db_transaction = crud_transaction.update_transaction(db, transaction_id, transaction)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


@router.delete("/transactions/{transaction_id}", response_model=TransactionInDB)
def delete_existing_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud_transaction.delete_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction
