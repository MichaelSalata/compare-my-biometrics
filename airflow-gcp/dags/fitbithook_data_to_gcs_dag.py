import glob
import os
# import logging
import time
import json

from airflow.models import Connection
from airflow.utils.db import provide_session

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
# import pyarrow.csv as pv
# import pyarrow.parquet as pq

from fitbit_json_to_parquet import profile_sleep_heartrate_jsons_to_parquet
from fitbit_hook import FitbitHook
# from download_locally import download_past_6_months

PROJECT_ID = str(os.environ.get("GCP_PROJECT_ID"))
GCP_GCS_BUCKET = str(os.environ.get("GCP_GCS_BUCKET", f"{PROJECT_ID}-fitbit-bucket"))
BIGQUERY_DATASET = str(os.environ.get("BIGQUERY_DATASET", "fitbit_dataset"))
# CREDENTIALS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "google_credentials.json")

airflow_path = os.environ.get("AIRFLOW_HOME")
dbt_is_test_run = "'{is_test_run: " + f"{os.environ.get("IS_DEV_ENV", False)}" + "}'"


def upload_to_gcs(bucket_name, max_retries=3):
    client = storage.Client()
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    bucket = client.bucket(bucket_name)
    CHUNK_SIZE = 8 * 1024 * 1024

    regex = os.path.join(airflow_path,"*.parquet")
    data_files = glob.glob(regex)
    if len(data_files) == 0:
        print("No Data Files Found -> uploading example data")
        regex = os.path.join(airflow_path,"example_data","*.parquet")
        data_files = glob.glob(regex)   
    
    for file_w_path in data_files:
        file_name = os.path.basename(file_w_path)
        blob = bucket.blob(file_name)   # IMPORTANT: path on str passed into bucket.blob will be were it's stored in the bucket
        blob.chunk_size = CHUNK_SIZE
        
        for attempt in range(max_retries):
            try:
                print(f"Uploading {file_w_path} to {bucket_name} (Attempt {attempt + 1}/{max_retries})...")
                blob.upload_from_filename(file_w_path)
                
                if blob.exists():
                    print(f"Upload Verification successful for gs://{bucket_name}/{file_name}")
                    break
                else:
                    print(f"Verification failed for {file_w_path}, retrying...")
            except Exception as e:
                print(f"Failed to upload {file_w_path} to GCS: {e}")
            
            time.sleep(2)


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
            extra_kv_tokens["user_id"] = tokens.get("user_id", extra_kv_tokens.get("access_token"))
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



def download_fitbit_data():
    hook = FitbitHook()
    hook.download_past_6_months("profile")
    hook.download_past_6_months("sleep")
    hook.download_past_6_months("heartrate")

default_args = {
    "owner": "MSalata",             # default: airflow
    "start_date": days_ago(1),
    "depends_on_past": False,       # default: False
    "retries": 3,                   # default: 0
}

# Official Documentation: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html#airflow.models.dag.DAG
with DAG(
    dag_id="fitbithook_data_to_gcs_dag",
    schedule_interval="@monthly",
    default_args=default_args,
    catchup=False,                  # default: True
    max_active_runs=3,
    tags=['dtc-de']
) as hook_dag:
    update_fitbit_tokens_task = PythonOperator(
        task_id="update_fitbit_tokens_task",
        python_callable=update_fitbit_connection,
    )

    download_fitbit_data_task = PythonOperator(
        task_id="download_fitbit_data_task",
        python_callable=download_fitbit_data,
        op_kwargs={
            "tokens_path": airflow_path,
        },
    )

    fitbit_to_parquet_task = PythonOperator(
        task_id="fitbit_to_parquet_task",
        python_callable=profile_sleep_heartrate_jsons_to_parquet,
        op_kwargs={
            "base_path": airflow_path,
        },
    )

    upload_to_gcs_task = PythonOperator(
        task_id="upload_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket_name": GCP_GCS_BUCKET,
        },
    )

    bq_external_sleep_table = BigQueryCreateExternalTableOperator(
        task_id="bq_external_sleep_table",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_sleep",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{GCP_GCS_BUCKET}/sleep*.parquet"],
            },
        },
    )

    bq_external_heartrate_table = BigQueryCreateExternalTableOperator(
        task_id="bq_external_heartrate_table",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_heartrate",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{GCP_GCS_BUCKET}/heartrate*.parquet"],
            },
        },
    )

    bq_external_profile_table = BigQueryCreateExternalTableOperator(
        task_id="bq_external_profile_table",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_profile",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{GCP_GCS_BUCKET}/profile*.parquet"],
            },
        },
    )

    dbt_transforms_task = BashOperator(
        task_id='dbt_transforms_task',
        bash_command=f"cd {airflow_path}/dbt_resources && dbt deps && dbt build --vars {dbt_is_test_run}",
        depends_on_past=True,
        trigger_rule="all_success"
    )

    update_fitbit_tokens_task >> download_fitbit_data_task >> fitbit_to_parquet_task >> upload_to_gcs_task >> [bq_external_profile_table, bq_external_heartrate_table, bq_external_sleep_table] >> dbt_transforms_task

# if (__name__ == "__main__") and os.environ.get("IS_DEV_ENV"):
#     dag.test()
    # example arguments
    # execution_date if you want to test argument-specific DAG runs
    # use_executor if you want to test the DAG using an executor. By default dag.test runs the DAG without an executor, it just runs all the tasks locally. By providing this argument, the DAG is executed using the executor configured in the Airflow environment.

    
