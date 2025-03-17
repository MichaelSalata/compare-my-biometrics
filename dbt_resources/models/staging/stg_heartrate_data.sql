{{
    config(
        materialized='view'
    )
}}

with heartrate_data as 
(
  select *,
    row_number() over(partition by src.dateTime) as rn
  from {{ source('staging','external_heartrate') }} as src
  where vendorid is not null 
)
with heartrate_data as (
    select
        -- identifiers
        {{ dbt_utils.generate_surrogate_key(['user_id', 'dateTime']) }} as heartrate_id,
        {{ dbt.safe_cast("user_id", api.Column.translate_type("string")) }} as user_id,

        -- timestamps
        cast(dateTime as timestamp) as date_time,

        -- Zone 1
        {{ dbt.safe_cast("Zone1_caloriesOut", api.Column.translate_type("float")) }} as zone1_calories_out,
        {{ dbt.safe_cast("Zone1_max_heartrate", api.Column.translate_type("integer")) }} as zone1_max_heartrate,
        {{ dbt.safe_cast("Zone1_min_heartrate", api.Column.translate_type("integer")) }} as zone1_min_heartrate,
        {{ dbt.safe_cast("Zone1_minutes", api.Column.translate_type("integer")) }} as zone1_minutes,

        -- Zone 2
        {{ dbt.safe_cast("Zone2_caloriesOut", api.Column.translate_type("float")) }} as zone2_calories_out,
        {{ dbt.safe_cast("Zone2_max_heartrate", api.Column.translate_type("integer")) }} as zone2_max_heartrate,
        {{ dbt.safe_cast("Zone2_min_heartrate", api.Column.translate_type("integer")) }} as zone2_min_heartrate,
        {{ dbt.safe_cast("Zone2_minutes", api.Column.translate_type("integer")) }} as zone2_minutes,

        -- Zone 3
        {{ dbt.safe_cast("Zone3_caloriesOut", api.Column.translate_type("float")) }} as zone3_calories_out,
        {{ dbt.safe_cast("Zone3_max_heartrate", api.Column.translate_type("integer")) }} as zone3_max_heartrate,
        {{ dbt.safe_cast("Zone3_min_heartrate", api.Column.translate_type("integer")) }} as zone3_min_heartrate,
        {{ dbt.safe_cast("Zone3_minutes", api.Column.translate_type("integer")) }} as zone3_minutes,

        -- Zone 4
        {{ dbt.safe_cast("Zone4_caloriesOut", api.Column.translate_type("float")) }} as zone4_calories_out,
        {{ dbt.safe_cast("Zone4_max_heartrate", api.Column.translate_type("integer")) }} as zone4_max_heartrate,
        {{ dbt.safe_cast("Zone4_min_heartrate", api.Column.translate_type("integer")) }} as zone4_min_heartrate,
        {{ dbt.safe_cast("Zone4_minutes", api.Column.translate_type("integer")) }} as zone4_minutes,

        -- Resting Heart Rate
        {{ dbt.safe_cast("restingHeartRate", api.Column.translate_type("integer")) }} as resting_heart_rate

    from {{ source('staging', 'external_heartrate') }} as src
    where (user_id is not null) and (rn = 1)
)

select *
from heartrate_data

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}