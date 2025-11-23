# LSEG M&A Database - Field Reference Guide

This comprehensive guide provides detailed information about the data fields available in the LSEG Mergers & Acquisitions (M&A) database through the Discovery Search API (`DEALS_MERGERS_AND_ACQUISITIONS` view).

## Overview

The LSEG M&A database contains over **1.51 million deals** since the 1970s with over **1,000 data elements** per transaction, including:
- Target and acquirer company profiles
- Deal terms and structure
- Financial and legal advisor information
- Deal valuations and pricing
- Transaction timeline and status
- Industry classifications

---

## How to Discover Available Fields

### Method 1: Using Metadata API (Recommended)

```python
import lseg.data as rd

# Open session first
rd.open_session()

# Get metadata for M&A deals
metadata = rd.discovery.metadata.Definition(
    view=rd.discovery.Views.DEALS_MERGERS_AND_ACQUISITIONS
).get_data()

# View all available fields
print(metadata.data.df)

# Close session
rd.close_session()
```

### Method 2: Data Item Browser (DIB)

Access the Data Item Browser tool within LSEG Workspace to search for available fields interactively. Navigate to **Deals > Mergers & Acquisitions** category.

### Method 3: Workspace Advanced Search

Build your query using the Advanced Search App in LSEG Workspace, add columns of interest, and export the query as Python code.

---

## Field Categories

## 1. Deal Identification Fields

### DealNumber
- **Field Name:** `DealNumber` or `SDCDealNumber`
- **Description:** Unique identifier assigned by LSEG to each M&A transaction
- **Type:** String/Number
- **Usage:** Primary key for deal identification and cross-referencing
- **Example:** `123456789`

### DealPermID
- **Field Name:** `DealPermID`
- **Description:** Permanent identifier for the deal in LSEG's PermID system
- **Type:** String
- **Usage:** Permanent, persistent identifier that doesn't change
- **Example:** `12-34567890123-E`

---

## 2. Transaction Date Fields

### TransactionAnnouncementDate
- **Field Name:** `TransactionAnnouncementDate`
- **Description:** Date when the M&A transaction was publicly announced
- **Type:** Date (YYYY-MM-DD)
- **Usage:** Filter and sort deals by announcement timing
- **Example:** `2024-03-15`

### TransactionEffectiveDate
- **Field Name:** `TransactionEffectiveDate` or `EffectiveDate`
- **Description:** Date when the transaction legally became effective or closed
- **Type:** Date (YYYY-MM-DD)
- **Usage:** Identify when deals were completed
- **Example:** `2024-06-30`

### TransactionWithdrawalDate
- **Field Name:** `TransactionWithdrawalDate`
- **Description:** Date when a proposed transaction was withdrawn or cancelled
- **Type:** Date (YYYY-MM-DD)
- **Usage:** Track failed or abandoned deals
- **Example:** `2024-04-20`

### ExpectedCompletionDate
- **Field Name:** `ExpectedCompletionDate`
- **Description:** Anticipated closing date for pending transactions
- **Type:** Date (YYYY-MM-DD)
- **Usage:** Monitor pending deal timelines
- **Example:** `2024-12-31`

---

## 3. Target Company Fields

### TargetCompanyName
- **Field Name:** `TargetCompanyName`
- **Description:** Full legal or common name of the company being acquired
- **Type:** String
- **Usage:** Identify the target company in transactions
- **Example:** `"Acme Corporation"`

### TargetRIC
- **Field Name:** `TargetRIC`
- **Description:** Reuters Instrument Code (RIC) for the target company's primary equity instrument
- **Type:** String
- **Usage:** Market-level identifier for pricing and data retrieval
- **Example:** `"ACME.N"` (Acme Corp on NYSE)
- **Format:** `TICKER.EXCHANGE` where exchange codes include:
  - `.N` = NYSE
  - `.O` = NASDAQ
  - `.L` = London Stock Exchange
  - `.T` = Tokyo Stock Exchange

