from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .database import payments_collection
from .logging_route import LoggingRoute
from .models import Payment, PaymentCreate, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["payments"], route_class=LoggingRoute)


@router.post("/", response_model=Payment, status_code=status.HTTP_201_CREATED)
async def create_payment(payment_create: PaymentCreate) -> Payment:
    payment = Payment(**payment_create.dict())

    inserted_payment = await payments_collection.insert_one(jsonable_encoder(payment))
    return await payments_collection.find_one({"_id": inserted_payment.inserted_id})


@router.get("/{payment_id}/", response_model=Payment)
async def get_payment(payment_id: str) -> Payment:
    if payment := await payments_collection.find_one({"_id": payment_id}):
        return payment

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{payment_id}/", response_model=Payment)
async def update_payment(payment_id: str, payment_update: PaymentUpdate) -> Payment:
    update_result = await payments_collection.update_one(
        {"_id": payment_id}, {"$set": jsonable_encoder(payment_update)}
    )

    if update_result.modified_count == 1:
        if payment_json := await payments_collection.find_one({"_id": payment_id}):
            return payment_json

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
