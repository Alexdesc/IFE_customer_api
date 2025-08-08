# IFE_customer_api

Se placer dans le dossier customer_api puis lancer la commande :
```
uvicorn main:app --reload
```

Pour tester les routes implémentées :

```
curl -X POST http://127.0.0.1:8000/import-csv/ --header 'Content-Type: application/json' --data '{
"customers_file_path": "C:\Users\Alex\Documents\IFE_customer_api\data\customers.csv",
"purchased_file_path": "C:\Users\Alex\Documents\IFE_customer_api\data\purchases.csv"
}'
```
Exemple de réponse attendue :
```
{"Customers file":"/opt/custexport/customers.csv","Purchases file":"/opt/custexport/purchases.csv"}
```