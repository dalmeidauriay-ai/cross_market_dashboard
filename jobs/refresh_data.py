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
    refresh_fx_history,
    refresh_stock_history,
    refresh_stock_snapshot,
    refresh_indices_snapshot,
    refresh_indices_history,
    refresh_monetary_policy,
    refresh_cross_asset_snapshot,
    refresh_commodity_history,
    refresh_commodity_futures,
)

# Ensure paths are absolute relative to the project root
BASE_DIR = os.getcwd()
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
FUTURES_DIR = os.path.join(PROCESSED_DIR, "futures_curves")
TRACKER_PATH = os.path.join(PROCESSED_DIR, "refresh_tracker.csv")

# =========================================================
# Load & Save tracker
# =========================================================
def load_tracker() -> pd.DataFrame:
    # ROBUST FIX: Create directory if missing
    os.makedirs(FUTURES_DIR, exist_ok=True)
    
    if not os.path.exists(TRACKER_PATH):
        print("DEBUG: Tracker not found. Creating a fresh tracker...")
        # Create an empty tracker with the required structure
        columns = ["csv_name", "last_update"]
        df = pd.DataFrame(columns=columns).set_index("csv_name")
        return df

    tracker = pd.read_csv(TRACKER_PATH)
    tracker.columns = tracker.columns.str.strip().str.replace(";", "")
    tracker["last_update"] = pd.to_datetime(tracker["last_update"])
    tracker = tracker.set_index("csv_name")
    return tracker

def save_tracker(tracker: pd.DataFrame):
    tracker.to_csv(TRACKER_PATH)
    print(f"SUCCESS: Tracker saved to {TRACKER_PATH}")

# =========================================================
# Refresh rules
# =========================================================
def should_refresh(tracker, csv_name, mode) -> bool:
    now = datetime.now()
    
    # If key doesn't exist in tracker, we MUST refresh
    if csv_name not in tracker.index:
        return True
        
    last_update = tracker.loc[csv_name, "last_update"]
    if pd.isna(last_update):
        return True

    if mode == "historical" or mode == "daily":
        return last_update.date() < now.date()
    elif mode == "snapshot":
        return (now - last_update.to_pydatetime()) > timedelta(hours=1)
    elif mode == "weekly":
        return (now - last_update.to_pydatetime()) > timedelta(days=7)
    return False

# =========================================================
# Main refresh orchestrator
# =========================================================
def run_refresh():
    print(f"DEBUG: Starting refresh in {BASE_DIR}")
    tracker = load_tracker()

    # Define tasks: (csv_name, refresh_func, mode)
    tasks = [
        ("FX_historical.csv", refresh_fx_history, "historical"),
        ("stocks_history.csv", refresh_stock_history, "historical"),
        ("indices_historical.csv", refresh_indices_history, "historical"),
        ("us_yields.csv", lambda: load_us_yields(force_refresh=True), "historical"),
        ("oecd_yields.csv", lambda: load_oecd_yields(force_refresh=True), "historical"),
        ("FX_rate_matrix.csv", lambda: load_fx_matrix(force_refresh=True), "snapshot"),
        ("stocks_snapshot.csv", refresh_stock_snapshot, "snapshot"),
        ("indices_snapshot.csv", refresh_indices_snapshot, "snapshot"),
        ("cross_asset_snapshot.csv", refresh_cross_asset_snapshot, "snapshot"),
        ("monetary_policy_check", refresh_monetary_policy, "weekly"),
        ("hist_metals.csv", refresh_commodity_history, "daily"),
        ("futures_curves_check", refresh_commodity_futures, "daily")
    ]

    for csv_name, func, mode in tasks:
        if should_refresh(tracker, csv_name, mode):
            print(f"Refreshing: {csv_name}...")
            try:
                func()
                tracker.loc[csv_name, "last_update"] = datetime.now()
                # Special case for commodities which update multiple files
                if csv_name == "hist_metals.csv":
                    tracker.loc["hist_energy.csv", "last_update"] = datetime.now()
                    tracker.loc["hist_agriculture.csv", "last_update"] = datetime.now()
            except Exception as e:
                print(f"ERROR refreshing {csv_name}: {e}")

    # Save tracker
    save_tracker(tracker)
    print("✅ Refresh complete. Files should be ready for commit.")

if __name__ == "__main__":
    run_refresh()