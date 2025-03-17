{{
    config(
        materialized='table'
    )
}}

WITH p AS (
    SELECT * FROM {{ ref('stg_profile_data') }}
    where user_id is not null
),
s AS (
    SELECT *
    FROM {{ ref('stg_sleep_data') }} as slp
    where slp.user_id is not null
    left join p ON p.user_id = slp.user_id
),
h AS (
    SELECT *
    FROM {{ ref('stg_heartrate_data') }} as hr
    where hr.user_id is not null
    left join profile p ON p.user_id = hr.user_id
),

SELECT 
    p.user_id,
    h.date_time,
    p.age,
    p.gender,
    p.height,
    p.weight,
    p.distance_unit,
    
    -- Sleep metrics
    s.duration,
    s.efficiency,
    s.minutes_awake,
    s.minutes_to_fall_asleep,
    s.time_in_bed,
    s.deep_minutes,
    s.light_minutes,
    s.rem_minutes,
    s.wake_minutes,

    -- Heartrate metrics
    h.zone1_calories_out,
    h.zone1_max_heartrate,
    h.zone1_min_heartrate,
    h.zone1_minutes,
    h.zone2_calories_out,
    h.zone2_max_heartrate,
    h.zone2_min_heartrate,
    h.zone2_minutes,
    h.zone3_calories_out,
    h.zone3_max_heartrate,
    h.zone3_min_heartrate,
    h.zone3_minutes,
    h.zone4_calories_out,
    h.zone4_max_heartrate,
    h.zone4_min_heartrate,
    h.zone4_minutes,
    h.resting_heart_rate
FROM sleep s
OUTER JOIN heartrate h
    ON s.date_of_sleep = h.date_time

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}