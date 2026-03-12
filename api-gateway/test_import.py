import sys, os, importlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../services'))
try:
    mod = importlib.import_module('revenue-service.use_cases.receipts.cancel_receipt')
    print("Success:", mod.CancelReceiptUseCase)
except Exception as e:
    print("Error:", e)
