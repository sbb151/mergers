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

### ⚠️ Important: httpx Compatibility Issue

If you encounter an error like `AttributeError: 'dict' object has no attribute 'url'`, this is due to a compatibility issue between `httpx` and `lseg-data`.

**Quick fix:**
```bash
pip install "httpx<0.26.0"
```

Then restart your Python kernel/environment. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more details.

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

### Example 4: Public-to-Public Transactions

```python
# Filter by both target AND acquirer public status
public_deals = extractor.search_ma_deals(
    target_public_status='Public',
    acquirer_public_status='Public',  # NEW parameter!
    min_transaction_value=1000,  # $1B+
    transaction_status=['Completed'],
    start_date='2023-01-01',
    top=100
)
```

### Example 5: Custom Field Selection with Identifiers

```python
deals = extractor.search_ma_deals(
    target_countries=['US'],
    select_fields=[
        'TransactionAnnouncementDate',
        'TargetCompanyName',
        'TargetRIC',           # Reuters Instrument Code
        'TargetPermID',        # Permanent ID
        'TargetISIN',          # International Securities ID
        'AcquirerCompanyName',
        'AcquirerRIC',
        'AcquirerPermID',
        'TransactionValueIncludingNetDebtOfTarget',
        'DealSummary'
    ],
    top=100
)
```

## Available Fields

### 📚 Comprehensive Field Reference

For a **complete, detailed reference** of all 1,000+ available M&A data fields with definitions, data types, and usage examples, see **[FIELD_REFERENCE.md](FIELD_REFERENCE.md)**.

### Quick Reference

**Deal Information:**
- `DealNumber` - Unique deal identifier
- `DealPermID` - Permanent deal ID
- `TransactionAnnouncementDate` - Deal announcement date
- `TransactionEffectiveDate` - Deal closing/completion date
- `TransactionValueIncludingNetDebtOfTarget` - Deal value in millions (most comprehensive)
- `TransactionStatus` - Status (Completed, Pending, Withdrawn, etc.)
- `FormOfTransactionName` - Type (Merger, Acquisition, etc.)
- `DealSummary` - Deal description

**Target Company:**
- `TargetCompanyName` - Name of target company
- `TargetRIC` - Reuters Instrument Code (e.g., "AAPL.O")
- `TargetTicker` - Stock ticker symbol
- `TargetISIN` - International Securities ID
- `TargetPermID` - Permanent company ID
- `TargetLEI` - Legal Entity Identifier
- `TargetCountry` - Target country code (ISO 2-letter)
- `TargetPublicStatus` - Public/Private/Subsidiary
- `TargetMacroIndustry` - Broad industry sector
- `TargetMidIndustry` - Specific industry

**Acquirer Company:**
- `AcquirerCompanyName` - Name of acquiring company
- `AcquirerRIC` - Reuters Instrument Code
- `AcquirerTicker` - Stock ticker symbol
- `AcquirerISIN` - International Securities ID
- `AcquirerPermID` - Permanent company ID
- `AcquirerLEI` - Legal Entity Identifier
- `AcquirerCountry` - Acquirer country code
- `AcquirerPublicStatus` - Public/Private/Subsidiary
- `AcquirerMacroIndustry` - Broad industry sector

**Deal Terms:**
- `PricePerShare` - Offer price per share
- `PremiumPercentage` - Premium over market price
- `ConsiderationStructure` - Payment method (Cash/Stock/Mixed)
- `PercentageAcquired` - Percentage of target acquired
- `AttitudeOfDeal` - Friendly/Hostile

**Advisors:**
- `TargetFinancialAdvisor` - Target's financial advisor(s)
- `AcquirerFinancialAdvisor` - Acquirer's financial advisor(s)
- `TargetLegalAdvisor` - Target's legal counsel
- `AcquirerLegalAdvisor` - Acquirer's legal counsel

**See [FIELD_REFERENCE.md](FIELD_REFERENCE.md) for 100+ additional fields including valuation multiples, financing details, regulatory information, and more.**

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

## Public Status Options

For both `target_public_status` and `acquirer_public_status` parameters:

- `Public` - Publicly traded company
- `Private` - Privately held company
- `Subsidiary` - Subsidiary of another company
- `Private Equity` - Private equity-owned entity
- `Government Owned` - Government entity
- `Joint Venture` - Joint venture entity

**Example usage:**
```python
# Public company acquiring public company
deals = extractor.search_ma_deals(
    target_public_status='Public',
    acquirer_public_status='Public',
    ...
)

# Private equity acquisitions of public targets
deals = extractor.search_ma_deals(
    target_public_status='Public',
    acquirer_public_status='Private Equity',
    ...
)
```

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

For detailed troubleshooting information, see **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**.

### Common Issues

#### httpx Compatibility Error
If you see `AttributeError: 'dict' object has no attribute 'url'`:
```bash
pip install "httpx<0.26.0"
```
Then restart your Python kernel/environment.

#### Session Connection Issues

**Desktop Session**: Ensure LSEG Workspace/Eikon is running and you're logged in.

**Platform Session**: Verify your credentials are correct and you have appropriate permissions.

#### No Data Returned

Check your filter criteria - it may be too restrictive. Try:
- Expanding the date range
- Removing some filters
- Increasing the `top` parameter

#### Import Errors

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
