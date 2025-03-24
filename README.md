INCOMPLETE
---
# Goals
- Visualize changes in health across time periods
	- **WHY**: my fitbit wellness report is currently broken and I would like to see activities impact my health
		- fitness
		- medications
		- stressful life events
- Meet [DataTalks Engineering Course Project Evaluation Criteria](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/projects#evaluation-criteria)
- Practice building data pipelines with the [DataTalks.club Data Engineering Course](https://github.com/DataTalksClub/data-engineering-zoomcamp) and best practices
	1. develop a schema based on the Data API and Analysis needs
	2. incrementally read each technology's documentation and build pipeline
	3. implement pipeline steps with key metrics in mind
	4. learn from feedback from the course peer review process

# Constraints
- Meet submission deadlines for [DataTalks.club 2025 Course Schedule](https://courses.datatalks.club/de-zoomcamp-2025/)

# Results - Overview
- ==INSERT DATA PIPELINE EXPLANATION HERE==
	- image

- [Looker Studio Data Presentation](https://lookerstudio.google.com/reporting/08b71d97-dc73-4d66-a694-e027c0d68330)

## Technologies Used
==TECH LISTED HERE==

# Building the Project Yourself
## Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) v2
- [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform)

## SETUP

### Clone this repo to your computer
```bash
gh repo clone MichaelSalata/compare-my-biometrics
cd compare-my-biometrics
```

### OPTIONAL: [Use YOUR Fitbit Data](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/Include-Your-Fitbit-Data.md)
**NOTE:** By default, the project uses [my example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data)  spanning **11-21-2024**  to  **3-16-2025**

### Setup a Project and Service Account
- create a service account

- download credentials.json for service account

- Set set your project name and and the path to you GCP service account credentials
	- **REQUIRED:**
		- .env -> set `GOOGLE_CREDENTIALS` to the path of your GCP service account credentials 
		- .env -> set `GCP_PROJECT_ID` to `your-projects-name`
		- variables.tf -> variable "project" -> default =  `your-projects-name`
	- **OPTIONAL:** changing `GCP_GCS_BUCKET` and/or `BIGQUERY_DATASET` requires updating variables.tf file

### OPTIONAL: .gitignore files with personal data
add `fitbit_tokens.json` to the .gitignore file
```bash
echo "fitbit_tokens.json" >> .gitignore
```

# Usage
NOTE: building an Airflow Docker image may take a long time
```bash
DOCKER_BUILDKIT=1 docker compose build
```

Run the Docker image
```bash
docker compose up airflow-init && docker compose up -d
```

log into Airflow and run the dag at `localhost:8080`

# Future Goals
- [ ] get the project **hosted in the cloud** solution
- [ ] make **Idempotent**
- [ ] implement **CI/CD**
- [ ] **expose my BigQuery DB**
	- (allowing connections from tools like PowerBI, Metabase, Looker Studio)
