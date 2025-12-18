from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def get_transaction(db: Session, transaction_id: int):
    return (
        db.query(Transaction)
        .options(joinedload(Transaction.category_rel))
        .filter(Transaction.id == transaction_id)
        .first()
    )


def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> List[Transaction]:
    return (
        db.query(Transaction)
        .options(joinedload(Transaction.category_rel))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        for key, value in transaction.model_dump().items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int):
    db_transaction = (
        db.query(Transaction)
        .options(joinedload(Transaction.category_rel))
        .filter(Transaction.id == transaction_id)
        .first()
    )
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction
