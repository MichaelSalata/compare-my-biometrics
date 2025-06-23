import os
import json
import subprocess
import logging
import glob

from datetime import datetime

from google.cloud import bigquery

from airflow.decorators import dag, task
from airflow.models import Connection
from airflow.utils.db import provide_session
from airflow.providers.google.cloud.hooks.gcs import GCSHook

from fitbit_json_to_parquet import flatten_fitbit_json_file


PROJECT_ID = str(os.environ.get("GCP_PROJECT_ID"))
GCP_GCS_BUCKET = str(os.environ.get("GCP_GCS_BUCKET", f"{PROJECT_ID}-fitbit-bucket"))
BIGQUERY_DATASET = str(os.environ.get("BIGQUERY_DATASET", "fitbit_dataset"))

airflow_path = os.environ.get("AIRFLOW_HOME")
DBT_IS_TEST_RUN = os.environ.get("IS_DEV_ENV", True)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
task_logger = logging.getLogger(__name__)

@provide_session
def update_fitbit_connection(session=None):
    try:
        # Check if the connection already exists
        existing_conn = session.query(Connection).filter(Connection.conn_id == "fitbit_default").first()
        if existing_conn:
            task_logger.info("Connection 'fitbit_default' already exists. Updating access_token...")
            try:
                with open("fitbit_tokens.json", 'r') as file:
                    tokens = json.load(file)
            except FileNotFoundError:
                task_logger.warning(f"fitbit_tokens.json not found")
                return

            existing_conn.login = tokens["client_id"]
            existing_conn.password = tokens["client_secret"]
            
            extra_kv_tokens = json.loads(existing_conn.extra) if existing_conn.extra else {}
            extra_kv_tokens["access_token"] = tokens.get("access_token", extra_kv_tokens.get("access_token"))
            extra_kv_tokens["user_id"] = tokens.get("user_id", extra_kv_tokens.get("access_token"))
            existing_conn.extra = json.dumps(extra_kv_tokens)
            session.commit()
            task_logger.info("user_id, client_id, client_secret, access_token and refresh_token updated successfully.")
            return
    except Exception as e:
        task_logger.error(f"Exception {e} checking or updating Fitbit connection")

    try:
        with open("fitbit_tokens.json", 'r') as file:
            tokens = json.load(file)
    except FileNotFoundError:
        task_logger.error(f"fitbit_tokens.json not found")
        return

    extra_kv_tokens = tokens.copy()
    del extra_kv_tokens["client_id"]
    del extra_kv_tokens["client_secret"]
    conn = Connection(
        conn_id="fitbit_default",
        conn_type="http",
        login=tokens["client_id"],
        password=tokens["client_secret"],
        extra=json.dumps(extra_kv_tokens)
    )
    session.add(conn)
    session.commit()
    task_logger.info("Connection 'fitbit_default' created successfully.")




@task
def flatten_fitbit_data(json_file: str):
    parquet_file, endpoint_id = flatten_fitbit_json_file(json_file=json_file)
    return {"filepath": parquet_file, "endpoint_id": endpoint_id}


@task
def upload_to_gcs(endpoint_file: dict):
    endpoint_id = endpoint_file["endpoint_id"]
    filename = os.path.basename(endpoint_file["filepath"])

    gcp_blob = f"{endpoint_id}/{filename}"
    task_logger.info(f"Uploading {filename} to {gcp_blob}...")
    gcs_hook = GCSHook()
    gcs_hook.upload(bucket_name=GCP_GCS_BUCKET, object_name=gcp_blob, filename=endpoint_file["filepath"])
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
def find_biometric_jsons(biometrics: list[str]):
    matched_files = []
    for b in biometrics:
        matched_files.extend(glob.glob(f"./example_data/{b}*.json"))

    return matched_files


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
    dag_id="parallel_backfill_fitbit_example_data",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['dtc-de']
)
def fitbit_example_data_pipeline():
    # the only fitbit data currently supported is both:
        # keyword mapped in FitbitHook.py plugin class
        # AND
        # keyword mapped in fitbit_json_to_parquet.py  flatten_fitbit_json func
    FITBIT_BIOMETRICS = ["sleep", "heartrate"]
    BQ_TABLES = FITBIT_BIOMETRICS + ["profile"]
    update_fitbit_connection()

    # flatten and upload profile
    flattened_profile = flatten_fitbit_data(json_file="./example_data/profile.json")
    profile_parquets_in_gcs = upload_to_gcs(flattened_profile)

    # flatten and upload biometrics
    flattened_biometrics = flatten_fitbit_data.expand(json_file=find_biometric_jsons(FITBIT_BIOMETRICS))
    biometrics_in_gcs = upload_to_gcs.expand(endpoint_file=flattened_biometrics)

    # create BigQuery external tables for parquet files in GCS
    setup_bq_ext_tables = parquets_to_bq_table.expand(endpoint_id=BQ_TABLES)


    [profile_parquets_in_gcs, biometrics_in_gcs] >> setup_bq_ext_tables >> run_dbt()
    

fitbit_dag = fitbit_example_data_pipeline()
