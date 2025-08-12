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

```
curl -X POST http://127.0.0.1:8000/send-customers/ --header 'Content-Type: application/json'
```

### Expected Response
```
{"Customers file":[{"title":2,"lastname":"Norris","firstname":"Chuck","postale_code":0,"city":"Fréjus","email":"chuck@norris.com"},{"title":1,"lastname":"Galante","firstname":"Marie","postale_code":0,"city":"","email":"marie-galante@france.fr"},{"title":2,"lastname":"Barbier","firstname":"Christophe","postale_code":0,"city":"Paris","email":"christophe@fake.email"},{"title":2,"lastname":"Dupont","firstname":"Eric","postale_code":0,"city":"Dijon","email":"eric.dupont@bourgogne.fr"},{"title":1,"lastname":"Wayne","firstname":"Bruce","postale_code":0,"city":"Montrouge","email":"bruce.wayne@display.aero"}],"Purchases file":[{"customer_id":2,"product_id":1221,"quantity":1,"price":10.0,"currency":"EUR","date":"2024-11-01"},{"customer_id":1,"product_id":4324,"quantity":1,"price":7.0,"currency":"EUR","date":"2024-11-02"},{"customer_id":3,"product_id":75672,"quantity":1,"price":91.2,"currency":"USD","date":"2050-12-31"},{"customer_id":3,"product_id":2123,"quantity":1,"price":13.0,"currency":"EUR","date":"2024-11-01"},{"customer_id":2,"product_id":3213,"quantity":1,"price":9.0,"currency":"EUR","date":"2025-01-02"},{"customer_id":6,"product_id":1221,"quantity":2,"price":10.0,"currency":"EUR","date":"2025-01-02"},{"customer_id":6,"product_id":2123,"quantity":1,"price":13.0,"currency":"EUR","date":"2025-01-02"},{"customer_id":6,"product_id":75672,"quantity":1,"price":91.2,"currency":"EUR","date":"2025-01-02"}]}
```
```
[{"salutation":"Mr.","last_name":"Norris","first_name":"Chuck","email":"chuck@norris.com","purchases":[{"product_id":4324,"price":7.0,"currency":"EUR","quantity":1,"purchased_at":"2024-11-02"}]},{"salutation":"Mrs.","last_name":"Galante","first_name":"Marie","email":"marie-galante@france.fr","purchases":[{"product_id":1221,"price":10.0,"currency":"EUR","quantity":1,"purchased_at":"2024-11-01"},{"product_id":3213,"price":9.0,"currency":"EUR","quantity":1,"purchased_at":"2025-01-02"}]},{"salutation":"Mr.","last_name":"Barbier","first_name":"Christophe","email":"christophe@fake.email","purchases":[{"product_id":75672,"price":91.2,"currency":"USD","quantity":1,"purchased_at":"2050-12-31"},{"product_id":2123,"price":13.0,"currency":"EUR","quantity":1,"purchased_at":"2024-11-01"}]},{"salutation":"Mr.","last_name":"Dupont","first_name":"Eric","email":"eric.dupont@bourgogne.fr","purchases":[]},{"salutation":"Mrs.","last_name":"Wayne","first_name":"Bruce","email":"bruce.wayne@display.aero","purchases":[{"product_id":1221,"price":10.0,"currency":"EUR","quantity":2,"purchased_at":"2025-01-02"},{"product_id":2123,"price":13.0,"currency":"EUR","quantity":1,"purchased_at":"2025-01-02"},{"product_id":75672,"price":91.2,"currency":"EUR","quantity":1,"purchased_at":"2025-01-02"}]}]
```

### Check data into sqlite Database
Check customers table :
```
sqlite3 ife.db -header -column "SELECT * FROM customers;"
customer_id  title  lastname  firstname   postal_code  city       email
-----------  -----  --------  ----------  -----------  ---------  ------------------------
1            2      Norris    Chuck       83600        Fréjus     chuck@norris.com
2            1      Galante   Marie       0                       marie-galante@france.fr
3            2      Barbier   Christophe  75009        Paris      christophe@fake.email
5            2      Dupont    Eric        21000        Dijon      eric.dupont@bourgogne.fr
6            1      Wayne     Bruce       92120        Montrouge  bruce.wayne@display.aero
```
Check purchases table :
```
sqlite3 ife.db -header -column "SELECT * FROM purchases;"purchase_identifier  customer_id  product_id  quantity  price  currency  date
-------------------  -----------  ----------  --------  -----  --------  ----------
2/01                 2            1221        1         10.0   EUR       2024-11-01
1/01                 1            4324        1         7.0    EUR       2024-11-02
3/01                 3            75672       1         91.2   USD       2050-12-31
3/02                 3            2123        1         13.0   EUR       2024-11-01
2/02                 2            3213        1         9.0    EUR       2025-01-02
6/01                 6            1221        2         10.0   EUR       2025-01-02
6/02                 6            2123        1         13.0   EUR       2025-01-02
6/03                 6            75672       1         91.2   EUR       2025-01-02
```

## Design Choices
- Rows in the CSV files that fail Pydantic validation are skipped to allow uninterrupted processing.
- postal_code and city are optional fields
- Logging can be enabled to capture and report invalid rows for further review.