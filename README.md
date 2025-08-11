# IFE_customer_api

## Getting Started

1. Navigate to the `customer_api` directory:
```
cd customer_api
```

2. Start the FastAPI app with Uvicorn in reload mode:
```
python -m uvicorn main:app --reload
```
### Testing the API
You can test the CSV import endpoint with the following `curl` command:

```
curl -X POST http://127.0.0.1:8000/import-csv/ \
--header 'Content-Type: application/json' \
--data '{
"customers_file_path": "C:\\Users\\Alex\\Documents\\IFE_customer_api\\data\\customers.csv",
"purchased_file_path": "C:\\Users\\Alex\\Documents\\IFE_customer_api\\data\\purchases.csv"
}'
```
### Expected Response
```
{"Customers file":[{"title":2,"lastname":"Norris","firstname":"Chuck","postale_code":0,"city":"Fréjus","email":"chuck@norris.com"},{"title":1,"lastname":"Galante","firstname":"Marie","postale_code":0,"city":"","email":"marie-galante@france.fr"},{"title":2,"lastname":"Barbier","firstname":"Christophe","postale_code":0,"city":"Paris","email":"christophe@fake.email"},{"title":2,"lastname":"Dupont","firstname":"Eric","postale_code":0,"city":"Dijon","email":"eric.dupont@bourgogne.fr"},{"title":1,"lastname":"Wayne","firstname":"Bruce","postale_code":0,"city":"Montrouge","email":"bruce.wayne@display.aero"}],"Purchases file":[{"customer_id":2,"product_id":1221,"quantity":1,"price":10.0,"currency":"EUR","date":"2024-11-01"},{"customer_id":1,"product_id":4324,"quantity":1,"price":7.0,"currency":"EUR","date":"2024-11-02"},{"customer_id":3,"product_id":75672,"quantity":1,"price":91.2,"currency":"USD","date":"2050-12-31"},{"customer_id":3,"product_id":2123,"quantity":1,"price":13.0,"currency":"EUR","date":"2024-11-01"},{"customer_id":2,"product_id":3213,"quantity":1,"price":9.0,"currency":"EUR","date":"2025-01-02"},{"customer_id":6,"product_id":1221,"quantity":2,"price":10.0,"currency":"EUR","date":"2025-01-02"},{"customer_id":6,"product_id":2123,"quantity":1,"price":13.0,"currency":"EUR","date":"2025-01-02"},{"customer_id":6,"product_id":75672,"quantity":1,"price":91.2,"currency":"EUR","date":"2025-01-02"}]}
```

## Design Choices
- Rows in the CSV files that fail Pydantic validation are skipped to allow uninterrupted processing.
- Logging can be enabled to capture and report invalid rows for further review.