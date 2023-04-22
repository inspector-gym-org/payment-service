from fastapi import APIRouter, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from .database import database
from .models import Payment

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=Payment)
async def create_payment(payment: Payment, response: Response) -> Payment:
    payment_json = jsonable_encoder(payment)

    try:
        await database["payments"].insert_one(payment_json)
        response.status_code = status.HTTP_201_CREATED

    except DuplicateKeyError:
        response.status_code = status.HTTP_200_OK

    return await database["users"].find_one({"_id": payment.id})


@router.get("/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str) -> Payment:
    if payment := await database["payments"].find_one({"_id": payment_id}):
        return payment

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
