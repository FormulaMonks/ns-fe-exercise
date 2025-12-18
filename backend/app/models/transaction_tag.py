from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class TransactionTag(Base):
    __tablename__ = "transaction_tags"

    transaction_id = Column(Integer, ForeignKey("transactions.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    transaction = relationship("Transaction", back_populates="tags_assoc")
    tag = relationship("Tag", back_populates="transactions")
