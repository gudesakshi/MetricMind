-- MetricMind business questions
-- 1. Total revenue
SELECT SUM(revenue) AS total_revenue FROM sales;

-- 2. Total profit
SELECT SUM(revenue - cost) AS total_profit FROM sales;

-- 3. Overall margin
SELECT SUM(revenue - cost) / NULLIF(SUM(revenue),0) AS profit_margin
FROM sales;

-- 4. Revenue by country
SELECT country, SUM(revenue) AS revenue
FROM sales
GROUP BY country
ORDER BY revenue DESC;

-- 5. Revenue by region
SELECT region, SUM(revenue) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 6. Revenue by product
SELECT product, SUM(revenue) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;

-- 7. Monthly revenue and MoM growth
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           SUM(revenue) AS revenue
    FROM sales
    GROUP BY 1
)
SELECT month,
       revenue,
       LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue,
       ROUND(
           (revenue - LAG(revenue) OVER (ORDER BY month))
           / NULLIF(LAG(revenue) OVER (ORDER BY month),0) * 100, 2
       ) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- 8. Product profitability
SELECT product,
       SUM(revenue) AS revenue,
       SUM(revenue - cost) AS profit,
       ROUND(SUM(revenue - cost) / NULLIF(SUM(revenue),0) * 100, 2) AS margin_pct
FROM sales
GROUP BY product
ORDER BY profit DESC;

-- 9. Europe margin
SELECT
    SUM(revenue - cost) AS profit,
    SUM(revenue) AS revenue,
    ROUND(SUM(revenue - cost) / NULLIF(SUM(revenue),0) * 100, 2) AS margin_pct
FROM sales
WHERE region = 'Europe';

-- 10. Countries driving growth: compare first half vs second half of available data
WITH period AS (
    SELECT country,
           CASE
             WHEN order_date < (SELECT MIN(order_date) + ((SELECT MAX(order_date) - MIN(order_date)) / 2) FROM sales)
             THEN 'First_Period' ELSE 'Second_Period'
           END AS p,
           SUM(revenue) AS revenue
    FROM sales
    GROUP BY country, p
),
pivoted AS (
    SELECT country,
           SUM(CASE WHEN p='First_Period' THEN revenue ELSE 0 END) AS first_revenue,
           SUM(CASE WHEN p='Second_Period' THEN revenue ELSE 0 END) AS second_revenue
    FROM period
    GROUP BY country
)
SELECT country, first_revenue, second_revenue,
       ROUND((second_revenue-first_revenue)/NULLIF(first_revenue,0)*100,2) AS growth_pct
FROM pivoted
ORDER BY growth_pct DESC;

-- 11. Declining products: first 3 months vs last 3 months
WITH monthly AS (
    SELECT product,
           DATE_TRUNC('month', order_date)::date AS month,
           SUM(revenue) AS revenue
    FROM sales
    GROUP BY product, 2
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY month) AS month_num,
           COUNT(*) OVER () AS total_rows
    FROM (SELECT DISTINCT month FROM monthly) m
    JOIN monthly USING(month)
)
-- For production use, calculate first/last 3 month windows explicitly based on min/max dates.
SELECT product,
       AVG(revenue) FILTER (WHERE month <= (SELECT MIN(month) + INTERVAL '2 months' FROM monthly)) AS first_3m_avg,
       AVG(revenue) FILTER (WHERE month >= (SELECT MAX(month) - INTERVAL '2 months' FROM monthly)) AS last_3m_avg
FROM monthly
GROUP BY product
ORDER BY (AVG(revenue) FILTER (WHERE month >= (SELECT MAX(month) - INTERVAL '2 months' FROM monthly))
        - AVG(revenue) FILTER (WHERE month <= (SELECT MIN(month) + INTERVAL '2 months' FROM monthly))) ASC;
