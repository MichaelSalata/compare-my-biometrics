import glob
import os
# import logging
import time

from airflow import DAG
from airflow.utils.dates import days_ago
# from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

from download_locally import download_past_6_months
from fitbit_json_to_parquet import profile_sleep_heartrate_jsons_to_parquet

PROJECT_ID = str(os.environ.get("GCP_PROJECT_ID", "dtc-de-446723"))
GCP_GCS_BUCKET = str(os.environ.get("GCP_GCS_BUCKET", f"{PROJECT_ID}-fitbit-bucket"))
BIGQUERY_DATASET = str(os.environ.get("BIGQUERY_DATASET", "fitbit_dataset"))
# CREDENTIALS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "google_credentials.json")

path_to_local_home = os.environ.get("AIRFLOW_HOME")


def upload_to_gcs(bucket_name, max_retries=3):
    client = storage.Client()
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    bucket = client.bucket(bucket_name)
    CHUNK_SIZE = 8 * 1024 * 1024

    # fitbit_data_regex = ["*.parquet"]
    regex = "*.parquet"

    data_files = glob.glob(regex)
    if len(data_files) == 0:
        print("No Data Files Found -> uploading example data")
        regex = "/opt/airflow/example_data/" + regex
    
    for blob_name in glob.glob(regex):
        blob = bucket.blob(blob_name)
        blob.chunk_size = CHUNK_SIZE
        
        for attempt in range(max_retries):
            try:
                print(f"Uploading {blob_name} to {bucket_name} (Attempt {attempt + 1}/{max_retries})...")
                blob.upload_from_filename(blob_name)
                
                if storage.Blob(bucket=bucket, name=blob_name).exists(client):
                    print(f"Upload Verification successful for gs://{bucket_name}/{blob_name}")
                    break
                else:
                    print(f"Verification failed for {blob_name}, retrying...")
            except Exception as e:
                print(f"Failed to upload {blob_name} to GCS: {e}")
            
            time.sleep(1)
            
    return


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="fitbit_data_to_gcs_dag",
    schedule_interval="@monthly",
    default_args=default_args,
    catchup=False,
    max_active_runs=3,
    tags=['dtc-de'],
) as dag:
    download_locally_task = PythonOperator(
        task_id="download_locally_task",
        python_callable=download_past_6_months,
        op_kwargs={
            "tokens_path": path_to_local_home,
        },
    )

    fitbit_to_parquet_task = PythonOperator(
        task_id="fitbit_to_parquet_task",
        python_callable=profile_sleep_heartrate_jsons_to_parquet,
        op_kwargs={
            "base_path": path_to_local_home,
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

    download_locally_task >> fitbit_to_parquet_task >> upload_to_gcs_task >> bq_external_profile_table >> bq_external_heartrate_table >> bq_external_sleep_table
