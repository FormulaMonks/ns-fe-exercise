from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel
from .category import Category
from .tag import Tag

class TransactionGridItem(BaseModel):
    id: int
    description: str
    amount: Decimal
    type: str
    category: Category
    user_id: int
    date: datetime
    tags: List[Tag]

class TransactionGridResponse(BaseModel):
    items: List[TransactionGridItem]
    total: int