### TargetTicker
- **Field Name:** `TargetTicker` or `TargetTickerSymbol`
- **Description:** Stock ticker symbol for the target company
- **Type:** String
- **Usage:** Identify traded securities
- **Example:** `"ACME"`

### TargetISIN
- **Field Name:** `TargetISIN`
- **Description:** International Securities Identification Number for target company's securities
- **Type:** String (12 characters)
- **Usage:** Global security identification
- **Example:** `"US0378331005"` (Apple Inc.)

### TargetPermID
- **Field Name:** `TargetPermID`
- **Description:** Permanent identifier for the target organization
- **Type:** String
- **Usage:** Persistent company identification across databases
- **Example:** `"4295905573"`

### TargetLEI
- **Field Name:** `TargetLEI`
- **Description:** Legal Entity Identifier for the target company
- **Type:** String (20 characters)
- **Usage:** Regulatory and compliance identification
- **Example:** `"549300VBUP8KXR3UMR59"`

### TargetCountry
- **Field Name:** `TargetCountry`
- **Description:** Country code (ISO 2-letter) where target company is headquartered
- **Type:** String (2 characters)
- **Usage:** Geographic filtering and analysis
- **Example:** `"US"`, `"UK"`, `"DE"`, `"JP"`, `"CN"`

### TargetNation
- **Field Name:** `TargetNation` or `TargetCountryName`
- **Description:** Full country name where target is headquartered
- **Type:** String
- **Usage:** Human-readable country identification
- **Example:** `"United States"`, `"United Kingdom"`

### TargetState
- **Field Name:** `TargetState` or `TargetStateProvince`
- **Description:** State or province of target company headquarters
- **Type:** String
- **Usage:** Sub-national geographic analysis
- **Example:** `"California"`, `"New York"`

### TargetCity
- **Field Name:** `TargetCity`
- **Description:** City where target company is headquartered
- **Type:** String
- **Usage:** Detailed location analysis
- **Example:** `"San Francisco"`, `"London"`

### TargetPublicStatus
- **Field Name:** `TargetPublicStatus`
- **Description:** Public/private status of target company at announcement
- **Type:** String (Enumerated)
- **Values:**
  - `"Public"` - Publicly traded company
  - `"Private"` - Privately held company
  - `"Subsidiary"` - Subsidiary of another company
  - `"Joint Venture"` - Joint venture entity
  - `"Government Owned"` - Government entity
- **Usage:** Filter by target ownership type
- **Example:** `"Public"`

### TargetMacroIndustry
- **Field Name:** `TargetMacroIndustry`
- **Description:** Broad industry classification for target company
- **Type:** String
- **Usage:** High-level industry analysis
- **Example:** `"Technology"`, `"Healthcare"`, `"Financials"`

### TargetMidIndustry
- **Field Name:** `TargetMidIndustry`
- **Description:** Mid-level industry classification (more specific than macro)
- **Type:** String
- **Usage:** Industry sector analysis
- **Example:** `"Software & IT Services"`, `"Pharmaceuticals"`

### TargetIndustry
- **Field Name:** `TargetIndustry`
- **Description:** Detailed industry classification
- **Type:** String
- **Usage:** Granular industry filtering
- **Example:** `"Application Software"`, `"Biotechnology"`

### TargetPrimarySICCode
- **Field Name:** `TargetPrimarySICCode`
- **Description:** Standard Industrial Classification code for target's primary business
- **Type:** String (4 digits)
- **Usage:** US-based industry classification
- **Example:** `"7372"` (Software)

### TargetPrimaryNAICSCode
- **Field Name:** `TargetPrimaryNAICSCode`
- **Description:** North American Industry Classification System code
- **Type:** String (6 digits)
- **Usage:** Modern industry classification system
- **Example:** `"511210"` (Software Publishers)

### TargetRevenue
- **Field Name:** `TargetRevenue` or `TargetLatestRevenue`
- **Description:** Target company's most recent annual revenue (in millions)
- **Type:** Number
- **Usage:** Size and scale analysis
- **Example:** `1250.5` (representing $1,250.5M)

