from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_serializer

from .category import Category


class TransactionBase(BaseModel):
    description: str
    amount: Decimal
    type: str
    category_id: int
    user_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDBBase(BaseModel):
    id: int
    description: str
    amount: Decimal
    type: str
    category_id: int
    user_id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("amount")
    def serialize_amount(self, amount: Decimal, _info):
        return float(amount)


class TransactionInDB(TransactionInDBBase):
    category_rel: Category
