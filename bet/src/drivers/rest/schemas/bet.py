from pydantic import BaseModel


class BetSchemaBase(BaseModel):
    pass


class BetSchemaAdd(BetSchemaBase):
    id_event: int
    amount: int