### TargetEBITDA
- **Field Name:** `TargetEBITDA`
- **Description:** Target's Earnings Before Interest, Taxes, Depreciation & Amortization
- **Type:** Number
- **Usage:** Profitability analysis
- **Example:** `350.2`

### TargetEmployees
- **Field Name:** `TargetEmployees` or `TargetNumberOfEmployees`
- **Description:** Number of employees at target company
- **Type:** Number
- **Usage:** Company size analysis
- **Example:** `5000`

---

## 4. Acquirer Company Fields

### AcquirerCompanyName
- **Field Name:** `AcquirerCompanyName` or `AcquirorCompanyName`
- **Description:** Full name of the acquiring company
- **Type:** String
- **Usage:** Identify the buyer in transactions
- **Example:** `"Global Tech Inc."`

### AcquirerRIC
- **Field Name:** `AcquirerRIC` or `AcquirorRIC`
- **Description:** Reuters Instrument Code for the acquirer's equity
- **Type:** String
- **Usage:** Acquirer security identification
- **Example:** `"GTECH.O"`

### AcquirerTicker
- **Field Name:** `AcquirerTicker` or `AcquirorTickerSymbol`
- **Description:** Stock ticker symbol for acquirer
- **Type:** String
- **Usage:** Trading symbol lookup
- **Example:** `"GTECH"`

### AcquirerISIN
- **Field Name:** `AcquirerISIN`
- **Description:** ISIN for acquirer's securities
- **Type:** String (12 characters)
- **Usage:** Global acquirer security ID
- **Example:** `"US1234567890"`

### AcquirerPermID
- **Field Name:** `AcquirerPermID` or `AcquirorPermID`
- **Description:** Permanent identifier for acquiring organization
- **Type:** String
- **Usage:** Persistent acquirer identification
- **Example:** `"4295904307"`

### AcquirerLEI
- **Field Name:** `AcquirerLEI`
- **Description:** Legal Entity Identifier for acquirer
- **Type:** String (20 characters)
- **Usage:** Regulatory identification
- **Example:** `"213800WSGIIZCXF1P572"`

### AcquirerCountry
- **Field Name:** `AcquirerCountry` or `RCSAcquirerCountry`
- **Description:** ISO 2-letter country code for acquirer headquarters
- **Type:** String (2 characters)
- **Usage:** Geographic analysis of buyers
- **Example:** `"US"`, `"UK"`, `"CN"`

### AcquirerNation
- **Field Name:** `AcquirerNation` or `RCSAcquirerCountryName`
- **Description:** Full country name for acquirer
- **Type:** String
- **Usage:** Readable country name
- **Example:** `"United States"`

### AcquirerPublicStatus
- **Field Name:** `AcquirerPublicStatus`
- **Description:** Public/private status of acquiring company
- **Type:** String (Enumerated)
- **Values:**
  - `"Public"` - Publicly traded
  - `"Private"` - Privately held
  - `"Subsidiary"` - Subsidiary entity
  - `"Private Equity"` - PE-owned entity
  - `"Government Owned"` - Government entity
- **Usage:** Filter by acquirer ownership type
- **Example:** `"Public"`

### AcquirerMacroIndustry
- **Field Name:** `AcquirerMacroIndustry`
- **Description:** Broad industry classification for acquirer
- **Type:** String
- **Usage:** Cross-industry M&A analysis
- **Example:** `"Financials"`, `"Industrials"`

### AcquirerMidIndustry
- **Field Name:** `AcquirerMidIndustry`
- **Description:** Mid-level industry for acquirer
- **Type:** String
- **Usage:** Sector-level acquirer analysis
- **Example:** `"Banks"`, `"Insurance"`

### UltimateParentCompanyName
- **Field Name:** `UltimateParentCompanyName`
- **Description:** Name of ultimate parent company of acquirer
- **Type:** String
- **Usage:** Identify true corporate buyer
- **Example:** `"Berkshire Hathaway Inc."`

