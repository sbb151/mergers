# LSEG M&A Data Extractor

A Python script for extracting Merger and Acquisition (M&A) data from the LSEG Data Library for Python.

## Features

- Extract M&A deal data from LSEG Data Platform
- Support for both Desktop Session (LSEG Workspace) and Platform Session authentication
- Flexible filtering by:
  - Target/Acquirer countries
  - Transaction value
  - Transaction status (Completed, Pending, Withdrawn, etc.)
  - Form of transaction (Merger, Acquisition)
  - Date range
  - Public/Private status
- Export data to CSV or Excel formats
- Comprehensive logging
- Easy-to-use API

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure you have access to LSEG Data Platform either through:
   - **Desktop Session**: LSEG Workspace/Eikon running on your machine
   - **Platform Session**: LSEG Data Platform credentials (app-key, client_id, client_secret)

## Quick Start

### Using Desktop Session (LSEG Workspace)

Make sure LSEG Workspace is running on your machine, then:

```python
from lseg_ma_extractor import LSEGMAExtractor

# Initialize with desktop session
extractor = LSEGMAExtractor(session_type="desktop")

# Open session
extractor.open_session()

# Get recent deals from last 30 days
recent_deals = extractor.get_recent_deals(days=30)
print(recent_deals)

# Export to CSV
extractor.export_to_csv(recent_deals, "ma_deals.csv")

# Close session
extractor.close_session()
```

### Using Platform Session (Cloud)

```python
from lseg_ma_extractor import LSEGMAExtractor

# Initialize with platform session
extractor = LSEGMAExtractor(session_type="platform")

# Open session with credentials
extractor.open_session(
    app_key="YOUR_APP_KEY",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)

# Search for deals
deals = extractor.search_ma_deals(
    target_countries=['US', 'UK'],
    min_transaction_value=100,  # $100M
    transaction_status=['Completed'],
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# Close session
extractor.close_session()
```

## Usage Examples

### Example 1: Recent M&A Deals

```python
# Get deals from last 60 days
recent_deals = extractor.get_recent_deals(days=60, top=100)
```

### Example 2: Large US Public Company Acquisitions

```python
large_deals = extractor.search_ma_deals(
    target_countries=['US'],
    min_transaction_value=500,  # $500M minimum
    target_public_status='Public',
    transaction_status=['Completed'],
    start_date='2024-01-01',
    end_date='2024-12-31',
    top=200
)
```

### Example 3: Cross-Border Mergers

```python
cross_border = extractor.search_ma_deals(
    target_countries=['UK', 'DE', 'FR'],
    acquirer_countries=['US', 'JP'],
    form_of_transaction=['Merger'],
    transaction_status=['Completed', 'Pending'],
    start_date='2023-01-01',
    top=150
)
```

### Example 4: Custom Field Selection

```python
deals = extractor.search_ma_deals(
    target_countries=['US'],
    select_fields=[
        'TransactionAnnouncementDate',
        'TargetCompanyName',
        'AcquirerCompanyName',
        'TransactionValueIncludingNetDebtOfTarget',
        'DealSummary',
        'AdvisorName',
        'AdvisorRole'
    ],
    top=100
)
```

## Available Fields

Common fields you can select:

- `TransactionAnnouncementDate` - Deal announcement date
- `TargetCompanyName` - Name of target company
- `TargetCountry` - Target country code
- `TargetRIC` - Target company RIC
- `TargetPublicStatus` - Public/Private status
- `AcquirerCompanyName` - Name of acquiring company
- `AcquirerCountry` - Acquirer country code
- `AcquirerRIC` - Acquirer company RIC
- `TransactionValueIncludingNetDebtOfTarget` - Deal value in millions
- `TransactionStatus` - Status (Completed, Pending, Withdrawn, etc.)
- `FormOfTransactionName` - Type (Merger, Acquisition, etc.)
- `DealSummary` - Deal description
- `AdvisorName` - Financial/Legal advisor name
- `AdvisorRole` - Advisor role

## Transaction Status Options

- `Completed` - Deal completed
- `Pending` - Deal pending completion
- `Announced` - Deal announced
- `Withdrawn` - Deal withdrawn
- `Rumored` - Rumored deal

## Form of Transaction Options

- `Merger` - Merger transactions
- `Acquisition` - Acquisition transactions
- `Buyback` - Share buyback
- `Reverse Takeover` - Reverse takeover

## Export Options

### Export to CSV

```python
extractor.export_to_csv(deals, "my_deals.csv")
```

### Export to Excel

```python
extractor.export_to_excel(deals, "my_deals.xlsx")
```

## Running the Example Script

The main script includes three example queries:

```bash
python lseg_ma_extractor.py
```

This will:
1. Fetch recent deals from the last 30 days
2. Search for large US & UK deals (>$100M, completed)
3. Find merger transactions only
4. Export results to CSV

## Configuration

For Platform Session, you can also use a configuration file. Create `lseg-data.config.json`:

```json
{
  "sessions": {
    "platform": {
      "app-key": "YOUR_APP_KEY",
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    }
  }
}
```

## M&A Database Coverage

The LSEG M&A database provides:
- Over 1.51 million deals
- Coverage since the 1970s
- 433,000+ US-target transactions
- 1.08+ million non-US target transactions
- 1,000+ data elements per deal

## Resources

- [LSEG Data Library Documentation](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python)
- [GitHub Examples](https://github.com/LSEG-API-Samples/Example.DataLibrary.Python)
- [Quick Reference Guide](https://developers.lseg.com/en/article-catalog/article/the-data-library-for-python-quick-reference-guide-access-layer)
- [LSEG Developer Community](https://community.developers.refinitiv.com/)

## Troubleshooting

### Session Connection Issues

**Desktop Session**: Ensure LSEG Workspace/Eikon is running and you're logged in.

**Platform Session**: Verify your credentials are correct and you have appropriate permissions.

### No Data Returned

Check your filter criteria - it may be too restrictive. Try:
- Expanding the date range
- Removing some filters
- Increasing the `top` parameter

### Import Errors

Ensure all dependencies are installed:
```bash
pip install --upgrade lseg-data pandas openpyxl
```

## License

This script is provided as-is for use with LSEG Data Platform. You must have appropriate LSEG licenses to access the data.

## Support

For issues with:
- **This script**: Open an issue in this repository
- **LSEG Data Library**: Visit [LSEG Developer Community](https://community.developers.refinitiv.com/)
- **Data access**: Contact your LSEG account representative
