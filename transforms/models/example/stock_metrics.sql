{{ config(materialized ='table')}}

SELECT * ,
        (close-open) / open *100 as daily_return,
        (high-low)  as price_range,
        AVG(close) OVER (
    PARTITION BY symbol
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) AS moving_avg_7d
FROM  stock_prices