---

## 5. Transaction Value Fields

### TransactionValueIncludingNetDebt
- **Field Name:** `TransactionValueIncludingNetDebtOfTarget`
- **Description:** Total deal value including target's net debt (in millions USD)
- **Type:** Number
- **Usage:** Most comprehensive deal value metric
- **Example:** `5000.0` (representing $5 billion)
- **Note:** This is the most commonly used value field

### TransactionValue
- **Field Name:** `TransactionValue` or `DealValue`
- **Description:** Base transaction value (in millions)
- **Type:** Number
- **Usage:** Core deal size metric
- **Example:** `4500.0`

### ValueOfTransaction
- **Field Name:** `ValueOfTransaction`
- **Description:** Announced value of the transaction
- **Type:** Number
- **Usage:** Deal pricing analysis
- **Example:** `4750.5`

### EnterpriseValue
- **Field Name:** `EnterpriseValue`
- **Description:** Enterprise value of the target
- **Type:** Number
- **Usage:** Valuation analysis
- **Example:** `5200.0`

### EquityValue
- **Field Name:** `EquityValue`
- **Description:** Value of target's equity
- **Type:** Number
- **Usage:** Shareholder value analysis
- **Example:** `4000.0`

### PricePerShare
- **Field Name:** `PricePerShare` or `DealPricePerShare`
- **Description:** Offer price per share for target stock
- **Type:** Number
- **Usage:** Per-share pricing analysis
- **Example:** `95.50`

### PremiumPercentage
- **Field Name:** `PremiumPercentage` or `Premium1Day`
- **Description:** Premium offered over target's stock price (usually 1-day prior)
- **Type:** Number (percentage)
- **Usage:** Deal premium analysis
- **Example:** `25.5` (representing 25.5% premium)

### TransactionCurrency
- **Field Name:** `TransactionCurrency`
- **Description:** Currency in which deal value is denominated
- **Type:** String (3-letter ISO code)
- **Usage:** Currency analysis
- **Example:** `"USD"`, `"EUR"`, `"GBP"`

---

## 6. Transaction Status & Type Fields

### TransactionStatus
- **Field Name:** `TransactionStatus` or `DealStatus`
- **Description:** Current status of the transaction
- **Type:** String (Enumerated)
- **Values:**
  - `"Completed"` - Deal has closed
  - `"Pending"` - Deal announced, awaiting completion
  - `"Announced"` - Recently announced
  - `"Withdrawn"` - Deal cancelled or withdrawn
  - `"Rumored"` - Unconfirmed reports
  - `"Intended"` - Intent announced, not formal
- **Usage:** Filter by deal stage
- **Example:** `"Completed"`

### FormOfTransactionName
- **Field Name:** `FormOfTransactionName` or `DealType`
- **Description:** Type/structure of the transaction
- **Type:** String (Enumerated)
- **Values:**
  - `"Merger"` - Merger of equals or statutory merger
  - `"Acquisition"` - Outright acquisition
  - `"Acquisition of Partial Interest"` - Minority stake purchase
  - `"Acquisition of Remaining Interest"` - Squeeze-out transaction
  - `"Buyback"` - Share repurchase
  - `"Exchange Offer"` - Share exchange
  - `"Reverse Takeover"` - Private company acquires public shell
- **Usage:** Filter by transaction structure
- **Example:** `"Acquisition"`

### AttitudeOfDeal
- **Field Name:** `AttitudeOfDeal` or `DealAttitude`
- **Description:** Whether transaction is friendly or hostile
- **Type:** String (Enumerated)
- **Values:**
  - `"Friendly"` - Target board supports deal
  - `"Hostile"` - Unsolicited/opposed by target
  - `"Neutral"` - Neither friendly nor hostile
- **Usage:** Analyze deal dynamics
- **Example:** `"Friendly"`

