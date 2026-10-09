"""Python function 4: scores one booking. Called by Node.js:  python3 predict.py '{"lead_time":200,...}'"""
import sys, json, joblib, pandas as pd
def predict(b):
    model = joblib.load("output/model.joblib")
    row = pd.DataFrame([{
        "lead_time": float(b["lead_time"]), "adr": float(b["adr"]), "total_nights": float(b["total_nights"]),
        "previous_cancellations": float(b.get("previous_cancellations", 0)),
        "is_repeated_guest": int(b.get("is_repeated_guest", 0)), "hotel": b["hotel"],
        "deposit_type": b["deposit_type"], "market_segment": b["market_segment"],
        "customer_type": b.get("customer_type", "Transient")}])
    p = float(model.predict_proba(row)[0, 1])
    level = "High" if p >= .6 else "Medium" if p >= .35 else "Low"
    advice = {"High": "Ask for a deposit or send a reconfirmation reminder; consider this room in overbooking.",
              "Medium": "Send a reminder 7 days before arrival.",
              "Low": "No action needed."}[level]
    return {"probability": round(p, 3), "risk": level, "advice": advice}
if __name__ == "__main__":
    print(json.dumps(predict(json.loads(sys.argv[1]))))
