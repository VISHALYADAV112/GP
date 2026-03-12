from main import app
from fastapi.testclient import TestClient
import sys
import traceback

try:
    print("Initializing TestClient...")
    client = TestClient(app)
    
    print("Testing /api/info ...")
    response = client.get("/api/info")
    print(f"Status: {response.status_code}")
    print(response.json())
    
    print("Testing /health ...")
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(response.json())
    
except Exception as e:
    print("FAILED APP INITIALIZATION:")
    traceback.print_exc()
    sys.exit(1)
