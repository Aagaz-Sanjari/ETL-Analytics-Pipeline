with raw_records as (

    select
        payload,
        ingested_at
    from {{ source('raw', 'ingested_records') }}
    where source = 'open_meteo'
      and dataset = 'current'

)

select
    payload->>'city' as city,
    (payload->>'latitude')::numeric as latitude,
    (payload->>'longitude')::numeric as longitude,
    (payload->>'observed_at')::timestamp at time zone 'UTC' as observed_at,
    (payload->>'temperature_c')::numeric as temperature_c,
    (payload->>'humidity_pct')::numeric as humidity_pct,
    (payload->>'wind_speed_kmh')::numeric as wind_speed_kmh,
    (payload->>'precipitation_mm')::numeric as precipitation_mm,
    ingested_at
from raw_records