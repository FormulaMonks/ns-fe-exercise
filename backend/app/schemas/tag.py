from pydantic import BaseModel, ConfigDict

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagInDBBase(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Tag(TagInDBBase):
    pass
