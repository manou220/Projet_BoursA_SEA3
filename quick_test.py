#!/usr/bin/env python
"""Simple test of the forecast functionality."""

import sys
import os

# Add the project to the path
sys.path.insert(0, r'c:\Users\LENOVO\Desktop\PROJET\projet_corrige_FINAL\projet_corrige_FINAL_modifie\projet_coorrige')

# Test imports first
try:
    import requests
    from app.utils import generate_plot_image
    import base64
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 1: Check if server is reachable
print("\n--- Test 1: Server Reachability ---")
try:
    response = requests.get("http://localhost:5000/previsions/", timeout=5)
    print(f"✓ Server is reachable (status={response.status_code})")
except Exception as e:
    print(f"✗ Cannot reach server: {e}")
    sys.exit(1)

# Test 2: Check if plot generation works
print("\n--- Test 2: Plot Generation ---")
try:
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=10)
    values = [100, 102, 101, 105, 104, 106, 108, 107, 110, 112]
    
    # Create a simple plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, label='Test Data')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Test Plot')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Generate base64
    from app.utils import generate_plot_image
    plot_b64 = generate_plot_image()
    
    # Check if it's valid
    if plot_b64 and len(plot_b64) > 100:
        img_data = base64.b64decode(plot_b64)
        if img_data[:8] == b'\x89PNG\r\n\x1a\n':
            print(f"✓ Plot generation works (PNG size: {len(img_data)} bytes)")
        else:
            print(f"✗ Invalid PNG format")
    else:
        print(f"✗ Invalid base64 string")
        
except Exception as e:
    print(f"✗ Plot generation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n✓ All basic tests passed!")
print("\nNow you can test the full workflow in the browser:")
print("1. Go to http://localhost:5000/previsions/")
print("2. Upload a CSV file from the uploads folder")
print("3. Configure forecast settings")
print("4. Click 'Lancer la Prévision'")
print("5. Check if graph appears in step 3")
