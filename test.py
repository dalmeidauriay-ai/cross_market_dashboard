# ---------------------------------------------------------
# Test script: initialize stocks data
# ---------------------------------------------------------
# Responsibility: Run once to fetch and save both
# historical and snapshot CSVs under data/processed.
# ---------------------------------------------------------

import pandas as pd
from app.services.data_loader import refresh_stock_history, load_stock_snapshot

def main():
    # Refresh historical dataset (all tickers, long-term)
    history_df = refresh_stock_history(start_date="2010-01-01")
    print("✅ Stocks historical data refreshed and saved to data/processed/stocks_history.csv")
    print(history_df.head())

    # Refresh snapshot dataset (current year, metrics)
    snapshot_df = load_stock_snapshot(force_refresh=True)
    print("✅ Stocks snapshot data refreshed and saved to data/processed/stocks_snapshot.csv")
    print(snapshot_df.head())

if __name__ == "__main__":
    main()