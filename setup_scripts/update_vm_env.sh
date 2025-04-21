#!/bin/bash

TFVARS_FILE=~/compare-my-biometrics/terraform/terraform.tfvars
ENV_FILE=~/compare-my-biometrics/airflow-gcp/.env

project=$(grep '^project' "$TFVARS_FILE" | awk -F'=' '{print $2}' | tr -d ' "')
ssh_user=$(grep '^ssh_user' "$TFVARS_FILE" | awk -F'=' '{print $2}' | tr -d ' "')
bucket_name=$(grep '^gcs_bucket_name' "$TFVARS_FILE" | awk -F'=' '{print $2}' | tr -d ' "')
bq_dataset_name=$(grep '^bq_dataset_name' "$TFVARS_FILE" | awk -F'=' '{print $2}' | tr -d ' "')

AIRFLOW_UID=$(id -u)
GOOGLE_CREDENTIALS="/home/${ssh_user}/google_credentials.json"
GCP_PROJECT_ID="$project"
GCP_GCS_BUCKET="$bucket_name"
BIGQUERY_DATASET="$bq_dataset_name"

# insert/overwrite key-value pairs in .env
update_env_var() {
    local key=$1
    local value=$2
    if grep -q "^${key}=" "$ENV_FILE"; then
        sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
    else
        echo "${key}=${value}" >> "$ENV_FILE"
    fi
}

update_env_var "AIRFLOW_UID" "$AIRFLOW_UID"
update_env_var "GOOGLE_CREDENTIALS" "$GOOGLE_CREDENTIALS"
update_env_var "GCP_PROJECT_ID" "$GCP_PROJECT_ID"
update_env_var "GCP_GCS_BUCKET" "$GCP_GCS_BUCKET"
update_env_var "BIGQUERY_DATASET" "$BIGQUERY_DATASET"