### PercentageAcquired
- **Field Name:** `PercentageAcquired` or `PercentOfSharesAcquired`
- **Description:** Percentage of target company being acquired
- **Type:** Number (0-100)
- **Usage:** Full vs. partial acquisition analysis
- **Example:** `100.0` (full acquisition), `51.0` (majority stake)

### PercentageOwnedAfterTransaction
- **Field Name:** `PercentageOwnedAfterTransaction`
- **Description:** Total ownership percentage after deal closes
- **Type:** Number (0-100)
- **Usage:** Post-transaction ownership analysis
- **Example:** `75.0`

---

## 7. Payment & Consideration Fields

### ConsiderationStructure
- **Field Name:** `ConsiderationStructure` or `PaymentMethod`
- **Description:** How the deal is being paid for
- **Type:** String (Enumerated)
- **Values:**
  - `"Cash"` - All-cash transaction
  - `"Stock"` - All-stock transaction
  - `"Cash and Stock"` - Mixed consideration
  - `"Debt Assumption"` - Acquirer assumes debt
  - `"Other"` - Alternative structures
- **Usage:** Analyze payment methods
- **Example:** `"Cash and Stock"`

### CashAmount
- **Field Name:** `CashAmount` or `CashConsideration`
- **Description:** Cash portion of deal value (in millions)
- **Type:** Number
- **Usage:** Cash component analysis
- **Example:** `2500.0`

### StockAmount
- **Field Name:** `StockAmount` or `StockConsideration`
- **Description:** Stock portion of deal value (in millions)
- **Type:** Number
- **Usage:** Stock component analysis
- **Example:** `2500.0`

### ExchangeRatio
- **Field Name:** `ExchangeRatio`
- **Description:** Ratio of acquirer shares offered per target share
- **Type:** Number
- **Usage:** Stock-for-stock deal analysis
- **Example:** `0.85` (0.85 acquirer shares per target share)

---

## 8. Deal Summary & Description Fields

### DealSummary
- **Field Name:** `DealSummary` or `Synopsis`
- **Description:** Text description of the transaction
- **Type:** String (Long text)
- **Usage:** Qualitative deal analysis
- **Example:** `"Global Tech Inc. to acquire Acme Corp for $5 billion..."`

### DealRationale
- **Field Name:** `DealRationale`
- **Description:** Strategic rationale for the transaction
- **Type:** String (Long text)
- **Usage:** Understand strategic motivations
- **Example:** `"Expands market presence in Asia-Pacific region..."`

### DealHighlights
- **Field Name:** `DealHighlights`
- **Description:** Key highlights and terms of the deal
- **Type:** String (Long text)
- **Usage:** Quick deal overview
- **Example:** `"25% premium, expected synergies of $200M annually..."`

---

## 9. Advisor Fields

### TargetFinancialAdvisor
- **Field Name:** `TargetFinancialAdvisor` or `TargetAdvisor`
- **Description:** Name(s) of financial advisor(s) to target
- **Type:** String (may contain multiple, comma-separated)
- **Usage:** Track advisor market share
- **Example:** `"Goldman Sachs & Co."`

### AcquirerFinancialAdvisor
- **Field Name:** `AcquirerFinancialAdvisor` or `AcquirerAdvisor`
- **Description:** Name(s) of financial advisor(s) to acquirer
- **Type:** String (may contain multiple)
- **Usage:** Advisor league table analysis
- **Example:** `"Morgan Stanley, J.P. Morgan"`

### TargetLegalAdvisor
- **Field Name:** `TargetLegalAdvisor`
- **Description:** Legal counsel for target company
- **Type:** String
- **Usage:** Legal advisor analysis
- **Example:** `"Wachtell, Lipton, Rosen & Katz"`

### AcquirerLegalAdvisor
- **Field Name:** `AcquirerLegalAdvisor`
- **Description:** Legal counsel for acquirer
- **Type:** String
- **Usage:** Legal advisor tracking
- **Example:** `"Skadden, Arps, Slate, Meagher & Flom LLP"`

