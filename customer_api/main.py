'''
Main file used to create fastAPI instances, creation/session of SQLite database
'''
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from schemas import CsvPaths
from models import Base
from services import process_csv, export_customers_with_purchases

SQLALCHEMY_DATABASE_URL = "sqlite:///./ife.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/import-csv/")
def import_csv(paths: CsvPaths, db: Session = Depends(get_db)):
    customers_content, purchases_content = process_csv(
        db,
        paths.customers_file_path, 
        paths.purchased_file_path
    )
    return {
        "Customers file": customers_content,
        "Purchases file": purchases_content
    }

@app.post("/send-customers/")
def export_data(db: Session = Depends(get_db)):
    return export_customers_with_purchases(db)