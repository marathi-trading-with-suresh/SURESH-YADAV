# Minor update to trigger Streamlit rebuild
import os, sys

# 🔧 Force current folder into Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scanner_module import scan_stocks

data = scan_stocks()

print("✅ Import OK. Timestamp:", data["timestamp"])
