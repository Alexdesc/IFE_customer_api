'''
Services, backend of fastAPI road execution
'''
import csv
from typing import Type, TypeVar
from pathlib import Path
from sqlalchemy.orm import Session
from pydantic import ValidationError
from models import Customers, Purchases
from schemas import CustomerCreate, PurchasesCreate

# I use this TypeVar in order for read_csv to have a generic list of object return
T = TypeVar("T")

def read_csv(path: Path, schema: Type[T]) -> list[T]:
    '''
    This function open and read a CSV file and then return a list of typed objects
    @path : Path of the file to open
    @schema : the desired dataclass type to return
    '''
    content = []
    try:
        with open(path, encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file, delimiter=";"):
                data = {k: v.strip() if v and v.strip() != "" else None for k, v in row.items()}
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
    '''
    Add a new list of customers into Customers SQLite database
    @db : The opened SQLite session
    @customers : The list of Customers 
    '''
    for people in customers:
        db_customer = Customers(
            customer_id=people.customer_id,
            title=people.title,
            lastname=people.lastname,
            firstname=people.firstname,
            postal_code=people.postal_code,
            city=people.city,
            email=people.email
        )
        # Merge if customer already exist
        db.merge(db_customer)
    db.commit()

def add_purchases(db: Session, purchases: list[PurchasesCreate]):
    '''
    Add a new list of purchases into Purchases SQLite database
    @db : The opened SQLite session
    @purchases : The list of Purchases 
    '''
    for transaction in purchases:
        db_purchase = Purchases(
            purchase_identifier=transaction.purchase_identifier,
            customer_id=transaction.customer_id,
            product_id=transaction.product_id,
            quantity=transaction.quantity,
            price=transaction.price,
            currency=transaction.currency,
            date=transaction.date
        )
        # Merge if purchase already exist
        db.merge(db_purchase)
    db.commit()

def process_csv(db: Session, customers_file_path: str, purchased_file_path: str):
    '''
    Process the fastapi endpoint /import-csv/
    @db : The opened SQLite session
    @customers_file_path : The local path to customer.csv
    @purchased_file_path : The local path to purchases.csv
    '''
    
    customers_content = read_csv(customers_file_path, CustomerCreate)
    purchases_content = read_csv(purchased_file_path, PurchasesCreate)

    add_customers(db, customers_content)
    add_purchases(db, purchases_content)
    
    return True

def export_customers_with_purchases(db: Session):
    '''
    Retrieves informations from database and format them
    @db : The opened SQLite session
    '''
    title_map = {1: "Mrs.", 2: "Mr."}

    data = [
        {
            "salutation": title_map.get(c.title, ""),
            "last_name": c.lastname,
            "first_name": c.firstname,
            "email": c.email,
            "purchases": [
                {
                    "product_id": p.product_id,
                    "price": p.price,
                    "currency": p.currency,
                    "quantity": p.quantity,
                    "purchased_at": p.date.isoformat()
                }
                for p in c.purchases
            ]
        }
        for c in db.query(Customers).all()
    ]
    return data