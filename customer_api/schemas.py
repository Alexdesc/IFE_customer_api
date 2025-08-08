'''
Pydantic schemas to store/get data to SQLite database
'''
from datetime import date
from pydantic import BaseModel, EmailStr, constr

class CsvPaths(BaseModel):
    '''
    Class dedicated to verify that both csv file are str
    '''
    customers_file_path: str
    purchased_file_path: str

class customerCreate(BaseModel):
    '''
    Class dedicated to store customers in pydantic objects
    '''
    title: int | None = 0
    lastname: str | None = ""
    firstname: str | None = ""
    postale_code: int | None = 00000
    city: str | None = ""
    email: EmailStr | None = ""

class customerRead(BaseModel):
    '''
    Class dedicated to get customers in pydantic objects
    '''
    customer_id: int
    title: int
    lastname: str
    firstname: str
    postale_code: int
    city: str
    email: EmailStr

class purchasesCreate(BaseModel):
    '''
    Class dedicated to store purchases in pydantic objects
    '''
    customer_id: int
    product_id: int
    quantity: int
    price: float
    currency: str
    date: date

class purchasesRead(BaseModel):
    '''
    Class dedicated to get purchases in pydantic objects
    '''
    #purchase_identifier: constr(regex=r'^\d{1,2}/\d{2}$')
    purchase_identifier: str
    customer_id: int
    product_id: int
    quantity: int
    price: float
    currency: str
    date: date