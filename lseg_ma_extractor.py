"""
LSEG Merger & Acquisition Data Extractor

This script extracts merger and acquisition data from the LSEG Data Library for Python.
It supports both Desktop Session (LSEG Workspace) and Platform Session authentication.

Requirements:
    pip install lseg-data pandas

Usage:
    python lseg_ma_extractor.py
"""

import lseg.data as rd
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LSEGMAExtractor:
    """Extract Merger and Acquisition data from LSEG Data Platform."""

    def __init__(self, session_type: str = "desktop"):
        """
        Initialize the LSEG M&A Data Extractor.

        Args:
            session_type: Either "desktop" (for LSEG Workspace) or "platform" (for cloud access)
        """
        self.session_type = session_type
        self.session = None

    def open_session(self, app_key: Optional[str] = None,
                     client_id: Optional[str] = None,
                     client_secret: Optional[str] = None) -> bool:
        """
        Open a session with LSEG Data Platform.

        Args:
            app_key: Application key (required for both session types)
            client_id: Client ID (required for platform session)
            client_secret: Client secret (required for platform session)

        Returns:
            bool: True if session opened successfully
        """
        try:
            if self.session_type == "desktop":
                logger.info("Opening Desktop Session (requires LSEG Workspace running)...")
                self.session = rd.open_session()
            elif self.session_type == "platform":
                if not all([app_key, client_id, client_secret]):
                    raise ValueError("Platform session requires app_key, client_id, and client_secret")
                logger.info("Opening Platform Session...")
                self.session = rd.open_session(
                    name="platform.ldp",
                    config={
                        "app-key": app_key,
                        "client_id": client_id,
                        "client_secret": client_secret
                    }
                )
            else:
                raise ValueError(f"Invalid session_type: {self.session_type}")

            logger.info("Session opened successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to open session: {str(e)}")
            return False

    def close_session(self):
        """Close the LSEG session."""
        if self.session:
            rd.close_session()
            logger.info("Session closed")

    def search_ma_deals(self,
                       target_countries: Optional[List[str]] = None,
                       acquirer_countries: Optional[List[str]] = None,
                       min_transaction_value: Optional[float] = None,
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None,
                       transaction_status: Optional[List[str]] = None,
                       form_of_transaction: Optional[List[str]] = None,
                       target_public_status: Optional[str] = None,
                       select_fields: Optional[List[str]] = None,
                       top: int = 100) -> pd.DataFrame:
        """
        Search for M&A deals with specified criteria.

        Args:
            target_countries: List of target country codes (e.g., ['US', 'UK', 'DE'])
            acquirer_countries: List of acquirer country codes
            min_transaction_value: Minimum transaction value in millions
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'
            transaction_status: List of statuses (e.g., ['Completed', 'Pending', 'Withdrawn'])
            form_of_transaction: List of transaction forms (e.g., ['Merger', 'Acquisition'])
            target_public_status: Target public status (e.g., 'Public', 'Private')
            select_fields: List of fields to retrieve
            top: Maximum number of results to return (default: 100)

        Returns:
            pd.DataFrame: DataFrame containing M&A deal data
        """
        try:
            # Build filter string
            filter_parts = []

            # Exclude standard exclusions
            filter_parts.append("(AcquirerCompanyName ne 'Creditors' and AcquirerCompanyName ne 'Shareholder')")

            # Target countries
            if target_countries:
                country_filters = " or ".join([f"TargetCountry eq '{c}'" for c in target_countries])
                filter_parts.append(f"({country_filters})")

            # Acquirer countries
            if acquirer_countries:
                country_filters = " or ".join([f"AcquirerCountry eq '{c}'" for c in acquirer_countries])
                filter_parts.append(f"({country_filters})")

            # Transaction value
            if min_transaction_value:
                filter_parts.append(f"TransactionValueIncludingNetDebtOfTarget ge {min_transaction_value}")

            # Target public status
            if target_public_status:
                filter_parts.append(f"TargetPublicStatus eq '{target_public_status}'")

            # Transaction status
            if transaction_status:
                status_filters = " or ".join([f"TransactionStatus eq '{s}'" for s in transaction_status])
                filter_parts.append(f"({status_filters})")

            # Form of transaction
            if form_of_transaction:
                form_filters = " or ".join([f"FormOfTransactionName xeq '{f}'" for f in form_of_transaction])
                filter_parts.append(f"({form_filters})")

            # Date range
            if start_date or end_date:
                date_parts = []
                if end_date:
                    date_parts.append(f"TransactionAnnouncementDate le {end_date}")
                if start_date:
                    date_parts.append(f"TransactionAnnouncementDate ge {start_date}")
                filter_parts.append(f"({' and '.join(date_parts)})")

            # Combine all filters
            filter_string = " and ".join(filter_parts)

            # Default select fields if not provided
            if not select_fields:
                select_fields = [
                    'TransactionAnnouncementDate',
                    'TargetCompanyName',
                    'TargetCountry',
                    'TargetRIC',
                    'AcquirerCompanyName',
                    'AcquirerCountry',
                    'AcquirerRIC',
                    'TransactionValueIncludingNetDebtOfTarget',
                    'TransactionStatus',
                    'FormOfTransactionName',
                    'TargetPublicStatus',
                    'DealSummary'
                ]

            select_string = ', '.join(select_fields)

            logger.info(f"Searching M&A deals with filter: {filter_string}")

            # Execute search
            response = rd.discovery.search(
                view=rd.discovery.Views.DEALS_MERGERS_AND_ACQUISITIONS,
                filter=filter_string,
                select=select_string,
                top=top
            )

            # The response is already a DataFrame in newer versions of lseg-data
            # Handle both old API (with .to_pandas()) and new API (direct DataFrame)
            if isinstance(response, pd.DataFrame):
                df = response
            elif hasattr(response, 'to_pandas'):
                df = response.to_pandas()
            elif hasattr(response, 'data') and hasattr(response.data, 'df'):
                df = response.data.df
            else:
                raise TypeError(f"Unexpected response type: {type(response)}")

            logger.info(f"Retrieved {len(df)} M&A deals")

            return df

        except Exception as e:
            logger.error(f"Error searching M&A deals: {str(e)}")
            raise

    def get_recent_deals(self, days: int = 30, top: int = 50) -> pd.DataFrame:
        """
        Get recent M&A deals from the last N days.

        Args:
            days: Number of days to look back (default: 30)
            top: Maximum number of results (default: 50)

        Returns:
            pd.DataFrame: DataFrame containing recent M&A deals
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        logger.info(f"Fetching M&A deals from {start_date} to {end_date}")

        return self.search_ma_deals(
            start_date=start_date,
            end_date=end_date,
            transaction_status=['Completed', 'Pending', 'Announced'],
            top=top
        )

    def export_to_csv(self, df: pd.DataFrame, filename: str = None):
        """
        Export DataFrame to CSV file.

        Args:
            df: DataFrame to export
            filename: Output filename (default: ma_deals_YYYYMMDD.csv)
        """
        if filename is None:
            filename = f"ma_deals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        df.to_csv(filename, index=False)
        logger.info(f"Data exported to {filename}")

    def export_to_excel(self, df: pd.DataFrame, filename: str = None):
        """
        Export DataFrame to Excel file.

        Args:
            df: DataFrame to export
            filename: Output filename (default: ma_deals_YYYYMMDD.xlsx)
        """
        if filename is None:
            filename = f"ma_deals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        df.to_excel(filename, index=False, engine='openpyxl')
        logger.info(f"Data exported to {filename}")


def main():
    """Main function demonstrating usage of the LSEG M&A Extractor."""

    # Initialize extractor with Desktop Session (default)
    # For Platform Session, use: extractor = LSEGMAExtractor(session_type="platform")
    extractor = LSEGMAExtractor(session_type="desktop")

    try:
        # Open session
        # For Desktop Session (LSEG Workspace must be running)
        if not extractor.open_session():
            logger.error("Failed to open session. Exiting.")
            return

        # For Platform Session, uncomment and provide credentials:
        # if not extractor.open_session(
        #     app_key="YOUR_APP_KEY",
        #     client_id="YOUR_CLIENT_ID",
        #     client_secret="YOUR_CLIENT_SECRET"
        # ):
        #     logger.error("Failed to open session. Exiting.")
        #     return

        # Example 1: Get recent deals from last 30 days
        logger.info("\n=== Example 1: Recent M&A Deals (Last 30 Days) ===")
        recent_deals = extractor.get_recent_deals(days=30, top=50)
        print(f"\nFound {len(recent_deals)} recent deals")
        print(recent_deals.head())

        # Example 2: Search for specific criteria
        logger.info("\n=== Example 2: US & UK M&A Deals (Completed, >$100M) ===")
        large_deals = extractor.search_ma_deals(
            target_countries=['US', 'UK'],
            min_transaction_value=100,  # $100M
            transaction_status=['Completed'],
            target_public_status='Public',
            start_date='2024-01-01',
            end_date='2024-12-31',
            top=100
        )
        print(f"\nFound {len(large_deals)} large deals")
        print(large_deals.head())

        # Example 3: Search for mergers only
        logger.info("\n=== Example 3: Merger Transactions Only ===")
        mergers = extractor.search_ma_deals(
            form_of_transaction=['Merger'],
            transaction_status=['Completed', 'Pending'],
            start_date='2024-01-01',
            top=50
        )
        print(f"\nFound {len(mergers)} merger transactions")
        print(mergers.head())

        # Export data
        if not recent_deals.empty:
            extractor.export_to_csv(recent_deals, "recent_ma_deals.csv")
            # Uncomment to export to Excel (requires openpyxl):
            # extractor.export_to_excel(recent_deals, "recent_ma_deals.xlsx")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")

    finally:
        # Always close the session
        extractor.close_session()


if __name__ == "__main__":
    main()
