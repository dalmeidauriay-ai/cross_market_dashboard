# Cross-Market Dashboard

A professional financial terminal designed for global macro analysis, smart equity benchmarking, and cross-asset relative value tracking.

## 🚀 Repository Structure

├─ app/                          # Main application code
│  ├─ main.py                    # Entry point (Unified Navigation)
│  ├─ pages/                     
│  │  ├─ p1_overview.py          # THE COMMAND CENTER: Global Indices, Macro & News
│  │  ├─ p2_stocks.py            # SMART EQUITIES: Stock vs. Regional Benchmarks
│  │  ├─ p3_fx.py                # FX HUB: Spot Matrix & Time-Series analysis
│  │  ├─ p4_rates.py             # RATES: Cross-country yield analysis & US Curve
│  │  └─ p5_commodities.py       # (In Progress) Global Resources
│  ├─ services/                  
│  │  ├─ tickers_mapping.py      # The "Brain": Multi-asset ticker dictionaries
│  │  ├─ data_loader.py          # Unified Loading & Smart Normalization logic
│  │  ├─ transforms.py           # Quantitative utilities (returns, vol, scaling)
│  │  ├─ fred_client.py          # FRED API interface for macro series
│  │  └─ yf_client.py            # Yahoo Finance fetching with local caching
├─ data/                         # Persistent CSV storage (Local Cache)
├─ jobs/                         # Daily ETL & Data Refresh scripts
└─ README.md

## 🛠 Features (Phase 1 Complete)

### 1. Global Command Center (Overview)
- **Triple-Region Index Tracking:** Real-time snapshots of Americas, Europe, and Asia.
- **Economic Pulse:** Live GDP growth, Inflation data (FRED integration), and other key macro indicator.
- **Global News Stream:** : Integrated feed of the top 50 financial headlines with a scrollable interface for rapid market intake.

### 2. Smart Equity Benchmarking
- **Context-Aware Comparison:** Automatically detects stock origin (e.g., LVMH -> FR) and restricts benchmarks to relevant local indices (CAC 40, 10Y France) and global peers (Euro Stoxx 50).
- **Single Stock return, vol windows analysis:** Detailed breakdown of total returns and annualized volatility across custom rolling windows (1M, 3M, YTD, 1Y).
- **Multi-Asset perfomance comparator:** Advanced charting with 100-base normalization for relative strength analysis. Includes an expanded correlation matrix assessing stocks against global indices.

### 3. FX Analysis Hub
- **Currency Matrix:** Real-time spot rates for major G10 pairs.
- **Time-Series Tracking:** Time-series analysis for currency pairs to identify long-term trends and volatility.
- *[To-Do]*: Implement real-time currency strength heatmaps and forward curve projections.

### 4. Rates & Fixed Income
- **Yield Curve Visualizer:** Dynamic plotting of the US Treasury curve (2Y to 30Y).
- **Cross-Country Analysis:** Comparative tool for sovereign yields (US, France, Germany, Japan).
- **Monetary Policy Tracker:** Central bank fund rates (Fed, ECB) vs. current inflation.

## 📈 Roadmap
- [ ] **Commodity Hub:** Full integration for Gold, Brent, Industrial Metals, and Rare Earth elements
- [ ] **Advanced Volatility:** VIX/VSTOXX term structure analysis and implied volatility surface modeling.
- [ ] **Risk Reporting:**  Automated Sharpe Ratio and Maximum Drawdown reporting for custom portfolios.
