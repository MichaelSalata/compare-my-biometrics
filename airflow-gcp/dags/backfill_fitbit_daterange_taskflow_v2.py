import os
import json

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

from airflow.models import Connection
from airflow.utils.db import provide_session

from airflow.operators.python import get_current_context
from airflow.utils.dates import days_ago

from google.cloud import bigquery

from fitbit_json_to_parquet import flatten_fitbit_json_file
from fitbit_hook import FitbitHook
from airflow.providers.google.cloud.hooks.gcs import GCSHook
# from download_locally import download_past_6_months


PROJECT_ID = str(os.environ.get("GCP_PROJECT_ID"))
GCP_GCS_BUCKET = str(os.environ.get("GCP_GCS_BUCKET", f"{PROJECT_ID}-fitbit-bucket"))
BIGQUERY_DATASET = str(os.environ.get("BIGQUERY_DATASET", "fitbit_dataset"))
# CREDENTIALS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "google_credentials.json")

AIRFLOW_PATH = os.environ.get("AIRFLOW_HOME")
DBT_IS_TEST_RUN = "'{is_test_run: " + str(os.environ.get("IS_DEV_ENV", "False")) + "}'"


@provide_session
def update_fitbit_connection(session=None):

    existing_conn = session.query(Connection).filter(Connection.conn_id == "fitbit_default").first()
    try:
        with open("fitbit_tokens.json", 'r') as tokens_file:
            tokens = json.load(tokens_file)

            # Update connection if it already exists
            if existing_conn:
                print("Connection 'fitbit_default' already exists. Updating access_token...")

                existing_conn.login = tokens["client_id"]
                existing_conn.password = tokens["client_secret"]
                
                extra_kv_tokens = json.loads(existing_conn.extra) if existing_conn.extra else {}
                extra_kv_tokens["access_token"] = tokens.get("access_token", extra_kv_tokens.get("access_token"))
                extra_kv_tokens["user_id"] = tokens.get("user_id")
                existing_conn.extra = json.dumps(extra_kv_tokens)
                print("user_id, client_id, client_secret, access_token and refresh_token updated successfully.")

            else:
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
                print("Connection 'fitbit_default' created successfully.")
            
            session.commit()
            return tokens.get("user_id")
    except FileNotFoundError:
        print(f"fitbit_tokens.json not found")
        if existing_conn:
            print(f"Using existing fitbit connection {existing_conn.conn_id}")
            user_id = json.loads(existing_conn.extra).get("user_id")
        else:
            print("No fitbit connection or tokens to estabilish one!")
            user_id = None

    if os.path.exists("fitbit_tokens.json"):
        try:
            os.remove("fitbit_tokens.json")
        except OSError as e:
            print(f"Error removing fitbit_tokens.json: {e}")
        
    session.commit()
    return user_id


default_args = {
    "owner": "MSalata",             # default: airflow
    "start_date": days_ago(1),
    "depends_on_past": False,       # default: False
    "retries": 2,                   # default: 0
    "FITBIT_BIOMETRICS": ["sleep", "heartrate"]
}


@dag(
    dag_id="backfill_fitbit_from_signup",
    default_args=default_args,
    start_date=days_ago(1),
    catchup=False,
    tags=['dtc-de']
)
def fitbit_pipeline():
    BQ_TABLES = default_args["FITBIT_BIOMETRICS"] + ["profile"]
    update_fitbit_connection()

    @task
    def download_profile():
        fitbit_hook = FitbitHook()
        response = fitbit_hook.fetch_from_endpoint(f"https://api.fitbit.com/1/user/{fitbit_hook.user_id}/profile.json")
        return {
            "json_file": FitbitHook.save_data(response),
            "signup_date": response["memberSince"]
        }
    
    @task
    def get_signup_date(profile_data: dict):
        return profile_data["signup_date"]

    @task
    def get_profile_path(profile_data: dict):
        return profile_data["json_file"]
    
    @task
    def download_since_signup(signup_date: str, endpoint_id: str):
        fitbit_hook = FitbitHook()
        context = get_current_context()
        end_date = context['execution_date'].date().isoformat()
        # end_date = {{start_date}}   # jinja references the when the task starts
        if endpoint_id in fitbit_hook.dayrange_endpoints:
            response = fitbit_hook.fetch_daterange(endpoint_id, start=signup_date, end=end_date)
            if response:
                return fitbit_hook._save_data(response, endpoint_id, start_date=signup_date, end_date=end_date)
            else:
                print(f"No data retrieved for {endpoint_id} from {signup_date} to {end_date}") 

    @task
    def flatten_fitbit_json(json_file: str):
        parquet_file, endpoint_id = flatten_fitbit_json_file(json_file)
        return {"filename": parquet_file, "endpoint_id": endpoint_id}


    @task
    def upload_to_gcs(filename: str, endpoint_id: str):
        gcp_blob = f"{endpoint_id}/{filename}"
        print(f"Uploading {filename} to {gcp_blob}...")
        gcs_hook = GCSHook()
        gcs_hook.upload(bucket_name=GCP_GCS_BUCKET, object_name=gcp_blob, filename=filename)
        print(f"Upload successful to {gcp_blob}")
        return gcp_blob

    @task
    def create_bq_table(endpoint_id: str):
        client = bigquery.Client()

        table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}.external_{endpoint_id}"

        table = bigquery.Table(table_id)
        external_config = bigquery.ExternalConfig(source_format=bigquery.SourceFormat.PARQUET)
        external_config.source_uris = [f"gs://{GCP_GCS_BUCKET}/{endpoint_id}/{endpoint_id}*.parquet"]

        table.external_data_configuration = external_config

        table = client.create_table(table, exists_ok=True)

        return endpoint_id

    # signup_date, profile_json, user_id = get_profile_data()
    profile_data = download_profile()
    flattened_profile = flatten_fitbit_json(json_file=profile_data.output["json_file"])
    profile_parquets_in_gcs = upload_to_gcs(**flattened_profile)

    biometric_jsons = download_since_signup.partial(signup_date=profile_data.output["signup_date"]).expand(endpoint_id=default_args["FITBIT_BIOMETRICS"])
    biometric_parquets = flatten_fitbit_json.expand(json_file=biometric_jsons)
    profile_biometrics_in_gcs = upload_to_gcs.expand_kwargs(biometric_parquets)

    setup_bq_ext_tables = create_bq_table.expand(endpoint_id=BQ_TABLES)

    [profile_biometrics_in_gcs, profile_parquets_in_gcs, setup_bq_ext_tables] >> BashOperator(
        bash_command=f"cd {AIRFLOW_PATH}/dbt_resources && dbt deps && dbt build --vars {DBT_IS_TEST_RUN}",
        trigger_rule="all_success"
    )

fitbit_dag = fitbit_pipeline()