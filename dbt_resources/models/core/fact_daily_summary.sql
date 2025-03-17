{{
    config(
        materialized='table'
    )
}}

WITH sleep AS (
    SELECT * FROM {{ ref('stg_sleep_data') }}
),
heartrate AS (
    SELECT * FROM {{ ref('stg_heartrate_data') }}
),
profile AS (
    SELECT * FROM {{ ref('stg_profile_data') }}
)


SELECT 
    p.user_id,
    h.date,
    p.age,
    p.gender,
    p.height,
    p.weight,
    p.distanceUnit,
    
    -- Sleep metrics
    s.minutesAsleep,
    s.minutesAwake,
    s.minutesToFallAsleep,
    s.timeInBed,
    s.deep_minutes,
    s.light_minutes,
    s.rem_minutes,
    s.wake_minutes,

    -- Heartrate metrics
    h.Zone1_caloriesOut,
    h.Zone1_max_heartrate,
    h.Zone1_min_heartrate,
    h.Zone1_minutes,
    h.Zone2_caloriesOut,
    h.Zone2_max_heartrate,
    h.Zone2_min_heartrate,
    h.Zone2_minutes,
    h.Zone3_caloriesOut,
    h.Zone3_max_heartrate,
    h.Zone3_min_heartrate,
    h.Zone3_minutes,
    h.Zone4_caloriesOut,
    h.Zone4_max_heartrate,
    h.Zone4_min_heartrate,
    h.Zone4_minutes,
    h.restingHeartRate

FROM heartrate h
LEFT JOIN sleep s 
    ON h.user_id = s.user_id 
    AND h.date = s.date
LEFT JOIN profile p 
    ON h.user_id = p.user_id
