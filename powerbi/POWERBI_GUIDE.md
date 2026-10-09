# Building the Power BI dashboard (about 30 minutes)

Power BI files (.pbix) can only be made inside Power BI Desktop, so this guide gives you the exact steps.
All data is already exported to `powerbi/data/` by `python3 pipeline.py`.

## 1. Load data
Home > Get data > Text/CSV > `powerbi/data/hotel_clean.csv` > Load.
(Optional: also load `by_lead_time.csv`, `by_segment.csv`, etc. if you prefer ready-made summaries.)
Or connect to the SQLite DB with the SQLite ODBC driver: `output/hotel.db`, table `hotel_clean`.

## 2. Power Query (Transform data)
- Check that `is_canceled`, `lead_time`, `adr`, `revenue` are numbers.
- Add a column > Conditional column: `lead_group` = 0-30 / 31-90 / 91-180 / 180+ based on `lead_time`.
- Sort `arrival_date_month` by month number: add an index column or a small Month table (January=1 ... December=12), then Sort by column.

## 3. DAX measures (Modeling > New measure)
```
Total Bookings   = COUNTROWS(hotel_clean)
Cancellations    = SUM(hotel_clean[is_canceled])
Cancellation Rate = DIVIDE([Cancellations], [Total Bookings])
Revenue Lost     = CALCULATE(SUM(hotel_clean[revenue]), hotel_clean[is_canceled] = 1)
Potential Revenue = SUM(hotel_clean[revenue])
Revenue Lost % = DIVIDE([Revenue Lost], [Potential Revenue])
Avg Lead Time (Cancelled) = CALCULATE(AVERAGE(hotel_clean[lead_time]), hotel_clean[is_canceled] = 1)
```

## 4. Page layout
| Area | Visual | Fields |
|---|---|---|
| Top row | 4 Card visuals | Total Bookings, Cancellation Rate, Revenue Lost, Revenue Lost % |
| Left | Clustered column | Axis: lead_group, Values: Cancellation Rate |
| Middle | Bar chart | Axis: market_segment, Values: Cancellation Rate |
| Right | Column chart | Axis: deposit_type, Values: Cancellation Rate |
| Bottom left | Line / column | Axis: arrival_date_month, Values: Revenue Lost |
| Bottom right | Matrix | Rows: market_segment, Columns: lead_group, Values: Cancellation Rate (add conditional formatting > background color) |
| Slicers | Dropdown | hotel, arrival_date_year, country |

## 5. Finish
Add a title, use 2 to 3 consistent colors, turn on Format > Edit interactions so slicers filter every chart.
Take screenshots (or publish to Power BI Service) and add them to your GitHub README.
