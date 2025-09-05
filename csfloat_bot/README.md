CSFloat Profit Bot (Educational)

Overview

- Automated scanner and opportunity finder for CSFloat Market using a headless browser client.
- Pluggable pricing and strategy modules (bandits + dynamic relist pricing) with strict risk controls.
- Works in dry-run by default; live buy actions require manual review and may violate site Terms if misused.

Important

- This repository is for educational and research purposes only. Use responsibly and comply with CSFloat's Terms of Service and your local laws.
- Do not bypass anti-bot measures, rate limits, or CAPTCHAs. The client here only uses a persistent cookie session that you create by logging in once.
- Live purchases are disabled by default (dry-run). Enable at your own risk.

Quick Start

1) Python 3.11+
2) Install deps:
   pip install -r requirements.txt
   playwright install chromium
3) Run a dry scan:
   python -m csfloat_bot.cli run --dry-run --budget 50 --headless
4) First run will open a browser page for you to log in to CSFloat. Cookies are stored under ~/.csfloat/cookies.json by default.

Features

- Budget-aware position sizing and max open positions
- Pluggable strategy: contextual bandit (Thompson Sampling) over categories and price tiers
- Price estimation via heuristics, with extension points to external feeds
- Risk controls: max hold duration, minimum ROI and spread thresholds, stop-out on adverse drift
- CLI with rich logging, dry-run and live modes

Configuration

See csfloat_bot/config.py for defaults. Override flags via CLI.

Notes on CSFloat API

- CSFloat does not publish an official public Market API for buy actions. This bot uses a headless browser to navigate pages and read publicly available listing data while you are logged in.
- If CSFloat publishes official client APIs, prefer those instead of scraping.

Disclaimer

Nothing here guarantees profits. Markets change, liquidity varies, and execution may fail. Use at your own risk.

