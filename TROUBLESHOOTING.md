# LSEG M&A Data Extractor - Troubleshooting Guide

## Common Issues and Solutions

### 1. AttributeError: 'dict' object has no attribute 'url'

**Error Message:**
```
AttributeError: 'dict' object has no attribute 'url'
```

**Cause:** This is a compatibility issue between `httpx` (>= 0.26.0) and older versions of `lseg-data`.

**Solutions:**

#### Option A: Downgrade httpx (Recommended - Easiest)
```bash
pip install "httpx<0.26.0"
```

Then restart your Python kernel/environment and try again.

#### Option B: Upgrade lseg-data to latest version
```bash
pip install --upgrade lseg-data
```

This should install a version compatible with newer httpx.

#### Option C: Install specific compatible versions
```bash
pip install lseg-data==2.0.1 "httpx>=0.24.0,<0.26.0"
```

#### Option D: Set environment variable to disable proxy
If you're not using a proxy, you can disable proxy detection:

**On macOS/Linux:**
```bash
export NO_PROXY="*"
export no_proxy="*"
```

**On Windows (PowerShell):**
```powershell
$env:NO_PROXY="*"
$env:no_proxy="*"
```

Then restart Python.

---

### 2. AttributeError: 'DataFrame' object has no attribute 'to_pandas'

**Error Message:**
```
AttributeError: 'DataFrame' object has no attribute 'to_pandas'
```

**Cause:** This error occurs because the `rd.discovery.search()` function already returns a pandas DataFrame directly in newer versions of `lseg-data`, not an object with a `.to_pandas()` method.

**Solution:**

This has been fixed in the latest version of the script. If you're using an older version:

1. **Update the script:**
   ```bash
   git pull origin claude/lseg-ma-data-extraction-01UNjWFPUMqQWct3491M34yG
   ```

2. **Or manually fix** the code in `lseg_ma_extractor.py` around line 193:

   Replace:
   ```python
   df = response.to_pandas()
   ```

   With:
   ```python
   # Handle both old and new API versions
   if isinstance(response, pd.DataFrame):
       df = response
   elif hasattr(response, 'to_pandas'):
       df = response.to_pandas()
   elif hasattr(response, 'data') and hasattr(response.data, 'df'):
       df = response.data.df
   else:
       raise TypeError(f"Unexpected response type: {type(response)}")
   ```

The updated script automatically handles both old and new API response formats.

---

### 3. Session Connection Failed

**Error:** "Failed to open session"

**Solutions:**

#### For Desktop Session:
- Ensure LSEG Workspace or Eikon is **running and logged in**
- Check that you're logged into Workspace with valid credentials
- Try closing and reopening Workspace
- Ensure no firewall is blocking the connection

#### For Platform Session:
- Verify your credentials (app-key, client_id, client_secret)
- Check that your account has appropriate permissions
- Ensure you have an active LSEG Data Platform subscription
- Check network connectivity

---

### 4. Empty DataFrame Returned

**Issue:** `search_ma_deals()` returns an empty DataFrame

**Solutions:**

1. **Broaden your search criteria:**
   - Remove some filters
   - Expand the date range
   - Increase the `top` parameter

2. **Check your filters:**
   ```python
   # Too restrictive:
   deals = extractor.search_ma_deals(
       target_countries=['US'],
       min_transaction_value=10000,  # $10B is very high!
       start_date='2024-11-01',
       end_date='2024-11-22',  # Only 3 weeks
   )

   # Better:
   deals = extractor.search_ma_deals(
       target_countries=['US'],
       min_transaction_value=100,  # $100M
       start_date='2024-01-01',
       end_date='2024-11-22',
   )
   ```

3. **Test with minimal filters:**
   ```python
   # Simple test
   deals = extractor.search_ma_deals(
       start_date='2024-01-01',
       top=10
   )
   ```

---

### 5. ModuleNotFoundError: No module named 'lseg'

**Error:** `ModuleNotFoundError: No module named 'lseg'` or `'lseg.data'`

**Solution:**
```bash
pip install lseg-data pandas openpyxl
```

---

### 6. Permission/Authorization Errors

**Error:** 401 Unauthorized or 403 Forbidden

**Solutions:**

1. **Check credentials:**
   - Verify app-key, client_id, and client_secret are correct
   - Ensure no extra spaces or quotes in credentials

