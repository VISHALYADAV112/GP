import requests
import json
import time

BASE_URL = "http://localhost:8002/api/v1"

def print_response(name, res):
    print(f"\n--- {name} ---")
    print(f"Status: {res.status_code}")
    try:
        print(json.dumps(res.json(), indent=2))
    except:
        print(res.text)

print("Waiting for API Gateway to boot...")
time.sleep(2)

# 1. Health & Root Info
try:
    print_response("Root Info", requests.get("http://localhost:8002/api/info"))
    print_response("Health Check", requests.get("http://localhost:8002/health"))
except Exception as e:
    print(f"Failed to connect to API Gateway: {e}")
    exit(1)

# 2. Let's try to hit the financial and revenue routers to see what endpoints they expose
print("\nScanning available routes from OpenAPI spec...")
try:
    openapi = requests.get("http://localhost:8002/api/openapi.json").json()
    paths = list(openapi['paths'].keys())
    print(f"Found {len(paths)} registered endpoints:")
    for p in paths:
        methods = list(openapi['paths'][p].keys())
        print(f"  {methods} {p}")
except Exception as e:
    print(f"Failed to fetch OpenAPI spec: {e}")
