"""
Advanced Examples for LSEG M&A Data Extractor

This script demonstrates various use cases for extracting M&A data.
"""

from lseg_ma_extractor import LSEGMAExtractor
import pandas as pd


def example_tech_acquisitions():
    """Example: Find technology sector acquisitions in the US."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Technology Sector Acquisitions in the US")
    print("="*60)

    extractor = LSEGMAExtractor(session_type="desktop")

    try:
        extractor.open_session()

        # Search for tech acquisitions
        tech_deals = extractor.search_ma_deals(
            target_countries=['US'],
            min_transaction_value=50,  # $50M minimum
            transaction_status=['Completed', 'Pending'],
            form_of_transaction=['Acquisition'],
            start_date='2024-01-01',
            end_date='2024-12-31',
            top=100
        )

        print(f"\nFound {len(tech_deals)} technology acquisitions")
        print("\nTop 10 by transaction value:")
        top_10 = tech_deals.nlargest(10, 'TransactionValueIncludingNetDebtOfTarget')
        print(top_10[['TransactionAnnouncementDate', 'TargetCompanyName',
                      'AcquirerCompanyName', 'TransactionValueIncludingNetDebtOfTarget']])

        # Export
        extractor.export_to_csv(tech_deals, "tech_acquisitions_2024.csv")

    finally:
        extractor.close_session()


def example_cross_border_deals():
    """Example: Analyze cross-border M&A activity."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Cross-Border M&A Activity")
    print("="*60)

    extractor = LSEGMAExtractor(session_type="desktop")

    try:
        extractor.open_session()

        # US companies acquiring in Europe
        us_to_eu = extractor.search_ma_deals(
            acquirer_countries=['US'],
            target_countries=['UK', 'DE', 'FR', 'IT', 'ES'],
            transaction_status=['Completed'],
            start_date='2023-01-01',
            end_date='2024-12-31',
            top=200
        )

        print(f"\nUS → Europe M&A: {len(us_to_eu)} deals")

        # Group by target country
        if not us_to_eu.empty:
            country_stats = us_to_eu.groupby('TargetCountry').agg({
                'TargetCompanyName': 'count',
                'TransactionValueIncludingNetDebtOfTarget': ['sum', 'mean']
            })
            print("\nDeals by Target Country:")
            print(country_stats)

        # Export
        extractor.export_to_csv(us_to_eu, "us_to_europe_ma.csv")

    finally:
        extractor.close_session()


def example_mega_deals():
    """Example: Find mega-deals (>$1B)."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Mega-Deals (>$1 Billion)")
    print("="*60)

    extractor = LSEGMAExtractor(session_type="desktop")

    try:
        extractor.open_session()

        # Search for deals over $1 billion
        mega_deals = extractor.search_ma_deals(
            min_transaction_value=1000,  # $1B
            transaction_status=['Completed', 'Pending', 'Announced'],
            start_date='2023-01-01',
            select_fields=[
                'TransactionAnnouncementDate',
                'TargetCompanyName',
                'TargetCountry',
                'AcquirerCompanyName',
                'AcquirerCountry',
                'TransactionValueIncludingNetDebtOfTarget',
                'TransactionStatus',
                'FormOfTransactionName',
                'DealSummary'
            ],
            top=100
        )

        print(f"\nFound {len(mega_deals)} mega-deals")

        if not mega_deals.empty:
            # Sort by value
            mega_deals_sorted = mega_deals.sort_values(
                'TransactionValueIncludingNetDebtOfTarget',
                ascending=False
            )

            print("\nTop 10 Largest Deals:")
            print(mega_deals_sorted.head(10)[['TransactionAnnouncementDate',
                                               'TargetCompanyName',
                                               'AcquirerCompanyName',
                                               'TransactionValueIncludingNetDebtOfTarget']])

            # Statistics
            print(f"\nTotal Deal Value: ${mega_deals['TransactionValueIncludingNetDebtOfTarget'].sum():.2f}M")
            print(f"Average Deal Value: ${mega_deals['TransactionValueIncludingNetDebtOfTarget'].mean():.2f}M")
            print(f"Median Deal Value: ${mega_deals['TransactionValueIncludingNetDebtOfTarget'].median():.2f}M")

        # Export
        extractor.export_to_csv(mega_deals, "mega_deals.csv")

    finally:
        extractor.close_session()


def example_quarterly_analysis():
    """Example: Analyze M&A activity by quarter."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Quarterly M&A Analysis (2024)")
    print("="*60)

    extractor = LSEGMAExtractor(session_type="desktop")

    try:
        extractor.open_session()

        quarters = [
            ('Q1 2024', '2024-01-01', '2024-03-31'),
            ('Q2 2024', '2024-04-01', '2024-06-30'),
            ('Q3 2024', '2024-07-01', '2024-09-30'),
            ('Q4 2024', '2024-10-01', '2024-12-31')
        ]

        quarterly_results = []

        for quarter, start, end in quarters:
            deals = extractor.search_ma_deals(
                transaction_status=['Completed', 'Announced'],
                start_date=start,
                end_date=end,
                top=500
            )

            if not deals.empty:
                total_value = deals['TransactionValueIncludingNetDebtOfTarget'].sum()
                avg_value = deals['TransactionValueIncludingNetDebtOfTarget'].mean()
                deal_count = len(deals)
            else:
                total_value = 0
                avg_value = 0
                deal_count = 0

            quarterly_results.append({
                'Quarter': quarter,
                'Deal Count': deal_count,
                'Total Value ($M)': total_value,
                'Average Value ($M)': avg_value
            })

            print(f"\n{quarter}: {deal_count} deals, Total: ${total_value:.2f}M, Avg: ${avg_value:.2f}M")

        # Create summary DataFrame
        summary_df = pd.DataFrame(quarterly_results)
        print("\n" + "="*60)
        print("Quarterly Summary:")
        print(summary_df.to_string(index=False))

        # Export summary
        summary_df.to_csv('quarterly_ma_summary_2024.csv', index=False)
        print("\nSummary exported to quarterly_ma_summary_2024.csv")

    finally:
        extractor.close_session()


