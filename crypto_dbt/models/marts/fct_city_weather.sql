with weather as (

    select * from {{ ref('stg_open_meteo_current') }}

)

select
    city,
    observed_at,
    temperature_c,
    humidity_pct,
    wind_speed_kmh,
    precipitation_mm,
    precipitation_mm > 0 as is_raining,
    temperature_c - lag(temperature_c) over (
        partition by city
        order by observed_at
    ) as temp_change_c,
    avg(temperature_c) over w as moving_avg_temp_3,
    max(temperature_c) over w as max_temp_3
from weather
window w as (
    partition by city
    order by observed_at
    rows between 2 preceding and current row
)