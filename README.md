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
{"status":"data saved into database"}
```
```
{"status":"queued","message":"Data will be sent"}
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
- With more time, use a real message broker to send data to external API.