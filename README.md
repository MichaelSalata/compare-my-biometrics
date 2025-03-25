# Goals
- Visualize changes in fitbit biometrics across time periods
	- **WHY**: my fitbit wellness report has been broken for months and I would like to see how activities impact my health
	- **Example Use Cases**: see the impact of a...
		- fitness routine
		- medication
		- stressful life event
- Practice building a robust and scalable data pipeline with each technology's best practices
	1. develop a schema based on the Data API and Analysis needs
	2. incrementally read each technology's documentation and build pipeline
	3. implement pipeline steps with key metrics in mind
	4. learn from feedback from the course peer review process

- Meet submission deadlines for [DataTalks.club 2025 Course Schedule](https://courses.datatalks.club/de-zoomcamp-2025/)

# Results - Overview
![Data Pipeline visualized](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/orchestration_visualized.png)

1. **Download Fitbit Data** – Retrieves biometric data from the Fitbit API and stores it locally in JSON format.
2. **Flattens JSON Tables and Converts Parquet** – Transforms the locally stored JSON files into Parquet format for optimized storage, transmission, and processing.
3. **Upload Data to Google Cloud Storage (GCS)** – Transfers the Parquet files to GCS for centralized cloud storage and accessibility.
4. **Create BigQuery Profile, Heart Rate and Sleep Table** – Establishes an external BigQuery table for user profiles, sleep data and heart rate data stored in GCS.
5. **Transform Data with dbt** – Applies SQL-based transformations in BigQuery using dbt to clean, standardize, and prepare data for analysis.

- [Looker Studio Data Presentation](https://lookerstudio.google.com/reporting/62d48d66-0361-4d53-9927-ed9a604cafd9/page/30qCF)
![Looker Studio Preview](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/Screenshot%20from%202025-03-24%2020-08-14.png)

## Technologies Used
- **Python** to **connect and download** from the Fitbit API and **reformat** the downloaded json files to parquet
- **Apache Airflow** *orchestrates and schedules* download, reformatting, upload, database transfer and SQL transformation.
- **PostgreSQL** provides Airflow a **database to store workflow metadata** about DAGs, tasks, runs, and other elements
- **Google BigQuery** to **process data analytics**.
- **dbt (Data Build Tool)** injects SQL **data transformations** into BigQuery and enables software management tools to better maintain SQL code 
- **Docker** encapsulates the pipeline ensuring portability, and scalable.

# Building the Project Yourself
## Requirements
[Docker](https://docs.docker.com/get-docker/),  [Docker Compose](https://docs.docker.com/compose/install/) v2,  [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform),  [Google Cloud Platform Project](https://console.cloud.google.com/),  

## SETUP
### Clone this Repository
```bash
gh repo clone MichaelSalata/compare-my-biometrics
cd compare-my-biometrics
```

### OPTIONAL: [Use YOUR Fitbit Data](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/Include-Your-Fitbit-Data.md)
**NOTE:** By default, the project uses [my example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data)  spanning **11-21-2024**  to  **3-16-2025**

### Setup a Service Account for a GCP Project 
- create a service account and download a .json key file
	1. GCP Dashboard -> IAM & Admin > Service accounts > Create service account
	2. set a name & Leave all other fields with default values -> Create and continue
	3. Grant the Viewer role (Basic > Viewer) -> Continue -> Done
	4. 3 dots below Actions -> Manage keys -> Add key -> Create new key -> JSON -> Create

### Set **Project Name** and the **path to your  .json key file**
#### Option 1: bash script
replace `GOOGLE_CREDENTIALS` and `GCP_PROJECT_ID` with yours and run this script.
```bash
#!/bin/bash
GOOGLE_CREDENTIALS="/the/path/to/your/gcp-credentials.json"
GCP_PROJECT_ID="your_project_name"

# Perform replacements in airflow-gcp/.env and terraform/variables.tf
sed -i "s|/home/michael/.google/credentials/google_credentials.json|$GOOGLE_CREDENTIALS|g" "airflow-gcp/.env"
sed -i "s|dtc-de-446723|$GCP_PROJECT_ID|" "airflow-gcp/.env"
sed -i "s|dtc-de-446723|$GCP_PROJECT_ID|" "terraform/variables.tf"
```
#### Option 2: Manual Variable setting
- `airflow-gcp/.env` -> set `GOOGLE_CREDENTIALS=/the/path/to/your/gcp-credentials.json` 
- `airflow-gcp/.env` -> set `GCP_PROJECT_ID=your_project_name`
- `terraform/variables.tf` -> `variable "project"` -> `default = your-projects-name`

**NOTE:** changing `GCP_GCS_BUCKET` and/or `BIGQUERY_DATASET` requires updating `terraform/variables.tf` file

# Usage
## create cloud infrastructure
```
cd terraform
terraform init
terraform apply
```
## Build the Image
```bash
DOCKER_BUILDKIT=1 docker compose build
```
*NOTE*: building the Docker image may take a LONG time
## Run the Image
```bash
docker compose up airflow-init && docker compose up -d
```
## Run the Airflow Dag
visit [localhost:8080](http://localhost:8080/)
log into Airflow with user:pass = airflow:airflow
run the dag 

# Future Goals
- [ ] get the project **hosted in the cloud** solution
- [ ] make **Idempotent**
- [ ] implement **CI/CD**
- [ ] **expose my BigQuery DB**
	- (allowing connections from tools like PowerBI, Metabase, Looker Studio)
