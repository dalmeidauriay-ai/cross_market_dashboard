# Repository Structure
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




# Cross-Market Dashboard - Storyboard and Framework

✅ 1. Project Setup & Structure
- [x] Organize repo with clear folders (app/, data/, jobs/, notebooks/)
- [x] Create main.py as entry point
- [ ] Add reusable components/ (charts, KPIs, layouts)
- [ ] Add config/ for constants and style settings
- [ ] Build services/ for data access (APIs, loaders)

✅ 2. Navigation & Layout
- [x] Implement top ribbon navigation with buttons
- [ ] Remove Streamlit’s default sidebar page list
- [ ] Sidebar reserved for slicers/filters (per page)

✅ 3. Pages (Big Themes)
3.1 Overview
- [x] Create p1_overview.py
- [ ] Add tabs: Global Indexes, Macro Indicators, Commodities, FX Matrix
- [ ] Populate with charts and KPIs
3.2 Equities
- [ ] Sidebar slicer: stock ticker, index, sector
- [ ] Time series plots
- [ ] Sector performance heatmap
- [ ] Valuation metrics
3.3 FX
- [ ] Sidebar slicer: currency pair, timeframe
- [ ] FX spot & forward curves
- [ ] Volatility surface
- [ ] Correlation matrix
3.4 Rates
- [ ] Sidebar slicer: country, maturity
- [ ] Yield curves
- [ ] Spread analysis
- [ ] Central bank policy tracker
3.5 Commodities
- [ ] Sidebar slicer: commodity type (oil, gold, wheat, etc.)
- [ ] Price time series
- [ ] Supply/demand indicators
- [ ] Futures curve
3.6 ETFs
- [ ] Sidebar slicer: ETF ticker, asset class
- [ ] Performance vs benchmark
- [ ] Holdings breakdown
- [ ] Flows analysis
3.7 Options & Volatility
- [ ] Sidebar slicer: underlying asset, expiry
- [ ] Implied vol surface
- [ ] Skew analysis
- [ ] Option greeks dashboard
3.8 Alternatives
- [ ] Sidebar slicer: asset type (PE, RE, crypto, etc.)
- [ ] Performance indices
- [ ] Risk/return metrics
- [ ] Allocation trends

✅ 4. Data Layer
- [ ] Define data sources (APIs, CSV, DB)
- [ ] Build loaders in services/
- [ ] Add transformation utilities
- [ ] Implement caching for performance

✅ 5. Components
- [ ] Reusable chart functions (line, bar, scatter, heatmap)
- [ ] KPI cards (returns, vol, Sharpe ratio, drawdown)
- [ ] Layout helpers (tabs, grids, styled tables)

✅ 6. Jobs & Automation
- [ ] Scheduled data refresh (daily/weekly)
- [ ] ETL scripts in jobs/
- [ ] Logging & error handling

✅ 7. Deployment
- [ ] Local dev with Streamlit
- [ ] Deploy to Streamlit Cloud / internal server
- [ ] Optional: Dockerize for portability
- [ ] CI/CD pipeline (future)

✅ 8. Future Enhancements
- [ ] User authentication
- [ ] Export to PDF/Excel
- [ ] Interactive backtesting module
- [ ] ML models for forecasting