2. **Check entitlements:**
   - Contact your LSEG account representative
   - Verify your subscription includes M&A data access
   - Check if your account has `DEALS_MERGERS_AND_ACQUISITIONS` view access

3. **For Desktop Session:**
   - Re-login to LSEG Workspace
   - Check Workspace subscription status

---

### 7. SSL/Certificate Errors

**Error:** SSL certificate verification failed

**Solution (Not recommended for production):**
```python
import os
os.environ['LSEG_DATA_SSL_VERIFY'] = 'false'
```

**Better solution:** Update your CA certificates:
```bash
# macOS
brew install ca-certificates

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ca-certificates

# Windows
# Update Windows and ensure latest root certificates are installed
```

---

### 8. Rate Limiting Errors

**Error:** 429 Too Many Requests

**Solution:**
- Add delays between requests
- Reduce the frequency of API calls
- Contact LSEG to increase rate limits

```python
import time

# Add delay between requests
deals1 = extractor.search_ma_deals(...)
time.sleep(2)  # Wait 2 seconds
deals2 = extractor.search_ma_deals(...)
```

---

### 9. Memory Issues with Large Datasets

**Issue:** Running out of memory when retrieving large datasets

**Solutions:**

1. **Use pagination:**
   ```python
   all_deals = []
   skip = 0
   batch_size = 100

   while True:
       # Note: You may need to use the Content layer API for skip parameter
       deals = extractor.search_ma_deals(top=batch_size)
       if deals.empty:
           break
       all_deals.append(deals)
       skip += batch_size

   final_df = pd.concat(all_deals, ignore_index=True)
   ```

2. **Select only needed fields:**
   ```python
   deals = extractor.search_ma_deals(
       select_fields=[
           'TransactionAnnouncementDate',
           'TargetCompanyName',
           'AcquirerCompanyName',
           'TransactionValueIncludingNetDebtOfTarget'
       ]
   )
   ```

3. **Process in chunks:**
   ```python
   # Process by year
   for year in range(2020, 2025):
       deals = extractor.search_ma_deals(
           start_date=f'{year}-01-01',
           end_date=f'{year}-12-31'
       )
       extractor.export_to_csv(deals, f'deals_{year}.csv')
   ```

---

### 10. Jupyter Notebook Kernel Crashes

**Solutions:**

1. **Increase kernel memory:**
   - Restart kernel before running
   - Close other notebooks
   - Reduce dataset size

2. **Clear output regularly:**
   ```python
   from IPython.display import clear_output

   deals = extractor.search_ma_deals(...)
   print(f"Retrieved {len(deals)} deals")
   clear_output(wait=True)
   ```

---

### 11. Date Format Errors

**Issue:** Date filters not working as expected

**Solution:** Use YYYY-MM-DD format:
```python
# Correct:
deals = extractor.search_ma_deals(
    start_date='2024-01-01',  # YYYY-MM-DD
    end_date='2024-12-31'
)

# Incorrect:
deals = extractor.search_ma_deals(
    start_date='01/01/2024',  # Wrong format
    end_date='12-31-2024'      # Wrong format
)
```

---

## Checking Your Environment

Run this diagnostic script:

```python
import sys
print(f"Python version: {sys.version}")

try:
    import lseg.data as rd
    print(f"lseg.data version: {rd.__version__}")
except Exception as e:
    print(f"lseg.data error: {e}")

try:
    import httpx
    print(f"httpx version: {httpx.__version__}")
except Exception as e:
    print(f"httpx error: {e}")

try:
    import pandas as pd
    print(f"pandas version: {pd.__version__}")
except Exception as e:
    print(f"pandas error: {e}")
```

---

## Getting Help

1. **LSEG Developer Community:** https://community.developers.refinitiv.com/
2. **LSEG Support:** Contact your account representative
3. **GitHub Issues:** For issues with this script, open an issue in the repository

---

## Quick Fix Summary

**Most Common Issue (httpx compatibility):**
```bash
# Run this command and restart your Python environment
pip install "httpx<0.26.0"
```

**Fresh Install:**
```bash
# Uninstall everything and reinstall with compatible versions
pip uninstall lseg-data httpx -y
pip install lseg-data "httpx<0.26.0" pandas openpyxl
```
