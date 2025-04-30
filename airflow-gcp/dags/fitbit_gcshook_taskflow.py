import glob
import os
# import logging
import time
import json

from airflow.decorators import dag, task

from airflow.models import Connection
from airflow.utils.db import provide_session

from airflow.utils.dates import days_ago
import subprocess

from google.cloud import storage, bigquery

from fitbit_json_to_parquet_v2 import flatten_fitbit_json
from fitbit_hook import FitbitHook
# from download_locally import download_past_6_months

PROJECT_ID = str(os.environ.get("GCP_PROJECT_ID"))
GCP_GCS_BUCKET = str(os.environ.get("GCP_GCS_BUCKET", f"{PROJECT_ID}-fitbit-bucket"))
BIGQUERY_DATASET = str(os.environ.get("BIGQUERY_DATASET", "fitbit_dataset"))
# CREDENTIALS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "google_credentials.json")

airflow_path = os.environ.get("AIRFLOW_HOME")
dbt_is_test_run = "'{is_test_run: " + f"{os.environ.get("IS_DEV_ENV", False)}" + "}'"


@provide_session
def update_fitbit_connection(session=None):
    try:
        # Check if the connection already exists
        existing_conn = session.query(Connection).filter(Connection.conn_id == "fitbit_default").first()
        if existing_conn:
            print("Connection 'fitbit_default' already exists. Updating access_token...")
            try:
                with open("fitbit_tokens.json", 'r') as file:
                    tokens = json.load(file)
            except FileNotFoundError:
                print(f"fitbit_tokens.json not found")
                return

            existing_conn.login = tokens["client_id"]
            existing_conn.password = tokens["client_secret"]
            
            extra_kv_tokens = json.loads(existing_conn.extra) if existing_conn.extra else {}
            extra_kv_tokens["access_token"] = tokens.get("access_token", extra_kv_tokens.get("access_token"))
            extra_kv_tokens["user_id"] = tokens.get("user_id")
            existing_conn.extra = json.dumps(extra_kv_tokens)
            session.commit()
            print("user_id, client_id, client_secret, access_token and refresh_token updated successfully.")
            return
    except Exception as e:
        print(f"Exception {e} checking or updating Fitbit connection")

    try:
        with open("fitbit_tokens.json", 'r') as file:
            tokens = json.load(file)
    except FileNotFoundError:
        print(f"fitbit_tokens.json not found")
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
    print("Connection 'fitbit_default' created successfully.")



default_args = {
    "owner": "MSalata",             # default: airflow
    "start_date": days_ago(1),
    "depends_on_past": False,       # default: False
    "retries": 3,                   # default: 0
}


@dag(
    dag_id="fitbit_gcshook_taskflow",
    schedule_interval="@monthly",
    start_date=days_ago(1),
    catchup=False,
    tags=['dtc-de']
)
def fitbit_pipeline():
    DATASETS = ["profile", "sleep", "heartrate"]
    update_fitbit_connection()
    hook = FitbitHook()

    @task
    def get_data(dataset: str):
        hook.download_past_6_months(dataset)

    @task
    def flatten_data(endpoint_id: str):
        return flatten_fitbit_json(endpoint_id)

    @task
    def upload_to_gcs(endpoint_id: str):

        client = storage.Client()

        bucket = client.bucket(GCP_GCS_BUCKET)
        CHUNK_SIZE = 8 * 1024 * 1024
        max_retries = 3  # Define the maximum number of retries

        file_regex = endpoint_id + "*.parquet"
        path_regex = os.path.join(airflow_path, file_regex)
        file_paths = glob.glob(path_regex)
        if len(file_paths) == 0:
            print(f"No Data Files Found -> uploading {file_regex} from example data")
            file_paths = glob.glob(os.path.join(airflow_path, "example_data", file_regex))   
        
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            blob = bucket.blob(file_name)   # IMPORTANT: the str passed into bucket.blob will be were it's stored in the bucket
            blob.chunk_size = CHUNK_SIZE
            
            for attempt in range(max_retries):
                try:
                    print(f"Uploading {file_path} to {GCP_GCS_BUCKET} (Attempt {attempt + 1}/{max_retries})...")
                    blob.upload_from_filename(file_path)
                    
                    if blob.exists():
                        print(f"Upload Verification successful for gs://{GCP_GCS_BUCKET}/{file_name}")
                        break
                    else:
                        print(f"Verification failed for {file_path}, retrying...")
                except Exception as e:
                    print(f"Failed to upload {file_path} to GCS: {e}")
                
                time.sleep(2)
        
        # return f"gs://{GCP_GCS_BUCKET}/{file_name}"
        return endpoint_id


    @task
    def create_bq_table(endpoint_id: str):
        client = bigquery.Client()

        table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}.external_{endpoint_id}"

        table = bigquery.Table(table_id)
        external_config = bigquery.ExternalConfig(source_format=bigquery.SourceFormat.PARQUET)
        external_config.source_uris = [f"gs://{GCP_GCS_BUCKET}/{endpoint_id}*.parquet"]

        table.external_data_configuration = external_config

        table = client.create_table(table, exists_ok=True)

        return table_id

    six_mo_backlog_data_endpoint_ids = get_data.expand(dataset=DATASETS)
    flattened_endpoint_ids = flatten_data.expand(endpoint_id=six_mo_backlog_data_endpoint_ids)
    uploaded_endpoint_ids = upload_to_gcs.expand(endpoint_id=flattened_endpoint_ids)
    bq_tables = create_bq_table.expand(endpoint_id=uploaded_endpoint_ids)

    @task
    def run_dbt():
        dbt_command = f"cd {airflow_path}/dbt_resources && dbt deps && dbt build --vars '{dbt_is_test_run}'"
        try:
            print("Executing:", dbt_command)
            subprocess.run(dbt_command, shell=True, check=True, text=True)
            print("DBT commands ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"DBT command failed: {e}")
            raise

    # all tasks in `bq_tables` must complete successfully before `run_dbt` is executed
    bq_tables >> run_dbt()


fitbit_dag = fitbit_pipeline()