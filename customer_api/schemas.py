'''
Pydantic schemas to verufy data integrity before pushing into SQL DB
'''
from datetime import date
from pydantic import BaseModel, EmailStr, constr

class CsvPaths(BaseModel):
    '''
    Class dedicated to verify that both csv file are str
    '''
    customers_file_path: str
    purchased_file_path: str

class CustomerCreate(BaseModel):
    '''
    Class dedicated to store customers in pydantic objects
    '''
    customer_id: int
    title: int
    lastname: str
    firstname: str
    postale_code: int
    city: str
    email: EmailStr

class PurchasesCreate(BaseModel):
    '''
    Class dedicated to store purchases in pydantic objects
    '''
    purchase_identifier: str
    customer_id: int
    product_id: int
    quantity: int
    price: float
    currency: str
    date: date