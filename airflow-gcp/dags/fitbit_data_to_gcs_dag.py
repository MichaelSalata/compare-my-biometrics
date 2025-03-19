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

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "dtc-de-446723")
GCP_GCS_BUCKET = os.environ.get("GCP_GCS_BUCKET", f"{PROJECT_ID}-fitbit-bucket")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'fitbit_dataset2')
CREDENTIALS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH", "/.google/credentials/google_credentials.json")


def upload_to_gcs(bucket_name, max_retries=3):
    client = storage.Client()
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    bucket = client.bucket(bucket_name)
    CHUNK_SIZE = 8 * 1024 * 1024

    fitbit_data_regex = ["profile*.json", "heartrate*.json", "sleep*.json"]
    for regex in fitbit_data_regex:
        for blob_name in glob.glob(regex):
            blob = bucket.blob(blob_name)
            blob.chunk_size = CHUNK_SIZE
            
            for attempt in range(max_retries):
                try:
                    print(f"Uploading {blob_name} to {bucket_name} (Attempt {attempt + 1})...")
                    blob.upload_from_filename(blob_name)
                    print(f"Uploaded: gs://{bucket_name}/{blob_name}")
                    
                    if storage.Blob(bucket=bucket, name=blob_name).exists(client):
                        print(f"Verification successful for {blob_name}")
                        return
                    else:
                        print(f"Verification failed for {blob_name}, retrying...")
                except Exception as e:
                    print(f"Failed to upload {blob_name} to GCS: {e}")
                
                time.sleep(2)  
            
            print(f"Giving up on {blob_name} after {max_retries} attempts.")


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@monthly",
    default_args=default_args,
    catchup=False,
    max_active_runs=3,
    tags=['dtc-de'],
) as dag:
    # TODO: adapt this to my download_locally
    download_locally = PythonOperator(
        task_id="download_locally",
        python_callable=download_past_6_months,
    )

    # TODO: adapt this to my fitbit_json_to_parquet
    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet",
        python_callable=profile_sleep_heartrate_jsons_to_parquet
    )

    local_to_gcs = PythonOperator(
        task_id="local_to_gcs",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket_name": GCP_GCS_BUCKET
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

    download_locally >> format_to_parquet_task >> local_to_gcs >> [bq_external_profile_table, bq_external_heartrate_table, bq_external_sleep_table]