### AdvisorFees
- **Field Name:** `AdvisorFees` or `TotalAdvisorFees`
- **Description:** Total fees paid to advisors (in millions)
- **Type:** Number
- **Usage:** Fee analysis
- **Example:** `75.5`

---

## 10. Regulatory & Approval Fields

### RegulatoryApprovalRequired
- **Field Name:** `RegulatoryApprovalRequired`
- **Description:** Whether regulatory approval is needed
- **Type:** Boolean/String
- **Values:** `"Yes"`, `"No"`
- **Usage:** Regulatory risk assessment
- **Example:** `"Yes"`

### AntitrustReview
- **Field Name:** `AntitrustReview` or `HSRRequired`
- **Description:** Antitrust/competition review status
- **Type:** String
- **Usage:** Regulatory timeline tracking
- **Example:** `"Required"`, `"Not Required"`, `"Completed"`

### ShareholderApprovalRequired
- **Field Name:** `ShareholderApprovalRequired`
- **Description:** Whether shareholder vote is required
- **Type:** Boolean/String
- **Values:** `"Yes"`, `"No"`
- **Usage:** Deal approval analysis
- **Example:** `"Yes"`

### TargetShareholderApprovalDate
- **Field Name:** `TargetShareholderApprovalDate`
- **Description:** Date target shareholders approved deal
- **Type:** Date
- **Usage:** Timeline tracking
- **Example:** `2024-05-15`

---

## 11. Financing Fields

### FinancingType
- **Field Name:** `FinancingType`
- **Description:** Type of financing used for the deal
- **Type:** String
- **Values:** `"Bank Financing"`, `"Bond Issuance"`, `"Internal Funds"`, `"Mixed"`
- **Usage:** Financing structure analysis
- **Example:** `"Bank Financing"`

### DebtFinancing
- **Field Name:** `DebtFinancing` or `DebtFinancingAmount`
- **Description:** Amount of debt financing used (in millions)
- **Type:** Number
- **Usage:** Leverage analysis
- **Example:** `3000.0`

### BridgeLoanAmount
- **Field Name:** `BridgeLoanAmount`
- **Description:** Bridge loan facility amount
- **Type:** Number
- **Usage:** Short-term financing analysis
- **Example:** `1500.0`

---

## 12. Geographic & Cross-Border Fields

### CrossBorderDeal
- **Field Name:** `CrossBorderDeal` or `IsCrossBorder`
- **Description:** Whether deal crosses national borders
- **Type:** Boolean/String
- **Values:** `"Yes"`, `"No"`
- **Usage:** International M&A analysis
- **Example:** `"Yes"`

### DomesticDeal
- **Field Name:** `DomesticDeal`
- **Description:** Whether acquirer and target are in same country
- **Type:** Boolean/String
- **Usage:** Domestic vs. cross-border segmentation
- **Example:** `"No"`

### RegionOfTarget
- **Field Name:** `RegionOfTarget`
- **Description:** Geographic region of target
- **Type:** String
- **Values:** `"North America"`, `"Europe"`, `"Asia Pacific"`, `"Latin America"`, `"Middle East & Africa"`
- **Usage:** Regional analysis
- **Example:** `"North America"`

---

## 13. Sector & Industry Trend Fields

### MacroEconomicSector
- **Field Name:** `MacroEconomicSector`
- **Description:** Broad economic sector classification
- **Type:** String
- **Values:** `"Technology"`, `"Healthcare"`, `"Financials"`, `"Energy"`, `"Industrials"`, `"Consumer"`, `"Materials"`, `"Utilities"`, `"Real Estate"`, `"Telecommunications"`
- **Usage:** Sector-level M&A trends
- **Example:** `"Technology"`

### IsVerticalMerger
- **Field Name:** `IsVerticalMerger`
- **Description:** Whether deal is vertical integration
- **Type:** Boolean/String
- **Usage:** Strategic type classification
- **Example:** `"Yes"`

