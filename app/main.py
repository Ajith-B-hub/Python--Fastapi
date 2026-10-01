from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db), _: str = Depends(get_current_user)) -> list[CustomerResponse]:
    return CustomerService.get_all(db)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)) -> CustomerResponse:
    return CustomerService.create(db, payload)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)) -> CustomerResponse:
    return CustomerService.get_by_id(db, customer_id)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)) -> CustomerResponse:
    return CustomerService.update(db, customer_id, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)) -> None:
    CustomerService.delete(db, customer_id)
    return None
