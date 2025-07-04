import os
import json
import subprocess
import logging

from datetime import datetime

from google.cloud import bigquery

from airflow.decorators import dag, task, task_group
from airflow.models import Connection
from airflow.utils.db import provide_session
from airflow.operators.python import get_current_context
from airflow.providers.google.cloud.hooks.gcs import GCSHook

from fitbit_json_to_parquet import flatten_fitbit_json_file
from fitbit_hook import FitbitHook

PROJECT_ID = str(os.environ.get("GCP_PROJECT_ID"))
GCP_GCS_BUCKET = str(os.environ.get("GCP_GCS_BUCKET", f"{PROJECT_ID}-fitbit-bucket"))
BIGQUERY_DATASET = str(os.environ.get("BIGQUERY_DATASET", "fitbit_dataset"))

airflow_path = os.environ.get("AIRFLOW_HOME")
DBT_IS_TEST_RUN = os.environ.get("IS_DEV_ENV", True)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
task_logger = logging.getLogger(__name__)


@task
def download_profile():
    fitbit_hook = FitbitHook()

    endpoint_suffix = fitbit_hook.static_endpoints.get("profile").format(user_id=fitbit_hook.user_id)
    response = fitbit_hook.fetch_from_endpoint(endpoint_suffix=endpoint_suffix)
    if response:
        signup_date_str = response.get("user").get("memberSince")
        signup_date = datetime.strptime(signup_date_str, "%Y-%m-%d")
        return {
            "json_file": fitbit_hook.save_data(data=response, endpoint_name="profile"),
            "signup_date": signup_date
        }
    else:
        raise Exception("empty profile API response")

@task
def get_profile_path(profile_data: dict):
    return profile_data["json_file"]


@task(retries=3)
def download_since_signup(signup_date: datetime, endpoint_id: str):
    fitbit_hook = FitbitHook()
    end_date = get_current_context()['execution_date'].date()
    if endpoint_id in fitbit_hook.dayrange_endpoints:
        response = fitbit_hook.fetch_daterange(endpoint_id=endpoint_id, start=signup_date, end=end_date)
        if response:
            return fitbit_hook.save_data(response, endpoint_id, start_date=signup_date, end_date=end_date)
        else:
            task_logger.warning(f"No data retrieved for {endpoint_id} from {signup_date} to {end_date}")
            return None


@task
def flatten_fitbit_data(json_file: str):
    parquet_file, endpoint_id = flatten_fitbit_json_file(json_file=json_file)
    return {"filename": parquet_file, "endpoint_id": endpoint_id}


@task
def upload_to_gcs(endpoint_file: dict):
    endpoint_id = endpoint_file["endpoint_id"]
    filename = endpoint_file["filename"]

    gcp_blob = f"{endpoint_id}/{filename}"
    task_logger.info(f"Uploading {filename} to {gcp_blob}...")
    gcs_hook = GCSHook()
    gcs_hook.upload(bucket_name=GCP_GCS_BUCKET, object_name=gcp_blob, filename=filename)
    task_logger.info(f"Upload successful to {gcp_blob}")
    return gcp_blob

@task
def parquets_to_bq_table(endpoint_id: str):
    client = bigquery.Client()

    table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}.external_{endpoint_id}"

    table = bigquery.Table(table_id)
    external_config = bigquery.ExternalConfig(source_format=bigquery.SourceFormat.PARQUET)
    external_config.source_uris = [f"gs://{GCP_GCS_BUCKET}/{endpoint_id}/{endpoint_id}*.parquet"]

    table.external_data_configuration = external_config

    table = client.create_table(table, exists_ok=True)

    return endpoint_id

@task
def prep_biometric_jobs(profile_data: dict, biometrics: list[str]):
    signup_date = profile_data["signup_date"]
    return [{"signup_date": signup_date, "biometric": b} for b in biometrics]


@task
def run_dbt():
    dbt_command = " && ".join([
        f"cd {airflow_path}/dbt_resources",
        "dbt deps",
        "dbt build --vars '{is_test_run: " + str(DBT_IS_TEST_RUN) + "}'"
        ])
    try:
        task_logger.info("Executing:", dbt_command)
        subprocess.run(dbt_command, shell=True, check=True, text=True)
        task_logger.info("DBT commands ran successfully.")
    except subprocess.CalledProcessError as e:
        task_logger.error(f"DBT command failed: {e}")
        raise e



default_args = {
    "owner": "MSalata",             # default: airflow
    "depends_on_past": False,       # default: False
    "retries": 0,                   # default: 0
}

@dag(
    dag_id="parallel_backfill_fitbit_from_signup",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['dtc-de']
)
def fitbit_pipeline():
    # the only fitbit data currently supported is both:
        # keyword mapped in FitbitHook.py plugin class
        # AND
        # keyword mapped in fitbit_json_to_parquet.py  flatten_fitbit_json func
    FITBIT_BIOMETRICS = ["sleep", "heartrate"]
    BQ_TABLES = FITBIT_BIOMETRICS + ["profile"]

    # download, flatten and upload profile
    profile_data = download_profile()
    flattened_profile = flatten_fitbit_data(json_file=get_profile_path(profile_data))
    profile_parquets_in_gcs = upload_to_gcs(flattened_profile)

    # download, flatten and upload 1 biometric datatype
    @task_group
    def ETL_biometrics(signup_date: datetime, biometric: str):
        biometric_json = download_since_signup(signup_date=signup_date, endpoint_id=biometric)
        biometric_parquet = flatten_fitbit_data(json_file=biometric_json)
        upload_to_gcs(biometric_parquet)
    
    # run the task_group for each biometric in parallel
    biometrics_in_gcs = ETL_biometrics.expand_kwargs(prep_biometric_jobs(profile_data, FITBIT_BIOMETRICS))

    # create BigQuery external tables for parquet files in GCS
    setup_bq_ext_tables = parquets_to_bq_table.expand(endpoint_id=BQ_TABLES)


    [profile_parquets_in_gcs, biometrics_in_gcs] >> setup_bq_ext_tables >> run_dbt()
    

fitbit_dag = fitbit_pipeline()
