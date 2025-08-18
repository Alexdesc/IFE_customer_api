'''
Main file used to create fastAPI instances, creation/session of SQLite database
'''
import time
import requests
from queue import Queue
from threading import Thread
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
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

# Local queue
pending_queue = Queue()

def worker():
    """
    Thread worker that consome data in queue and try to send data
    ToDo: Better solution, use a dedicated message broker
    """
    while True:
        data = pending_queue.get()
        try:
            response = requests.post("https://mockapi.example.com/v1/customers", json=data, timeout=5)
            response.raise_for_status()
            print(f"[OK] Data sent : {response.json()}")
        except Exception as e:
            print(f"[ERROR] Try again in 10s : {e}")
            time.sleep(10)
            pending_queue.put(data)  # Put data back into queue to retry later
        finally:
            pending_queue.task_done()

# Launch worker at start
thread = Thread(target=worker, daemon=True)
thread.start()

@app.post("/import-csv/")
def import_csv(paths: CsvPaths, db: Session = Depends(get_db)):
    success = process_csv(db, paths.customers_file_path, paths.purchased_file_path)
    if success:
        return {"status": "data saved into database"}
    raise HTTPException(status_code=500, detail="failed to save data into database")
    
@app.post("/send-customers/")
def send_customers(db: Session = Depends(get_db)):
    export_data = export_customers_with_purchases(db)
    # Put data into worker queue
    pending_queue.put(export_data)
    return {"status": "queued", "message": "Data will be sent"}