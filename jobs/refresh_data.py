# jobs/refresh_data.py

import os
import pandas as pd
from datetime import datetime, timedelta

# ---------------------------------------------------------
# Imports from services
# ---------------------------------------------------------
from app.services.data_loader import (
    load_fx_matrix,
    load_us_yields,
    load_oecd_yields,
    refresh_fx_history,   # ✅ new helper replaces build_fx_history
    refresh_stock_history,
    refresh_stock_snapshot,
    refresh_indices_snapshot,
    refresh_indices_history,
    refresh_monetary_policy,
    refresh_cross_asset_snapshot,
    refresh_commodity_history,
    refresh_commodity_futures,
)

TRACKER_PATH = os.path.join("data", "processed", "refresh_tracker.csv")


# =========================================================
# Load & Save tracker
# =========================================================
def load_tracker() -> pd.DataFrame:
    tracker = pd.read_csv(TRACKER_PATH)
    # Clean up any stray spaces or semicolons in column names
    tracker.columns = tracker.columns.str.strip().str.replace(";", "")
    # Parse the last_update column into proper datetimes
    tracker["last_update"] = pd.to_datetime(tracker["last_update"])
    # Use csv_name as the index
    tracker = tracker.set_index("csv_name")
    return tracker


def save_tracker(tracker: pd.DataFrame):
    tracker.to_csv(TRACKER_PATH)


# =========================================================
# Refresh rules
# =========================================================
def should_refresh(last_update: pd.Timestamp, mode: str) -> bool:
    """
    Decide whether to refresh based on mode:
    - mode="historical": refresh if last update < today
    - mode="snapshot": refresh if last update > 1h ago
    """
    now = datetime.now()

    if pd.isna(last_update):
        return True

    if mode == "historical":
        return last_update.date() < now.date()
    elif mode == "snapshot":
        return (now - last_update.to_pydatetime()) > timedelta(hours=1)
    else:
        return False


# =========================================================
# Main refresh orchestrator
# =========================================================
def run_refresh():
    tracker = load_tracker()

    # Historical datasets
    if should_refresh(tracker.loc["FX_historical.csv", "last_update"], "historical"):
        print("Refreshing FX historical...")
        refresh_fx_history()  # ✅ cleaner call
        tracker.loc["FX_historical.csv", "last_update"] = datetime.now()

    if should_refresh(tracker.loc["stocks_history.csv", "last_update"], "historical"):
        print("Refreshing stocks historical...")
        refresh_stock_history()
        tracker.loc["stocks_history.csv", "last_update"] = datetime.now()

    if should_refresh(tracker.loc["indices_historical.csv", "last_update"], "historical"):
        print("Refreshing indices historical...")
        refresh_indices_history()
        tracker.loc["indices_historical.csv", "last_update"] = datetime.now()

    if should_refresh(tracker.loc["us_yields.csv", "last_update"], "historical"):
        print("Refreshing US yields historical...")
        load_us_yields(force_refresh=True)
        tracker.loc["us_yields.csv", "last_update"] = datetime.now()

    if should_refresh(tracker.loc["oecd_yields.csv", "last_update"], "historical"):
        print("Refreshing OECD yields historical...")
        load_oecd_yields(force_refresh=True)
        tracker.loc["oecd_yields.csv", "last_update"] = datetime.now()


    # Snapshot datasets
    if should_refresh(tracker.loc["FX_rate_matrix.csv", "last_update"], "snapshot"):
        print("Refreshing FX matrix snapshot...")
        load_fx_matrix(force_refresh=True)
        tracker.loc["FX_rate_matrix.csv", "last_update"] = datetime.now()


    if should_refresh(tracker.loc["stocks_snapshot.csv", "last_update"], "snapshot"):
        print("Refreshing stocks snapshot...")
        refresh_stock_snapshot()
        tracker.loc["stocks_snapshot.csv", "last_update"] = datetime.now()

    if should_refresh(tracker.loc["indices_snapshot.csv", "last_update"], "snapshot"):
        print("Refreshing indices snapshot...")
        refresh_indices_snapshot()
        tracker.loc["indices_snapshot.csv", "last_update"] = datetime.now()

    # Cross-Asset Snapshot refresh
    if should_refresh(tracker.loc["cross_asset_snapshot.csv", "last_update"] if "cross_asset_snapshot.csv" in tracker.index else None, "snapshot"):
        print("Refreshing Cross-Asset Snapshot...")
        refresh_cross_asset_snapshot()
        tracker.loc["cross_asset_snapshot.csv", "last_update"] = datetime.now()
    
    # Monetary Policy (Weekly refresh is sufficient)
    # We use a dummy CSV name "monetary_policy_check" to track this task in your tracker CSV
    if should_refresh(tracker.loc["monetary_policy_check", "last_update"] if "monetary_policy_check" in tracker.index else None, "weekly"):
        print("Refreshing Monetary Policy Data...")
        refresh_monetary_policy()
        tracker.loc["monetary_policy_check", "last_update"] = datetime.now()

    # ---------------------------------------------------------
    # Commodities Refresh (Daily)
    # ---------------------------------------------------------
    # We check one representative file (e.g., hist_metals.csv)
    if should_refresh(tracker.loc["hist_metals.csv", "last_update"] if "hist_metals.csv" in tracker.index else None, "daily"):
        print("Refreshing Commodity History...")
        refresh_commodity_history()
        # Update tracker for all groups
        tracker.loc["hist_metals.csv", "last_update"] = datetime.now()
        tracker.loc["hist_energy.csv", "last_update"] = datetime.now()
        tracker.loc["hist_agriculture.csv", "last_update"] = datetime.now()

    # Futures Curves Refresh (Daily)
    # We track this with a dummy key since it generates many files
    if should_refresh(tracker.loc["futures_curves_check", "last_update"] if "futures_curves_check" in tracker.index else None, "daily"):
        print("Refreshing Commodity Futures Curves...")
        refresh_commodity_futures()
        tracker.loc["futures_curves_check", "last_update"] = datetime.now()

    # Save tracker
    save_tracker(tracker)
    print("✅ Refresh complete")