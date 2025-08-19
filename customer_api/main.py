'''
Main file used to create fastAPI instances, creation/session of SQLite database
'''
import os
import time
import requests
from queue import Queue
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from schemas import CsvPaths
from models import Base
from services import process_csv, export_customers_with_purchases

SQLALCHEMY_DATABASE_URL = "sqlite:///./ife.db"

# Worker sleep 10 secondes between each retry
WORKER_SLEEP = 10

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Database file and Tables defined in models
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    """
    Creates a new database session
    """
    db = SessionLocal()
    try:
        # Gives a live DB session
        yield db
    finally:
        db.close()

# Local queue
pending_queue = Queue()

def worker():
    """
    Thread worker that consume data in queue and try to send data
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
            time.sleep(WORKER_SLEEP)
            # Put data back into queue to retry later
            pending_queue.put(data)
        finally:
            pending_queue.task_done()

# Launch worker on application start if not testing
if os.environ.get("TESTING") != "1":
    from threading import Thread
    # daemon = True --> Thread closed at the end of main app
    thread = Thread(target=worker, daemon=True)
    thread.start()

@app.post("/import-csv/")
def import_csv(paths: CsvPaths, db: Session = Depends(get_db)):
    '''
    Import CSV data from files and save data into SQL Tables
    @paths : 2 files path for customers and purchases
    @db : The database live session
    '''
    success = process_csv(db, paths.customers_file_path, paths.purchased_file_path)
    if success:
        return {"status": "data saved into database"}
    raise HTTPException(status_code=500, detail="failed to save data into database")
    
@app.post("/send-customers/")
def send_customers(db: Session = Depends(get_db)):
    '''
    Export data from SQL database and send it to the Worker Queue
    @db : The database live session
    '''
    export_data = export_customers_with_purchases(db)
    # Put data into worker queue
    pending_queue.put(export_data)
    return {"status": "queued", "message": "Data will be sent"}