### IsHorizontalMerger
- **Field Name:** `IsHorizontalMerger`
- **Description:** Whether deal is between competitors
- **Type:** Boolean/String
- **Usage:** Consolidation analysis
- **Example:** `"Yes"`

---

## 14. ESG & Special Situation Fields

### ESGConsiderations
- **Field Name:** `ESGConsiderations`
- **Description:** Environmental, Social, Governance factors in deal
- **Type:** String (Long text)
- **Usage:** ESG-focused M&A analysis
- **Example:** `"Renewable energy focus..."`

### Divestiture
- **Field Name:** `Divestiture` or `IsDivestiture`
- **Description:** Whether transaction is a corporate divestiture
- **Type:** Boolean/String
- **Usage:** Divestiture activity tracking
- **Example:** `"Yes"`

### SpinOff
- **Field Name:** `SpinOff` or `IsSpinOff`
- **Description:** Whether transaction is a spin-off
- **Type:** Boolean/String
- **Usage:** Corporate restructuring analysis
- **Example:** `"No"`

### LeveragedBuyout
- **Field Name:** `LeveragedBuyout` or `IsLBO`
- **Description:** Whether deal is an LBO
- **Type:** Boolean/String
- **Usage:** Private equity deal identification
- **Example:** `"Yes"`

### GoingPrivateTransaction
- **Field Name:** `GoingPrivateTransaction`
- **Description:** Public-to-private transaction
- **Type:** Boolean/String
- **Usage:** Public-to-private trend analysis
- **Example:** `"Yes"`

---

## 15. Valuation Multiples Fields

### EVtoEBITDA
- **Field Name:** `EVtoEBITDA` or `EnterpriseValueToEBITDA`
- **Description:** Enterprise value to EBITDA multiple
- **Type:** Number
- **Usage:** Valuation analysis
- **Example:** `12.5` (representing 12.5x multiple)

### EVtoRevenue
- **Field Name:** `EVtoRevenue` or `EnterpriseValueToSales`
- **Description:** Enterprise value to revenue multiple
- **Type:** Number
- **Usage:** Revenue-based valuation
- **Example:** `3.2`

### PriceToEarnings
- **Field Name:** `PriceToEarnings` or `PE Ratio`
- **Description:** Price to earnings ratio offered
- **Type:** Number
- **Usage:** P/E-based valuation
- **Example:** `18.5`

### PriceToBook
- **Field Name:** `PriceToBook` or `PBRatio`
- **Description:** Price to book value ratio
- **Type:** Number
- **Usage:** Book value analysis
- **Example:** `2.3`

---

## Usage Examples in Python

### Example 1: Basic Field Selection

```python
from lseg_ma_extractor import LSEGMAExtractor

extractor = LSEGMAExtractor(session_type="desktop")
extractor.open_session()

# Select specific fields
deals = extractor.search_ma_deals(
    start_date='2024-01-01',
    select_fields=[
        'TransactionAnnouncementDate',
        'TargetCompanyName',
        'TargetRIC',
        'TargetCountry',
        'AcquirerCompanyName',
        'AcquirerRIC',
        'TransactionValueIncludingNetDebtOfTarget',
        'TransactionStatus'
    ],
    top=100
)

extractor.close_session()
```

### Example 2: Comprehensive Deal Profile

```python
# Get detailed deal information
deals = extractor.search_ma_deals(
    start_date='2024-01-01',
    select_fields=[
        # Identifiers
        'DealNumber',
        'DealPermID',

        # Target Info
        'TargetCompanyName',
        'TargetRIC',
        'TargetPermID',
        'TargetISIN',
        'TargetCountry',
        'TargetPublicStatus',
        'TargetMacroIndustry',

        # Acquirer Info
        'AcquirerCompanyName',
        'AcquirerRIC',
        'AcquirerPermID',
        'AcquirerCountry',
        'AcquirerPublicStatus',

        # Deal Terms
        'TransactionAnnouncementDate',
        'TransactionEffectiveDate',
        'TransactionValueIncludingNetDebtOfTarget',
        'TransactionStatus',
        'FormOfTransactionName',
        'ConsiderationStructure',
        'PremiumPercentage',

        # Advisors
        'TargetFinancialAdvisor',
        'AcquirerFinancialAdvisor',

        # Description
        'DealSummary'
    ],
    top=50
)
```

