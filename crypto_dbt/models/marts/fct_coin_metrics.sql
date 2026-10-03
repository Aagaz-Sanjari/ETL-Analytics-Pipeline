with prices as (

    select * from {{ ref('stg_coingecko_markets') }}

),

with_previous as (

    select
        coin_id,
        symbol,
        current_price,
        market_cap,
        total_volume,
        last_updated_at,
        lag(current_price) over (
            partition by coin_id
            order by last_updated_at
        ) as previous_price
    from prices

)

select
    coin_id,
    symbol,
    current_price,
    market_cap,
    total_volume,
    last_updated_at,
    previous_price,
    round(
        (current_price - previous_price) / nullif(previous_price, 0) * 100,
        4
    ) as return_pct,
    avg(current_price) over w as moving_avg_3,
    coalesce(stddev_samp(current_price) over w, 0) as rolling_volatility_3
from with_previous
window w as (
    partition by coin_id
    order by last_updated_at
    rows between 2 preceding and current row
)