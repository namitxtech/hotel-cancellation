"""End-to-end pipeline: load -> clean (pandas) -> store (SQLite) -> analyse (SQL) -> export (Power BI) -> model (sklearn)."""
import os, re, json, sqlite3, subprocess, sys
import numpy as np, pandas as pd, joblib
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RAW, DB = "data/hotel_bookings.csv", "output/hotel.db"
NUM = ["lead_time", "adr", "total_nights", "previous_cancellations", "is_repeated_guest"]
CAT = ["hotel", "deposit_type", "market_segment", "customer_type"]

def clean(df):
    """Python function 1: data cleaning. Returns clean df + a log of what was removed."""
    log = {"raw_rows": len(df)}
    df = df.drop_duplicates();                         log["duplicates_removed"] = log["raw_rows"] - len(df)
    df["country"] = df["country"].fillna("Unknown");   df["children"] = df["children"].fillna(0)
    n = len(df); df = df[(df.adults + df.children) > 0]; log["zero_guest_removed"] = n - len(df)
    n = len(df); df = df[df.adr > 0];                  log["bad_price_removed"] = n - len(df)
    df["total_nights"] = df.stays_in_weekend_nights + df.stays_in_week_nights
    n = len(df); df = df[df.total_nights > 0];         log["zero_night_removed"] = n - len(df)
    df["revenue"] = (df.adr * df.total_nights).round(2)
    log["clean_rows"] = len(df)
    return df.reset_index(drop=True), log

def run_sql(con, path="sql/analysis.sql"):
    """Python function 2: runs every named query in the .sql file and returns DataFrames."""
    text = open(path).read()
    out = {}
    for name, q in re.findall(r"-- name: (\w+)\n(.*?);", text, re.S):
        out[name] = pd.read_sql_query(q, con)
    return out

def train(df):
    """Python function 3: trains logistic regression and returns metrics."""
    X, y = df[NUM + CAT], df["is_canceled"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    pre = ColumnTransformer([("num", StandardScaler(), NUM), ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])
    model = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
    p = model.predict_proba(Xte)[:, 1]; pred = (p >= .5).astype(int)
    m = dict(accuracy=round(accuracy_score(yte, pred), 3), precision=round(precision_score(yte, pred), 3),
             recall=round(recall_score(yte, pred), 3), roc_auc=round(roc_auc_score(yte, p), 3))
    names = model.named_steps["pre"].get_feature_names_out()
    coef = pd.Series(model.named_steps["clf"].coef_[0], index=names).sort_values()
    m["top_risk_factors"] = [{"feature": k.split("__")[1], "weight": round(v, 2)} for k, v in coef.tail(6)[::-1].items()]
    m["top_protective_factors"] = [{"feature": k.split("__")[1], "weight": round(v, 2)} for k, v in coef.head(4).items()]
    joblib.dump(model, "output/model.joblib")
    return m

def main():
    os.makedirs("output", exist_ok=True)
    if not os.path.exists(RAW):
        subprocess.run([sys.executable, "generate_data.py"], check=True)
    df, log = clean(pd.read_csv(RAW))
    con = sqlite3.connect(DB)
    df.to_sql("hotel_clean", con, if_exists="replace", index=False)
    res = run_sql(con)
    metrics = train(df)
    # JSON for the Node.js dashboard
    payload = {k: v.to_dict("records") for k, v in res.items()}
    payload["cleaning_log"], payload["model_metrics"] = log, metrics
    json.dump(payload, open("output/results.json", "w"), indent=2)
    # CSVs for Power BI
    os.makedirs("powerbi/data", exist_ok=True)
    df.to_csv("powerbi/data/hotel_clean.csv", index=False)
    for k, v in res.items(): v.to_csv(f"powerbi/data/{k}.csv", index=False)
    print(json.dumps(log)); print(json.dumps(metrics, indent=1)); print(res["overall_kpis"].to_string(index=False))

if __name__ == "__main__":
    main()
