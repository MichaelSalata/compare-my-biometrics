{{ config(materialized='view') }}
 
select
    -- identifiers
    {{ dbt.safe_cast("user_id", api.Column.translate_type("string")) }} as user_id,

    -- profile info
    {{ dbt.safe_cast("age", api.Column.translate_type("integer")) }} as age,
    {{ dbt.safe_cast("averageDailySteps", api.Column.translate_type("integer")) }} as average_daily_steps,
    TIMESTAMP_MILLIS(CAST(dateOfBirth / 1000000 AS INT64)) as date_of_birth,
    {{ dbt.safe_cast("displayName", api.Column.translate_type("string")) }} as display_name,
    {{ dbt.safe_cast("distanceUnit", api.Column.translate_type("string")) }} as distance_unit,
    {{ dbt.safe_cast("firstName", api.Column.translate_type("string")) }} as first_name,
    {{ dbt.safe_cast("fullName", api.Column.translate_type("string")) }} as full_name,
    {{ dbt.safe_cast("lastName", api.Column.translate_type("string")) }} as last_name,
    {{ dbt.safe_cast("gender", api.Column.translate_type("string")) }} as gender,
    {{ dbt.safe_cast("height", api.Column.translate_type("float")) }} as height,
    {{ dbt.safe_cast("heightUnit", api.Column.translate_type("string")) }} as height_unit,
    {{ dbt.safe_cast("weight", api.Column.translate_type("float")) }} as weight,
    {{ dbt.safe_cast("weightUnit", api.Column.translate_type("string")) }} as weight_unit

from {{ source('staging', 'external_profile') }} as src
where user_id is not null

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}