### Example 3: Identifier-Focused Query

```python
# Focus on company identifiers for data linking
deals = extractor.search_ma_deals(
    target_countries=['US'],
    start_date='2024-01-01',
    select_fields=[
        # Target Identifiers
        'TargetCompanyName',
        'TargetRIC',
        'TargetTicker',
        'TargetISIN',
        'TargetPermID',
        'TargetLEI',

        # Acquirer Identifiers
        'AcquirerCompanyName',
        'AcquirerRIC',
        'AcquirerTicker',
        'AcquirerISIN',
        'AcquirerPermID',
        'AcquirerLEI',

        # Deal basics
        'TransactionAnnouncementDate',
        'TransactionValueIncludingNetDebtOfTarget'
    ],
    top=100
)
```

---

## Field Naming Conventions

LSEG uses several naming patterns:

1. **Prefix patterns:**
   - `Target*` - Fields related to target company
   - `Acquirer*` / `Acquiror*` - Fields related to acquiring company
   - `Transaction*` - Fields related to the deal itself
   - `Deal*` - Alternative prefix for transaction fields

2. **Common suffixes:**
   - `*Date` - Date fields
   - `*Value` - Monetary values
   - `*Percentage` / `*Percent` - Percentage values
   - `*Status` - Status/state fields
   - `*Name` - Text name fields

3. **Identifier suffixes:**
   - `*RIC` - Reuters Instrument Code
   - `*Ticker` - Stock ticker symbol
   - `*ISIN` - International Securities ID
   - `*PermID` - Permanent identifier
   - `*LEI` - Legal Entity Identifier

---

## Important Notes

### Field Availability
- Not all fields are populated for every deal
- Historical deals may have limited data
- Field availability depends on deal type and data source
- Use metadata API to check which fields have data for your query results

### Field Naming Variations
- Some fields have alternative names (e.g., `AcquirerRIC` vs `AcquirorRIC`)
- Use metadata API to discover exact field names for your LSEG version
- Field names are case-sensitive in queries

### Data Types
- **Date fields:** Use YYYY-MM-DD format
- **Numeric fields:** Values in millions unless otherwise specified
- **Boolean fields:** May be represented as "Yes"/"No" strings
- **Enumerated fields:** Have specific allowed values (see field descriptions)

### Performance Tips
1. Only select fields you need - reduces data transfer and processing time
2. Use specific filters to narrow results before retrieving many fields
3. For large datasets, consider pagination or chunking by date range

---

## Additional Resources

- **LSEG Data Item Browser:** Interactive tool within Workspace to discover fields
- **Metadata API:** Programmatically discover available fields
- **LSEG Developer Community:** Ask questions about specific fields
- **Contact:** Your LSEG account representative for entitlements questions

---

## Getting Metadata Programmatically

To get a complete, up-to-date list of fields available for your account:

```python
import lseg.data as rd
import pandas as pd

rd.open_session()

# Get metadata
metadata_response = rd.discovery.metadata.Definition(
    view=rd.discovery.Views.DEALS_MERGERS_AND_ACQUISITIONS
).get_data()

# Extract field information
fields_df = metadata_response.data.df

# View field names and descriptions
print(fields_df[['name', 'description', 'type']])

# Export to CSV for reference
fields_df.to_csv('ma_fields_metadata.csv', index=False)

rd.close_session()
```

This will give you the definitive list of fields available for your specific LSEG entitlements and library version.

---

**Last Updated:** November 2024
**Version:** 1.0
**Coverage:** LSEG Data Library for Python 2.0+
