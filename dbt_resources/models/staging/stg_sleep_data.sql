{{ config(materialized='view') }}
 
with sleep_data as 
(
  select *,
    row_number() over(partition by dateOfSleep, user_id) as rn
  from {{ source('staging','external_sleep') }}
  where dateOfSleep is not null 
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['user_id', 'dateOfSleep']) }} as sleep_id,
    {{ dbt.safe_cast("user_id", api.Column.translate_type("string")) }} as user_id,

    -- timestamps
    cast(dateOfSleep as timestamp) as date_of_sleep,
    cast(startTime as timestamp) as start_time,
    cast(endTime as timestamp) as end_time,

    -- sleep info
    {{ dbt.safe_cast("duration", api.Column.translate_type("integer")) }} as duration,
    {{ dbt.safe_cast("efficiency", api.Column.translate_type("float")) }} as efficiency,
    {{ dbt.safe_cast("infoCode", api.Column.translate_type("integer")) }} as info_code,
    {{ dbt.safe_cast("isMainSleep", api.Column.translate_type("boolean")) }} as is_main_sleep,
    {{ dbt.safe_cast("logId", api.Column.translate_type("integer")) }} as log_id,
    {{ dbt.safe_cast("logType", api.Column.translate_type("string")) }} as log_type,
    {{ dbt.safe_cast("minutesAfterWakeup", api.Column.translate_type("integer")) }} as minutes_after_wakeup,
    {{ dbt.safe_cast("minutesAsleep", api.Column.translate_type("integer")) }} as minutes_asleep,
    {{ dbt.safe_cast("minutesAwake", api.Column.translate_type("integer")) }} as minutes_awake,
    {{ dbt.safe_cast("minutesToFallAsleep", api.Column.translate_type("integer")) }} as minutes_to_fall_asleep,
    {{ dbt.safe_cast("timeInBed", api.Column.translate_type("integer")) }} as time_in_bed,
    {{ dbt.safe_cast("type", api.Column.translate_type("string")) }} as type,

    -- sleep stages
    {{ dbt.safe_cast("deep_count", api.Column.translate_type("integer")) }} as deep_count,
    {{ dbt.safe_cast("deep_minutes", api.Column.translate_type("integer")) }} as deep_minutes,
    {{ dbt.safe_cast("deep_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as deep_thirty_day_avg_minutes,
    {{ dbt.safe_cast("light_count", api.Column.translate_type("integer")) }} as light_count,
    {{ dbt.safe_cast("light_minutes", api.Column.translate_type("integer")) }} as light_minutes,
    {{ dbt.safe_cast("light_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as light_thirty_day_avg_minutes,
    {{ dbt.safe_cast("rem_count", api.Column.translate_type("integer")) }} as rem_count,
    {{ dbt.safe_cast("rem_minutes", api.Column.translate_type("integer")) }} as rem_minutes,
    {{ dbt.safe_cast("rem_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as rem_thirty_day_avg_minutes,
    {{ dbt.safe_cast("wake_count", api.Column.translate_type("integer")) }} as wake_count,
    {{ dbt.safe_cast("wake_minutes", api.Column.translate_type("integer")) }} as wake_minutes,
    {{ dbt.safe_cast("wake_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as wake_thirty_day_avg_minutes

from sleep_data


-- select
--    -- identifiers
--     {{ dbt_utils.generate_surrogate_key(['vendorid', 'tpep_pickup_datetime']) }} as tripid,    
--     {{ dbt.safe_cast("vendorid", api.Column.translate_type("integer")) }} as vendorid,
--     {{ dbt.safe_cast("ratecodeid", api.Column.translate_type("integer")) }} as ratecodeid,
--     {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
--     {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,

--     -- timestamps
--     cast(tpep_pickup_datetime as timestamp) as pickup_datetime,
--     cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime,
    
--     -- trip info
--     store_and_fwd_flag,
--     {{ dbt.safe_cast("passenger_count", api.Column.translate_type("integer")) }} as passenger_count,
--     cast(trip_distance as numeric) as trip_distance,
--     -- yellow cabs are always street-hail
--     1 as trip_type,
    
--     -- payment info
--     cast(fare_amount as numeric) as fare_amount,
--     cast(extra as numeric) as extra,
--     cast(mta_tax as numeric) as mta_tax,
--     cast(tip_amount as numeric) as tip_amount,
--     cast(tolls_amount as numeric) as tolls_amount,
--     cast(improvement_surcharge as numeric) as improvement_surcharge,
--     cast(total_amount as numeric) as total_amount,
--     coalesce({{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }},0) as payment_type,
--     {{ get_payment_type_description('payment_type') }} as payment_type_description
-- from tripdata
-- where rn = 1

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}