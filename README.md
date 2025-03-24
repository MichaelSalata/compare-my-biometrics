# Goals
- Visualize changes in health across time periods
	- **WHY**: my fitbit wellness report is currently broken and I would like to see activities impact my health
		- fitness
		- medications
		- stressful life events
- Meet [DataTalks Engineering Course Project Evaluation Criteria](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/projects#evaluation-criteria)
- Practice building data pipelines with the [DataTalks.club Data Engineering Course](https://github.com/DataTalksClub/data-engineering-zoomcamp)
	- read each technology's documentation and best practices
	- implement features to accomplish goals
	- receive and implement feedback through the course's peer review process

# Constraints
- Meet submission deadlines for [DataTalks.club 2025 Course Schedule](https://courses.datatalks.club/de-zoomcamp-2025/)
	- meetings with real clients and and gathering data for a novel project can balloon out the time commitment

# Results - Overview
- ==INSERT DATA PIPELINE EXPLAINATION HERE==
	- image

- [Looker Studio Data Presentation](https://lookerstudio.google.com/reporting/08b71d97-dc73-4d66-a694-e027c0d68330)

## Technologies Used


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
By default, the project uses [example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data) for 1 user spanning **11-21-2024**  to  **3-16-2025**

#### Get a CLIENT_ID and CLIENT_SECRET
- [dev.fitbit.com](https://dev.fitbit.com/) > Manage > [Register An App](https://dev.fitbit.com/apps/new/) > [Log in](https://dev.fitbit.com/login)
	- `Continue with Google` if you use your google account
	- **IMPORTANT**: mark the project `Personal` and use Callback URL `http://127.0.0.1:8080/`
	- [example image](https://miro.medium.com/v2/resize:fit:720/format:webp/1*UJHMOYsFZvrBmpNjFfpBJA.jpeg)

#### Find your ACCESS_TOKEN
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

