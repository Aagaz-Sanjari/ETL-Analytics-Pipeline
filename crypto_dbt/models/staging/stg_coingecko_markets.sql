with raw_records as (

    select
        payload,
        ingested_at
    from {{ source('raw', 'ingested_records') }}
    where source = 'coingecko'
      and dataset = 'markets'

)

select
    payload->>'id' as coin_id,
    payload->>'symbol' as symbol,
    payload->>'name' as coin_name,
    (payload->>'current_price')::numeric as current_price,
    (payload->>'market_cap')::numeric as market_cap,
    (payload->>'total_volume')::numeric as total_volume,
    (payload->>'high_24h')::numeric as high_24h,
    (payload->>'low_24h')::numeric as low_24h,
    (payload->>'price_change_percentage_24h')::numeric as price_change_pct_24h,
    (payload->>'last_updated')::timestamptz as last_updated_at,
    ingested_at
from raw_records
where (payload->>'current_price')::numeric > 0