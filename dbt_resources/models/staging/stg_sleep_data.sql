{{ config(materialized='view') }}
 
with sleep_data as 
(
  select *,
    row_number() over(partition by dateOfSleep, user_id) as rn
  from {{ source('staging','external_sleep') }}
  where dateOfSleep is not null and user_id is not null
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['user_id', 'logId']) }} as sleep_id,
    {{ dbt.safe_cast("user_id", api.Column.translate_type("string")) }} as user_id,

    -- timestamps
    TIMESTAMP_MILLIS(CAST(dateOfSleep / 1000000 AS INT64)) as date_of_sleep,
    TIMESTAMP_MILLIS(CAST(startTime / 1000000 AS INT64)) as start_time,
    TIMESTAMP_MILLIS(CAST(endTime / 1000000 AS INT64)) as end_time,

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
    -- deep
    {{ dbt.safe_cast("deep_count", api.Column.translate_type("integer")) }} as deep_count,
    {{ dbt.safe_cast("deep_minutes", api.Column.translate_type("integer")) }} as deep_minutes,
    {{ dbt.safe_cast("deep_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as deep_thirty_day_avg_minutes,

    -- light
    {{ dbt.safe_cast("light_count", api.Column.translate_type("integer")) }} as light_count,
    {{ dbt.safe_cast("light_minutes", api.Column.translate_type("integer")) }} as light_minutes,
    {{ dbt.safe_cast("light_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as light_thirty_day_avg_minutes,

    -- rem
    {{ dbt.safe_cast("rem_count", api.Column.translate_type("integer")) }} as rem_count,
    {{ dbt.safe_cast("rem_minutes", api.Column.translate_type("integer")) }} as rem_minutes,
    {{ dbt.safe_cast("rem_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as rem_thirty_day_avg_minutes,

    -- wake
    {{ dbt.safe_cast("wake_count", api.Column.translate_type("integer")) }} as wake_count,
    {{ dbt.safe_cast("wake_minutes", api.Column.translate_type("integer")) }} as wake_minutes,
    {{ dbt.safe_cast("wake_thirtyDayAvgMinutes", api.Column.translate_type("integer")) }} as wake_thirty_day_avg_minutes
    
from sleep_data
where rn = 1


-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}