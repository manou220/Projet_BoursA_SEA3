#!/usr/bin/env python
"""
End-to-end test for forecast functionality.
Tests the complete workflow: upload -> analyze -> forecast with graph generation.
"""

import requests
import json
import base64
from pathlib import Path

BASE_URL = "http://localhost:5000"
TEST_FILE = "uploads/test_data.csv"

def test_forecast_workflow():
    """Test the complete forecast workflow."""
    print("=" * 60)
    print("TESTING FORECAST WORKFLOW")
    print("=" * 60)
    
    session = requests.Session()
    
    # Step 1: Upload file
    print("\n1. Testing file upload...")
    with open(TEST_FILE, 'rb') as f:
        files = {'file': f}
        response = session.post(
            f"{BASE_URL}/upload_file",
            files=files,
            data={'source_type': 'local'}
        )
    
    if response.status_code != 200:
        print(f"   ❌ Upload failed: {response.status_code}")
        print(f"   Response: {response.text[:500]}")
        return False
    
    upload_data = response.json()
    if not upload_data.get('success'):
        print(f"   ❌ Upload not successful: {upload_data}")
        return False
    
    print(f"   ✓ Upload successful")
    print(f"   Filename: {upload_data.get('filename')}")
    print(f"   Columns: {upload_data.get('columns', [])[:3]}...")
    
    # Step 2: Test forecast submission
    print("\n2. Testing forecast submission...")
    
    forecast_data = {
        'forecast_filename': upload_data.get('filename'),
        'target_column': 'Close',
        'forecast_steps': 5,
        'confidence_level': 95,
        'forecast_interval': 'jour',
        'forecast_type': 'close_price',
        'selected_model_file': 'model_final_bourse_xgboost.joblib',
        'ajax': 'true'
    }
    
    response = session.post(
        f"{BASE_URL}/previsions/",
        data=forecast_data,
        headers={'Accept': 'application/json'}
    )
    
    if response.status_code != 200:
        print(f"   ❌ Forecast failed: {response.status_code}")
        print(f"   Response: {response.text[:500]}")
        return False
    
    try:
        forecast_result = response.json()
    except json.JSONDecodeError:
        print(f"   ❌ Response is not JSON: {response.text[:200]}")
        return False
    
    if not forecast_result.get('success'):
        print(f"   ❌ Forecast not successful: {forecast_result}")
        return False
    
    print(f"   ✓ Forecast successful")
    
    # Step 3: Verify graph data
    print("\n3. Verifying graph data...")
    
    forecast_plot = forecast_result.get('forecast_plot')
    if not forecast_plot:
        print(f"   ❌ No forecast_plot in response")
        return False
    
    # Verify it's valid base64
    try:
        img_data = base64.b64decode(forecast_plot)
        print(f"   ✓ Valid base64 image ({len(img_data)} bytes)")
        
        # Check if it looks like a PNG (starts with PNG magic bytes)
        if img_data[:8] == b'\x89PNG\r\n\x1a\n':
            print(f"   ✓ Valid PNG image")
        else:
            print(f"   ⚠️  Image data doesn't start with PNG magic bytes")
    except Exception as e:
        print(f"   ❌ Invalid base64: {e}")
        return False
    
    # Step 4: Verify table data
    print("\n4. Verifying forecast table...")
    
    forecast_results = forecast_result.get('forecast_results')
    if not forecast_results:
        print(f"   ❌ No forecast_results in response")
        return False
    
    if '<table' not in forecast_results:
        print(f"   ❌ forecast_results doesn't contain table HTML")
        return False
    
    print(f"   ✓ Valid HTML table")
    
    # Step 5: Verify metrics
    print("\n5. Verifying forecast metrics...")
    
    metrics = forecast_result.get('forecast_metrics')
    if not metrics:
        print(f"   ❌ No metrics in response")
        return False
    
    print(f"   ✓ Metrics present:")
    for key, value in metrics.items():
        print(f"     - {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    try:
        success = test_forecast_workflow()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
