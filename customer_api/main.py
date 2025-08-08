import json
from fastapi import FastAPI
from schemas import CsvPaths
from services import process_csv

app = FastAPI()

@app.post("/import-csv/")
def import_csv(paths: CsvPaths):
    customer_content, purchases_content = process_csv(paths.customers_file_path, paths.purchased_file_path)
    return {"Customers file": json.dump(customer_content), "Purchases file": json.dump(purchases_content)}

@app.post("/send-customers/")
def create_item():
    return {"message": "Hello again, FastAPI!"}