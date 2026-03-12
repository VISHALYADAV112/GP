import sys
import traceback

try:
    print("Loading main...")
    import main
    print("Main loaded. Starting uvicorn...")
    import uvicorn
    uvicorn.run(main.app, host="127.0.0.1", port=8001, log_level="debug")
except Exception as e:
    print(f"FAILED TO START! {e}")
    traceback.print_exc()
    sys.exit(1)
