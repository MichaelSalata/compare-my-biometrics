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
==TECH LIST HERE==

# Building the Project Yourself
## Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) v2
- [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform)

## Installation


### Clone this repo to your computer

```bash
git clone <repo-url>
cd <repo-dir>
```

### OPTIONAL: Include Your Fitbit Data
By default, the project uses [my example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data)  spanning **11-21-2024**  to  **3-16-2025**

#### Get your CLIENT_ID and CLIENT_SECRET
- [dev.fitbit.com](https://dev.fitbit.com/) > Manage > [Register An App](https://dev.fitbit.com/apps/new/) > [Log in](https://dev.fitbit.com/login)
	- `Continue with Google` if you use your google account
	- **IMPORTANT**: mark the project `Personal` and use Callback URL `http://127.0.0.1:8080/`
	- [example image](https://miro.medium.com/v2/resize:fit:720/format:webp/1*UJHMOYsFZvrBmpNjFfpBJA.jpeg)

#### Get your ACCESS_TOKEN
OPTION 1:
- run this in the dag directory
```bash
python3 /dags/gather_keys_oauth2.py CLIENT_ID CLIENT_SECRET
```
- replace CLIENT_ID and CLIENT_SECRET with what was shown on your app
- this writes `fitbit_tokens.json` in it the dag directory

 	- stores your fitbit authentication tokens locally (in `/dags/fitbit_tokens.json`) 
  	- allows your data to be downloaded for analysis
   	- `python3 /gather_keys_oauth2.py` may need to be rerun later when your access token expires
	   	- note: it reuses CLIENT_ID and CLIENT_SECRET which get stored in `fitbit_tokens.json`

### Setting up google cloud
- create a service account
- download credentials for service account
- Set personal variables in the `.env` file


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
