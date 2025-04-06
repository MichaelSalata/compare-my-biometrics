# Goals
- Visualize changes in fitbit biometrics across time periods
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

- Meet submission deadlines for [DataTalks.club 2025 Course Schedule](https://courses.datatalks.club/de-zoomcamp-2025/)

# Results - Overview
![Data Pipeline visualized](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/orchestration_visualized.png)

1. **Download Fitbit Data** – Retrieves biometric data from the Fitbit API and stores it locally in JSON format.
2. **Flattens JSON Tables and Converts Parquet** – Transforms the locally stored JSON files into Parquet format for optimized storage, transmission, and processing.
3. **Upload Data to Google Cloud Storage (GCS)** – Transfers the Parquet files to GCS for centralized cloud storage and accessibility.
4. **Create BigQuery Profile, Heart Rate and Sleep Table** – Establishes an external BigQuery table for user profiles, sleep data and heart rate data stored in GCS.
5. **Transform Data and Partition BigQuery with dbt** – Inject SQL-based transformations to BigQuery to clean, standardize, and prepare data for analysis.

## [Looker Studio Data Presentation](https://lookerstudio.google.com/reporting/62d48d66-0361-4d53-9927-ed9a604cafd9/page/30qCF)
![Looker Studio Preview](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/Screenshot%20from%202025-03-24%2020-08-14.png)

## Technologies Used
- **Python** to **connect and download** from the Fitbit API and **reformat** the downloaded json files to parquet
- **Apache Airflow** *orchestrates and schedules* download, reformatting, upload, database transfer and SQL transformation.
- **PostgreSQL** provides Airflow a **database to store workflow metadata** about DAGs, tasks, runs, and other elements
- **Google BigQuery** to **process data analytics**. **Table partitioning is done the dbt staging process**
- **dbt (Data Build Tool)** injects SQL **data transformations** into BigQuery and enables software management tools to better maintain SQL code
- **Docker** encapsulates the pipeline ensuring portability, and scalable.

# Setup and Usage
## Requirements
[Docker](https://docs.docker.com/get-docker/),  [Docker Compose](https://docs.docker.com/compose/install/) v2,  [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform),  [Google Cloud Platform Project](https://console.cloud.google.com/),  

## SETUP Locally
### Clone this Repository
```bash
gh repo clone MichaelSalata/compare-my-biometrics
cd compare-my-biometrics
```

### OPTIONAL: [Use YOUR Fitbit Data](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/Use-Your-Fitbit-Data.md)
**NOTE:** By default, the project uses [my example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data)  spanning **11-21-2024**  to  **3-16-2025**

### Setup a Service Account for a GCP Project 
- create a service account and download a .json key file
	1. GCP Dashboard -> IAM & Admin > Service accounts > Create service account
	2. set a name & Leave all other fields with default values -> Create and continue
	3. Grant the Viewer role (Basic > Viewer) -> Continue -> Done
	4. 3 dots below Actions -> Manage keys -> Add key -> Create new key -> JSON -> Create
	5. Enable these APIs
		- [IAM API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
		- [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)

### Set **Project Name** and the **path to your  .json key file**
#### OPTION 1: bash script
assign `GOOGLE_CREDENTIALS` and `GCP_PROJECT_ID`  and run this script in the project folder
```bash
#!/bin/bash
GOOGLE_CREDENTIALS="/the/path/to/your/gcp-credentials.json"
GCP_PROJECT_ID="your_project_name"

sed -i "0,/\/home\/michael\/.google\/credentials\/google_credentials.json/s|/home/michael/.google/credentials/google_credentials.json|$GOOGLE_CREDENTIALS|" "airflow-gcp/.env"
sed -i "0,/dtc-de-446723/s|dtc-de-446723|$GCP_PROJECT_ID|" "airflow-gcp/.env"
sed -i "0,/dtc-de-446723/s|dtc-de-446723|$GCP_PROJECT_ID|" "terraform/variables.tf"
```
#### OPTION 2: Manual Variable setting
- `airflow-gcp/.env` -> set `GOOGLE_CREDENTIALS=/the/path/to/your/gcp-credentials.json` 
- `airflow-gcp/.env` -> set `GCP_PROJECT_ID=your_project_name`
- `terraform/variables.tf` -> `variable "project"` -> `default = your-projects-name`

***NOTE*:** changing `GCP_GCS_BUCKET` and/or `BIGQUERY_DATASET` requires updating `terraform/variables.tf` file

## Usage Locally
### create cloud infrastructure
```
cd terraform
terraform init
terraform apply
```
***NOTE**:* remember to run `terraform destroy `after you're done
### Build the Docker Image
```bash
cd airflow-gcp/
DOCKER_BUILDKIT=1 docker compose build
```
***NOTE***: building the Docker image may take a LONG time
### Run the Docker Image
```bash
cd airflow-gcp/
docker compose up airflow-init && docker compose up -d
```
***NOTE**:* starting the image takes ~15 minutes
### Run the Airflow Dag
1. visit [localhost:8080](http://localhost:8080/)
2. log into Airflow (default user:pass = airflow:airflow)
3. run the dag
## Turn off, Remove Docker Images, Destroy Cloud Infrastructure
```bash
docker compose down --volumes --rmi all
terraform destroy
```

## Cloud Setup

### Setup a Service Account for a GCP Project 
- create a service account and download a .json key file
	1. GCP Dashboard -> IAM & Admin > Service accounts > Create service account
	2. set a name & Leave all other fields with default values -> Create and continue
	3. Grant the Viewer role (Basic > Viewer) -> Continue -> Done
	4. 3 dots below Actions -> Manage keys -> Add key -> Create new key -> JSON -> Create
	5. Enable the [IAM API](https://console.cloud.google.com/apis/library/iam.googleapis.com) and the [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)
- Set Google Compute VM permissions
	1. find your service account at [IAM Cloud UI](https://console.cloud.google.com/iam-admin/iam) 
	2. `+Add another role` and add
		- Compute **Instance** Admin
		- Compute **Network** Admin
		- Compute **Security** Admin
	3. Enable the [Compute Engine API](https://console.cloud.google.com/apis/library/compute.googleapis.com)

## Start Compute Instance
- find service credentials
	- put path to credentials in .env
	- OR put credentials file in local dir

### assign  `.env` and `terraform.tfvars` variables
generate an ssh keys and add the file paths and username to `terraform/terraform.tfvars`
```bash
ssh-keygen -t rsa -b 2048 -C "your-email@example.com"
# Follow the prompts to specify the file in which to save the key
```
example `terraform/terraform.tfvars` variables...
```
...
ssh_user = "tatlreach" # email without @gmail.com
public_ssh_key_path = "~/.ssh/id_rsa.pub"
private_ssh_key_path = "~/.ssh/id_rsa"
```



from service credentials.json?
NOTE: overwrite/remove `AIRFLOW_UID`?
NOTE: if you're from the EU you mey need to reassign `region` and/or `location` in terraform.tfvars


- terraform init && terraform apply
	- pushes credentials, terraform.tfvars, fitbit_tokens.json to gcloud instance
	- remote execute setup script
	- **NOTE**: terraform deploying ~20 minutes, if you'd like you can Visit your VM in the meantime

## **OPTIONAL**: Visit your VM instance and/or Visit the Airflow Webserver

OPTION 1:
- get your Compute Instance VM's external IP in [your Google VM instances](https://console.cloud.google.com/compute/instances)
- visit that IP on port 8080 e.g.
OPTION 2:
- run `visit_8080_on_vm.sh` in `./setup_scripts`

# Special Thanks
Thanks to [Alexey](https://github.com/alexeygrigorev), [Manuel](https://github.com/ManuelGuerra1987) and the [Datatalks Club](https://datatalks.club/) community. Their [Data Engineering Course](https://github.com/DataTalksClub/data-engineering-zoomcamp) was instrumental in creating this project.

# Future Goals
- [ ] get the project **hosted in the cloud**
- [ ] make **Idempotent**
- [ ] implement **CI/CD**
- [ ] **expose my BigQuery DB**
	- (allowing connections from tools like PowerBI, Metabase, Looker Studio)
- [ ] handle secure user data with [Airflow Secrets](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/index.html)
