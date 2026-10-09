-- name: overall_kpis
SELECT COUNT(*) AS total_bookings, SUM(is_canceled) AS cancellations,
       ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate,
       ROUND(SUM(CASE WHEN is_canceled=1 THEN revenue ELSE 0 END),0) AS revenue_lost,
       ROUND(SUM(revenue),0) AS potential_revenue
FROM hotel_clean;
-- name: by_lead_time
SELECT CASE WHEN lead_time<=30 THEN '0-30' WHEN lead_time<=90 THEN '31-90'
            WHEN lead_time<=180 THEN '91-180' ELSE '180+' END AS label,
       COUNT(*) AS bookings, ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate
FROM hotel_clean GROUP BY label ORDER BY MIN(lead_time);
-- name: by_deposit
SELECT deposit_type AS label, COUNT(*) AS bookings, ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate
FROM hotel_clean GROUP BY deposit_type ORDER BY cancel_rate DESC;
-- name: by_segment
SELECT market_segment AS label, COUNT(*) AS bookings, ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate
FROM hotel_clean GROUP BY market_segment ORDER BY cancel_rate DESC;
-- name: by_hotel
SELECT hotel AS label, COUNT(*) AS bookings, ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate
FROM hotel_clean GROUP BY hotel;
-- name: by_month
SELECT arrival_date_month AS label, COUNT(*) AS bookings, ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate,
       ROUND(SUM(CASE WHEN is_canceled=1 THEN revenue ELSE 0 END),0) AS revenue_lost
FROM hotel_clean GROUP BY arrival_date_month
ORDER BY CASE arrival_date_month WHEN 'January' THEN 1 WHEN 'February' THEN 2 WHEN 'March' THEN 3 WHEN 'April' THEN 4
 WHEN 'May' THEN 5 WHEN 'June' THEN 6 WHEN 'July' THEN 7 WHEN 'August' THEN 8 WHEN 'September' THEN 9
 WHEN 'October' THEN 10 WHEN 'November' THEN 11 ELSE 12 END;
-- name: by_country
SELECT country AS label, COUNT(*) AS bookings, ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate
FROM hotel_clean GROUP BY country ORDER BY bookings DESC LIMIT 8;
-- name: high_risk_combo
SELECT market_segment, CASE WHEN lead_time>180 THEN '180+' ELSE '<=180' END AS lead_group,
       COUNT(*) AS bookings, ROUND(100.0*SUM(is_canceled)/COUNT(*),1) AS cancel_rate
FROM hotel_clean GROUP BY market_segment, lead_group HAVING COUNT(*)>200 ORDER BY cancel_rate DESC LIMIT 5;
