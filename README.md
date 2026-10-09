# Hotel Booking Cancellation Analysis

**Question:** Which bookings are most likely to cancel, and what can the hotel do to reduce lost revenue?

**Stack:** Python (pandas, NumPy, scikit-learn, joblib, sqlite3) · SQL (SQLite) · Power BI · Node.js (Express, Chart.js)

## Run it
```bash
pip install pandas numpy scikit-learn joblib
python3 pipeline.py        # clean -> SQLite -> SQL analysis -> CSVs for Power BI -> train model
npm install
npm start                  # open http://localhost:3000
```

## Structure
| File | Purpose |
|---|---|
| `generate_data.py` | Creates sample data with the Kaggle "Hotel Booking Demand" columns |
| `pipeline.py` | `clean()`, `run_sql()`, `train()` and the main flow |
| `sql/analysis.sql` | 8 named SQL queries (KPIs, lead time, deposit, channel, month, country, risky combos) |
| `predict.py` | `predict()` scores one booking, called by Node.js |
| `server.js` | Express API: `/api/results`, `/api/predict`, `/api/refresh` |
| `public/index.html` | Dashboard UI |
| `powerbi/` | Exported CSVs + step-by-step Power BI guide with DAX |

## Use the real dataset
Download `hotel_bookings.csv` from Kaggle ("Hotel Booking Demand"), put it in `data/`, and rerun `python3 pipeline.py`.
Then update the findings and numbers in your resume bullets and README from the new results.
