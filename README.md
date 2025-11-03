📂 Repository Structure

cross_market_dashboard/
├─ app/                          # Main application code
│  ├─ main.py                    # Entry point (Streamlit multipage navigation)
│  ├─ pages/                     # Each dashboard page
│  │  ├─ overview.py             # Page 1: Global snapshot (indexes, macro, commo, FX matrix)
│  │  ├─ equities.py             # Page 2: Equities (stocks vs indexes)
│  │  ├─ fx.py                   # Page 3: FX (matrix + time series)
│  │  ├─ rates.py                # Page 4: Rates (FRED yields, OECD, US curve)
│  │  ├─ commodities.py          # Page 5: Commodities (oil, gold, wheat, etc.)
│  │  ├─ etfs.py                 # Page 6: ETFs (sector & regional comparisons)
│  │  ├─ options.py              # Page 7: Options & Volatility (VIX, vol indices)
│  │  ├─ alternatives.py         # Page 8: Alternatives (crypto, real estate, etc.)
│  │
│  ├─ components/                # Reusable UI + plotting components
│  │  ├─ charts.py               # Generic plotting (line, bar, heatmap)
│  │  ├─ snapshots.py            # Snapshot visuals (yield curve, OECD barh, FX matrix styling)
│  │  ├─ widgets.py              # Sidebar controls (date range, selectors, filters)
│  │
│  ├─ services/                  # Data access + processing
│  │  ├─ data_loader.py          # Unified load (CSV or API)
│  │  ├─ fred_client.py          # FRED fetch logic
│  │  ├─ yf_client.py            # Yahoo Finance fetch logic
│  │  ├─ transforms.py           # Cleaning, normalization, returns, % changes
│  │
│  ├─ config/                    # Configuration files
│  │  ├─ symbols.py              # Tickers and friendly names per asset class
│  │  ├─ style.py                # Fonts, colors, themes
│
├─ data/                         # Local data cache
│  ├─ raw/                       # Raw CSVs (direct downloads)
│  ├─ processed/                 # Cleaned & aligned datasets
│
├─ notebooks/                    # Experiments, prototyping
│
├─ jobs/                         # Scheduled refresh tasks
│  ├─ refresh_data.py            # Script to update data daily
│
├─ tests/                        # Unit tests (optional, for services/transforms)
│
├─ README.md                     # Project overview
├─ .gitignore                    # Ignore data/, .env, cache files
├─ .env                          # API keys (FRED, etc.) — not committed



