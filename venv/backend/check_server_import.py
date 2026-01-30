import sys
import os

try:
    print("Attempting to import server...")
    import server
    print("Server imported successfully.")
except Exception as e:
    import traceback
    print("CRASH DURING IMPORT:")
    traceback.print_exc()
