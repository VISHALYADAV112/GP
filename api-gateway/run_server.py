import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting Uvicorn Server on 8002...")
    uvicorn.run(app, host="127.0.0.1", port=8002, workers=1)
