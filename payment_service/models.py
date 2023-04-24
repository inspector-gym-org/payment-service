from datetime import datetime
from enum import Enum
from typing import Any, Callable, Generator
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], ObjectId], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema) -> None:
        field_schema.update(type="string")


class PaymentStatus(Enum):
    ACCEPTED = 1
    REJECTED = 2

    PROCESSING = 3
    CREATED = 4


class User(BaseModel):
    telegram_id: int


class ItemType(Enum):
    TRAINING_PLAN = 1


class Item(BaseModel):
    price: float

    item_type: ItemType
    training_plan_id: UUID | None


class Payment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: PaymentStatus = Field(default=PaymentStatus.CREATED)

    user: User
    items: list[Item]

    created: datetime = Field(default_factory=datetime.now)
    last_updated: datetime | None = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class PaymentUpdate(BaseModel):
    status: PaymentStatus

    last_updated: datetime = Field(default_factory=datetime.now)
