'''
Models schema to create both Customers and Purchases databases into SQL databases
'''
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customers(Base):
    '''
    Database model in order to store Customer in csv file
    '''
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    title = Column(Integer, default=0, nullable=True)
    lastname = Column(String, default="", nullable=True)
    firstname = Column(String, default="", nullable=True)
    postal_code = Column(Integer, default=0, nullable=True)
    city = Column(String, default="", nullable=True)
    email = Column(String, default="", nullable=True)

    purchases = relationship("Purchases", back_populates="customer")

class Purchases(Base):
    '''
    Database model in order to store Purchases in csv file
    '''
    __tablename__ = "purchases"
    purchase_identifier = Column(String, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    customer = relationship("Customers", back_populates="purchases")