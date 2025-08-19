'''
Test using pytest the two api routes
'''
import os
os.environ["TESTING"] = "1"  # Must be set BEFORE main is imported
from fastapi.testclient import TestClient
import pytest
from main import app, pending_queue

client = TestClient(app)

# Indicate to main.py that this is a test (the worker will not start)
os.environ["TESTING"] = "1"

client = TestClient(app)

def test_import_csv_success(monkeypatch):
    # Mock process_csv to always return True
    monkeypatch.setattr("main.process_csv", lambda db, c_path, p_path: True)
    
    response = client.post("/import-csv/", json={
        "customers_file_path": "customers.csv",
        "purchased_file_path": "purchases.csv"
    })
    assert response.status_code == 200
    assert response.json() == {"status": "data saved into database"}

def test_send_customers_queued(monkeypatch):
    # Mock export_customers_with_purchases to return dummy data
    monkeypatch.setattr("main.export_customers_with_purchases", lambda db: {"dummy": "data"})
    
    # Mock requests.post so it does not actually send any HTTP request
    import requests
    class MockResponse:
        def raise_for_status(self): return None
        def json(self): return {"ok": True}
    monkeypatch.setattr(requests, "post", lambda *a, **kw: MockResponse())
    
    # Call the route
    response = client.post("/send-customers/")
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
    
    # Verify that the data was actually put into the queue
    queued_data = pending_queue.get_nowait()
    assert queued_data == {"dummy": "data"}
