# Introduction
This is a data pipeline that takes in Fitbit data, uploads it a Data Lake (Google Cloud Storage), copies it into a BigQuery database and injects SQL into BigQuery to create a data schema ready for analysis.
# Goals
- Visualize changes in Fitbit biometrics across time periods
	- **WHY**: my fitbit wellness report has been broken for months and I would like to see how activities impact my health
	- **Example Use Cases**: see the impact of a...
		- fitness routine
		- medication
		- stressful life event
- Practice building a scalable data pipeline with best practices and fault tolerance
	1. develop a schema based on the Data API and Analysis needs
	2. incrementally read each technology's documentation and build pipeline
	3. implement pipeline steps with key metrics in mind
	4. learn from feedback from the course peer review process
- Meet submission deadlines for the [DataTalks.club 2025 Course Schedule](https://courses.datatalks.club/de-zoomcamp-2025/)
# Results - Overview
![Data Pipeline visualized](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/orchestration_visualized.png)

1. **OPTIONALLY Download Your Fitbit Data** – Retrieves biometric data from the Fitbit API and stores it in JSON format.
2. **Flattens JSON Tables and Converts to Parquet** – Transforms the JSON files into Parquet format for optimized storage, transmission, and processing.
3. **Upload Fitbit Data to a Google Cloud Storage Bucket** – Transfers the Parquet files to GCS, utilizing the bucket as a Data Lake.
4. **Create BigQuery Heart Rate, Sleep and Profile Tables** – Creates external BigQuery tables for user profiles, sleep and heart rate data stored in GCS.
5. **Partitions and Transforms Data in BigQuery** – Using DBT, inject SQL-based transformations to BigQuery to clean, standardize, and prepare data for analysis.

## [Looker Studio Data Presentation](https://lookerstudio.google.com/reporting/62d48d66-0361-4d53-9927-ed9a604cafd9/page/30qCF)
[![Looker Studio Preview](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/Screenshot%20from%202025-03-24%2020-08-14.png)](https://lookerstudio.google.com/reporting/62d48d66-0361-4d53-9927-ed9a604cafd9/page/30qCF)

## Technologies Used
- **Python** to **connect and download** from the Fitbit API and **reformat** the downloaded json files to parquet
- **Apache Airflow** *orchestrates and schedules* download, reformatting, upload, database transfer and SQL transformation.
- **PostgreSQL** provides Airflow a **database to store workflow metadata** about DAGs, tasks, runs, and other elements
- **Google BigQuery** to **process data analytics**. **Table partitioning is done in the dbt staging process**
- **dbt (Data Build Tool)** injects SQL **data transformations** into BigQuery. Keeping SQL externally allows version control better to better maintain SQL code.
- **Docker** encapsulates the pipeline ensuring portability.

# Setup and Deploy on Google Cloud
## 1. Requirements
[Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform),  [Google Cloud Platform Project](https://console.cloud.google.com/),  [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)

## 2. Setup a Service Account for a Google Cloud Project
- create a service account and download a .json key file
	1. GCP Dashboard -> IAM & Admin > Service accounts > Create service account
	2. set a name & Leave all other fields with default values -> Create and continue
	3. Grant the Viewer role (Basic > Viewer) -> Continue -> Done
	4. 3 dots below Actions -> Manage keys -> Add key -> Create new key -> JSON -> Create
- **Add Cloud Storage & BigQuery permissions** to your Service Account
	1. find your service account at [IAM Cloud UI](https://console.cloud.google.com/iam-admin/iam) 
	2. use `+Add another role` to add these roles
		- **Storage** Admin
		- **Storage Object** Admin
		- **BigQuery** Admin
		- Viewer
	3. Enable the [IAM API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
	4. Enable the [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)
- **Add Compute VM permissions** to your Service Account
	1. find your service account at [IAM Cloud UI](https://console.cloud.google.com/iam-admin/iam) 
	2. use `+Add another role` to add these roles
		- Compute **Instance** Admin
		- Compute **Network** Admin
		- Compute **Security** Admin
	3. Enable the [Compute Engine API](https://console.cloud.google.com/apis/library/compute.googleapis.com)

## 3. Prepare Terraform to Launch The Project
### 3-a. Clone this Project Locally
```bash
git clone https://github.com/MichaelSalata/compare-my-biometrics.git
```
### 3-b. Create your SSH key
```bash
ssh-keygen -t rsa -b 2048 -C "your_ssh_username@example.com"
```
### 3-c. Fill Out `terraform/terraform.tfvars`
**NOTE**: pick a **unique** `gcs_bucket_name` like  `projectName-fitbit-bucket`
```
credentials          = "/path/to/service_credentials.json"
project              = "google_project_name"
gcs_bucket_name      = "UNIQUE-google-bucket-name"
ssh_user = "your_ssh_username_WITHOUT@example.com"
public_ssh_key_path = "~/path/to/id_rsa.pub"
private_ssh_key_path = "~/path/to/id_rsa"
```
***example***
```
credentials          = "/home/michael/.google/credentials/google_credentials.json"
project              = "dtc-de-1287361"
gcs_bucket_name      = "dtc-de-1287361-fb-bucket"
ssh_user             = "michael"
public_ssh_key_path  = "~/.ssh/id_rsa.pub"
private_ssh_key_path = "~/.ssh/id_rsa"
```
## OPTIONAL: [Use YOUR Fitbit Data](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/Use-Your-Fitbit-Data.md)
Alternatively, you can run the example DAG(`parallel_backfill_fitbit_example_data`) which uses [my example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data)  spanning **11-21-2024**  to  **3-16-2025**
## 4. Launch with Terraform
```bash
cd ./terraform
terraform init
terraform apply
```
## 5. Launch the DAG from Airflow's Webserver
**OPTION 1**:
- run `bash ./setup_scripts/visit_8080_on_vm.sh` 

**OPTION 2**:
- get your Compute Instance's **External IP** in [your Google VM instances](https://console.cloud.google.com/compute/instances)
- visit **External IP**:8080
- choose and run the appropriate DAG

## 6. Close Down Resources
1. Ctrl+C will stop Terraform running
2. These commands will destroy the resources the your services account provisioned
```bash
cd ./terraform
terraform destroy
```

# Special Thanks
Thanks to [Alexey](https://github.com/alexeygrigorev), [Manuel](https://github.com/ManuelGuerra1987) and the [Datatalks Club](https://datatalks.club/) community. Their [Data Engineering Course](https://github.com/DataTalksClub/data-engineering-zoomcamp) was instrumental in creating this project.

# Future Goals
- [x] get the project **hosted in the cloud** ✅ 2025-04-07
- [ ] make **Idempotent**
- [ ] implement **CI/CD**
- [ ] handle secure user data with [Airflow Secrets](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/index.html)
