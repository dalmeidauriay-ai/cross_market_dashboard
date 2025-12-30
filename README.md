# Repository Structure
cross_market_dashboard/
├─ app/                          # Application Core
│  ├─ main.py                    # Entry point & Navigation logic
│  ├─ pages/                     # Dashboard Modules
│  │  ├─ p1_overview.py          # Global Market & Macro Snapshot
│  │  ├─ p2_stocks.py            # Equities Performance & Analytics
│  │  ├─ p3_fx.py                # Foreign Exchange Matrix & Trends
│  │  ├─ p4_rates.py             # Rates (FRED yields, OECD, US curve)
│  │  ├─ p5_commo.py             # Commodities, Ratios & Futures Curves
│  │
│  ├─ services/                  # Backend Logic
│  │  ├─ data_loader.py          # Data ingestion (CSV/API)
│  │  ├─ yf_client.py            # Yahoo Finance API Integration
│  │  ├─ fred_client.py          # Fred Integration
│  │  ├─ transforms.py           # Financial math & data cleaning
│  │  ├─ tickers_mapping.py      # Centralized asset dictionaries
│  │
├─ data/                         # Data Warehouse
│  ├─ processed/                 # Refreshed CSVs & Futures Chains
│  │  ├─ futures_curves/         # Individual commodity term structures
│  ├─ raw/                       # Dirty CSVs
│  ├─ test/                      # May use as path for test.py
│  │
├─ jobs/                         # Automation
│  ├─ refresh_data.py            # Automated ETL & Data Refresh engine
│
├─ README.md                     # Project documentation
├─ test.py                       # Play ground
└─ .gitignore                    # Prevents tracking of cache and local data


🌍 Cross-Market Macro Dashboard

A professional-grade financial terminal built with Streamlit and Python. This dashboard centralizes global market data, macro indicators, and futures term structures into a single, high-performance interface.
📂 Project Architecture

(Current structure matches your local files: app/pages/p1 through p5)
🚀 Key Features Implemented
1. Global Macro Terminal (Overview)

    Global Snapshot: Performance tracking for Americas, Europe, and Asia indices.

    Monetary Policy: Central bank rate tracker (Fed, ECB, BoE, etc.).

    Macro Pulse: Real-time GDP and Inflation (YoY) metrics.

    Cross-Asset Snapshot: Unified view of Gold, Oil, BTC, and Bond Yields.

2. Equity Analytics

    Performance Tables: Daily, Weekly, and YTD performance for global leaders.

    Stock Comparator: Interactive tool to compare stock returns vs. benchmarks with correlation and cumulative return plots.

3. FX Hub

    Relative Strength Matrix: A heat-mapped grid showing cross-currency strength.

    Trend Analysis: Historical time-series for major currency pairs.

4. Fixed Income & Yield Curves (Rates)

    U.S. Yield Curve: Dynamic visualization of the 2Y, 5Y, 10Y, and 30Y Treasury yields.

    OECD Comparison: Snapshot of 10Y Government Bond yields across major economies.

    Spread Analysis: Tracking yield evolution over time to identify curve flattening or inversion.

5. Commodities & Futures (Advanced)

    Macro Sentiment Ratios: Dr. Copper (Copper/Gold) and Gold/Silver ratios with independent date controls.

    Futures Forward Curves: Dynamic visualization of term structures (Contango vs. Backwardation) using automated futures chain stitching.

🛠️ Planned Enhancements (Roadmap)
📈 Phase 1: Advanced Analytics

    Overview Correlation Matrix: Develop a cross-asset correlation heatmap on the Overview page to link Equities, FX, and Commodities, identifying broad market trends.

    FX Volatility Insights: Implement a volatility surface or historical volatility chart in the FX Hub to assess market "nervousness."

⚙️ Phase 2: Data Optimization

    Commodity Data Expansion: Move beyond Yahoo Finance for Commodities by integrating more specialized providers (e.g., Quandl or EIA) for better historical depth.

    Enhanced Overview: Adding a "Macro Events" calendar or a correlation-based trend signal (e.g., Risk-On/Risk-Off meter).

🎨 Phase 3: Realistic UI Refinements

    Performance Optimization: Further refining the refresh_data.py job to handle larger datasets without slowing down the Streamlit UI.

    Global Styling: Finalizing a unified CSS theme across all 5 pages for a seamless "Terminal" feel.