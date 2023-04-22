from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .database import database
from .models import Payment

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=Payment, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: Payment) -> Payment:
    payment_json = jsonable_encoder(payment)

    inserted_payment = await database["payments"].insert_one(payment_json)
    return await database["payments"].find_one({"_id": inserted_payment.inserted_id})


@router.get("/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str) -> Payment:
    if payment := await database["payments"].find_one({"_id": payment_id}):
        return payment

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