def example_public_to_private():
    """Example: Public-to-private transactions."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Public-to-Private Transactions")
    print("="*60)

    extractor = LSEGMAExtractor(session_type="desktop")

    try:
        extractor.open_session()

        # Find public companies being taken private
        p2p_deals = extractor.search_ma_deals(
            target_public_status='Public',
            transaction_status=['Completed', 'Pending'],
            start_date='2023-01-01',
            top=150
        )

        print(f"\nFound {len(p2p_deals)} public-to-private transactions")

        if not p2p_deals.empty:
            # Analyze by country
            country_breakdown = p2p_deals['TargetCountry'].value_counts()
            print("\nTop Countries for Public-to-Private Deals:")
            print(country_breakdown.head(10))

            # Analyze by transaction value
            print(f"\nTotal Transaction Value: ${p2p_deals['TransactionValueIncludingNetDebtOfTarget'].sum():.2f}M")

        # Export
        extractor.export_to_csv(p2p_deals, "public_to_private_deals.csv")

    finally:
        extractor.close_session()


def example_recent_pending_deals():
    """Example: Monitor recently announced pending deals."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Recently Announced Pending Deals")
    print("="*60)

    extractor = LSEGMAExtractor(session_type="desktop")

    try:
        extractor.open_session()

        # Get pending deals announced in last 30 days
        pending_deals = extractor.search_ma_deals(
            transaction_status=['Pending', 'Announced'],
            start_date='2024-10-23',  # Last 30 days from Nov 22, 2024
            select_fields=[
                'TransactionAnnouncementDate',
                'TargetCompanyName',
                'TargetCountry',
                'TargetRIC',
                'AcquirerCompanyName',
                'AcquirerCountry',
                'TransactionValueIncludingNetDebtOfTarget',
                'TransactionStatus',
                'DealSummary'
            ],
            top=100
        )

        print(f"\nFound {len(pending_deals)} pending deals announced in last 30 days")

        if not pending_deals.empty:
            # Sort by announcement date
            pending_deals_sorted = pending_deals.sort_values(
                'TransactionAnnouncementDate',
                ascending=False
            )

            print("\nMost Recent Deals:")
            print(pending_deals_sorted.head(10)[['TransactionAnnouncementDate',
                                                  'TargetCompanyName',
                                                  'AcquirerCompanyName',
                                                  'TransactionValueIncludingNetDebtOfTarget']])

        # Export
        extractor.export_to_csv(pending_deals, "recent_pending_deals.csv")

    finally:
        extractor.close_session()


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("LSEG M&A Data Extractor - Advanced Examples")
    print("="*70)
    print("\nNOTE: Make sure LSEG Workspace is running (Desktop Session)")
    print("      or update the session_type to 'platform' with credentials")
    print("="*70)

    # Run examples
    # Uncomment the examples you want to run:

    # example_tech_acquisitions()
    # example_cross_border_deals()
    # example_mega_deals()
    # example_quarterly_analysis()
    # example_public_to_private()
    example_recent_pending_deals()

    print("\n" + "="*70)
    print("Examples completed! Check the generated CSV files.")
    print("="*70)


if __name__ == "__main__":
    main()
