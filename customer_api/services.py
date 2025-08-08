import json

def process_csv(customers_file_path: str, purchased_file_path: str):
    try:
        with open(purchased_file_path) as file2:
            purchases_csv = json.load(file2)
    except FileNotFoundError:
        purchases_csv = {'purchases_csv' : 'Not Found'}
    
    try:
        with open(customers_file_path) as file1:
            customers_csv = json.load(file1)
    except FileNotFoundError:
        customers_csv = {'customers_csv' : 'Not Found'}
    
    return customers_csv, purchases_csv
