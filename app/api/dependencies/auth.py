from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.kafka_service import KafkaService
from app.services.redis_service import RedisService


class CustomerService:
    @staticmethod
    def get_all(db: Session) -> list[Customer]:
        return db.scalars(select(Customer).order_by(Customer.id)).all()

    @staticmethod
    def get_by_id(db: Session, customer_id: int) -> Customer:
        customer = db.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer

    @staticmethod
    def create(db: Session, payload: CustomerCreate) -> Customer:
        existing = db.scalar(select(Customer).where(Customer.email == payload.email))
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer with this email already exists")

        customer = Customer(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            phone=payload.phone,
            address=payload.address,
            is_active=payload.is_active,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

        RedisService.set_value(f"customer:{customer.id}", customer.to_dict() if hasattr(customer, "to_dict") else {"id": customer.id, "email": customer.email})
        KafkaService.publish_event(
            "customer-events",
            {
                "event": "customer_created",
                "customer_id": customer.id,
                "email": customer.email,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
        return customer

    @staticmethod
    def update(db: Session, customer_id: int, payload: CustomerUpdate) -> Customer:
        customer = CustomerService.get_by_id(db, customer_id)

        for field, value in payload.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(customer, field, value)

        customer.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(customer)

        RedisService.set_value(f"customer:{customer.id}", {"id": customer.id, "email": customer.email})
        KafkaService.publish_event(
            "customer-events",
            {"event": "customer_updated", "customer_id": customer.id, "email": customer.email, "timestamp": datetime.utcnow().isoformat()},
        )
        return customer

    @staticmethod
    def delete(db: Session, customer_id: int) -> None:
        customer = CustomerService.get_by_id(db, customer_id)
        db.delete(customer)
        db.commit()
        RedisService.delete_value(f"customer:{customer_id}")
        KafkaService.publish_event(
            "customer-events",
            {"event": "customer_deleted", "customer_id": customer_id, "timestamp": datetime.utcnow().isoformat()},
        )
