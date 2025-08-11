import csv
from typing import Type, TypeVar
from pathlib import Path
from sqlalchemy.orm import Session
from pydantic import ValidationError
from models import Customers, Purchases
from schemas import CustomerCreate, PurchasesCreate

T = TypeVar("T")

def read_csv(path: Path, schema: Type[T]) -> list[T]:
    content = []
    try:
        with open(path, encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file, delimiter=";"):
                data = {k: (v or "").strip() for k, v in row.items()}
                try:
                    obj = schema(**data)
                    content.append(obj)
                except ValidationError:
                    # I use this except in oder to continue execution
                    # We can use a logger to log invalid lines
                    continue
        return content
    except FileNotFoundError:
        return []
    
def add_customers(db: Session, customers: list[CustomerCreate]):
    for cust in customers:
        db_customer = Customers(
            title=cust.title or 0,
            lastname=cust.lastname or "",
            firstname=cust.firstname or "",
            postale_code=cust.postale_code or 0,
            city=cust.city or "",
            email=cust.email or ""
        )
        db.add(db_customer)
    db.commit()

def add_purchases(db: Session, purchases: list[PurchasesCreate]):
    for p in purchases:
        db_purchase = Purchases(
            customer_id=p.customer_id,
            product_id=p.product_id,
            quantity=p.quantity,
            price=p.price,
            currency=p.currency,
            date=p.date
        )
        db.add(db_purchase)
    db.commit()

def process_csv(db: Session, customers_file_path: str, purchased_file_path: str):
    customers_content = read_csv(customers_file_path, CustomerCreate)
    purchases_content = read_csv(purchased_file_path, PurchasesCreate)

    add_customers(db, customers_content)
    add_purchases(db, purchases_content)
    
    return customers_content, purchases_content
