"""Creates a synthetic dataset with the SAME columns as Kaggle's 'Hotel Booking Demand'.
To use the real data: download hotel_bookings.csv from Kaggle and save it as data/hotel_bookings.csv
(the pipeline skips generation if that file already exists)."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
N = 30000
hotel = rng.choice(["City Hotel", "Resort Hotel"], N, p=[.66, .34])
lead = np.clip(rng.gamma(1.6, 75, N), 0, 600).astype(int)
deposit = rng.choice(["No Deposit", "Non Refund", "Refundable"], N, p=[.87, .12, .01])
segment = rng.choice(["Online TA", "Offline TA/TO", "Direct", "Corporate", "Groups"], N, p=[.47, .20, .13, .10, .10])
cust = rng.choice(["Transient", "Contract", "Transient-Party", "Group"], N, p=[.75, .04, .2, .01])
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
month = rng.choice(months, N, p=np.array([5,6,8,9,9,9,11,12,9,7,5,5])/95)
country = rng.choice(["PRT","GBR","FRA","ESP","DEU","IRL","ITA","USA","IND"], N, p=[.34,.12,.11,.09,.08,.05,.05,.08,.08])
repeat = (rng.random(N) < .04).astype(int)
prev_c = np.where(rng.random(N) < .06, rng.integers(1, 4, N), 0)
wk = rng.integers(0, 6, N); we = rng.integers(0, 4, N)
adr = np.clip(rng.normal(100, 35, N) + (hotel == "Resort Hotel") * 8 + np.isin(month, ["July","August"]) * 25, 20, 400).round(2)
# hidden "true" cancellation logic (this is what the analysis should discover)
z = (-2.5 + 0.008*lead + (segment == "Online TA")*0.7 - (segment == "Direct")*0.6 - (segment == "Corporate")*0.8
     + (deposit == "Non Refund")*3.0 - repeat*1.2 + prev_c*0.8 + (hotel == "City Hotel")*0.3 + (country == "PRT")*0.5)
canceled = (rng.random(N) < 1/(1+np.exp(-z))).astype(int)
y = rng.choice([2015, 2016, 2017], N, p=[.2, .45, .35])
df = pd.DataFrame(dict(hotel=hotel, is_canceled=canceled, lead_time=lead, arrival_date_year=y, arrival_date_month=month,
    stays_in_weekend_nights=we, stays_in_week_nights=wk, adults=rng.choice([1,2,3], N, p=[.2,.75,.05]),
    children=rng.choice([0,1,2], N, p=[.92,.05,.03]), country=country, market_segment=segment,
    is_repeated_guest=repeat, previous_cancellations=prev_c, deposit_type=deposit,
    customer_type=cust, adr=adr))
# add a few dirty rows to make the cleaning step meaningful
df.loc[rng.choice(N, 150, replace=False), "country"] = None
df.loc[rng.choice(N, 60, replace=False), ["adults","children"]] = 0
df.loc[rng.choice(N, 20, replace=False), "adr"] = -5
df = pd.concat([df, df.sample(200, random_state=1)])   # duplicates
df.to_csv("data/hotel_bookings.csv", index=False)
print("saved", df.shape)
