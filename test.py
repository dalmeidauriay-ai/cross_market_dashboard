import yfinance as yf
import pandas as pd
import os

# Define output directory
OUTPUT_DIR = os.path.join("data", "test")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define Assets
# Note: Corn changed to 'C=F' for better historical data depth
ASSETS = {
    "Metals": {
        "Gold": "GC=F", 
        "Silver": "SI=F", 
        "Copper": "HG=F", 
        "Platinum": "PL=F", 
        #"Aluminum": "ALI=F", # No Yahoo ticker found
        "Steel HRC": "HRC=F",
        #"Zinc": "ZNC=F", # No Yahoo ticker found
        "Nickel": "NIKL", #Sprott Nickel Miners ETF (NIKL)
        "Palladium": "PA=F",
        #"Cobalt": "COB=F", # No Yahoo ticker found
        "Lithum": "LIT" # Global X Lithium & Battery Tech ETF (LIT)
    },
    "Energy": {
        "Crude Oil WTI": "CL=F", 
        "Brent Oil": "BZ=F", 
        "Natural Gas": "NG=F", 
        "Heating Oil": "HO=F", 
        "RBOB Gasoline": "RB=F",
        #"Low Sulphur Gasoil": "G=F", # No Yahoo ticker found
        # "Propane": "PB=F", # No Yahoo ticker found
        "Coal": "QG=F",
        "Uranium": "SRUUF", # Sprott Uranium Miners ETF (SRUUF)
        "Ethanol": "EH=F"
    },
    "Agri": {
        "Wheat": "ZW=F", 
        "Corn": "XC=F", 
        "Soybeans": "ZS=F", 
        "Cocoa": "CC=F", 
        "Coffee": "KC=F", 
        "Orange Juice": "OJ=F",
        "Sugar": "SB=F",
        "Cotton": "CT=F",
        "Live Cattle": "LE=F",
        "Rice": "ZR=F",
        #"Rubber": "RR=F", # No Yahoo ticker found
        #"Palm Oil": "PO=F", # No Yahoo ticker found
    },
    "Benchmarks": {
        "Dollar Index (DXY)": "DX-Y.NYB", 
        "10Y US Yield": "^TNX"
    }
}
START_DATE = "2010-01-01"

def fetch_and_process():
    for group, tickers in ASSETS.items():
        print(f"\n--- Fetching {group} ---")
        group_df = pd.DataFrame()
        
        for name, ticker in tickers.items():
            print(f"Downloading {name} ({ticker})...")
            # Fetch data from 2010
            data = yf.download(ticker, start=START_DATE, progress=False)
            
            if not data.empty:
                # Yahoo Finance can return multi-index or single index depending on version
                # We prioritize 'Adj Close', fallback to 'Close'
                col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
                group_df[name] = data[col]
        
        if not group_df.empty:
            # 1. Sort by date
            group_df.sort_index(inplace=True)
            
            # 2. Forward Fill NAs (use previous day's price)
            group_df = group_df.ffill()
            
            # 3. Save to CSV
            file_name = f"{group.lower().replace(' ', '_')}_hist.csv"
            save_path = os.path.join(OUTPUT_DIR, file_name)
            group_df.to_csv(save_path)
            print(f"✅ Saved & Filled {group} to {save_path}")

if __name__ == "__main__":
    fetch_and_process()