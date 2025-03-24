**Compare My Biometrics**
-----------------------
# **Goals**:
- Visualize changes in health across time periods
	- **WHY**: my fitbit wellness report is currently broken and I would like to see how these things impact my health
		- new medications
		- exercising
		- stressful life events
- Meet [DataTalks Engineering Course Project Evaluation Criteria](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/projects#evaluation-criteria)
- Learn and Practice building a Data Pipeline pipeline through the [DataTalks.club Data Engineering Course](https://github.com/DataTalksClub/data-engineering-zoomcamp)
	- read each technology's documentation and best practices
	- implement features necessary to accomplish goals
	- receive and implement feedback through the course's peer review process

# **Constraints**
- Meet submission deadlines for DataTalks.club Course Schedule
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

## Installation


### Clone this repo to your computer

```bash
git clone <repo-url>
cd <repo-dir>
```

### OPTIONAL: Include Your Fitbit Data
By default, the project uses example fitbit data in the example_data directory.

#### Steps to use your Fitbit data with the project
##### Find your CLIENT_ID and CLIENT_SECRET
- [dev.fitbit.com](https://dev.fitbit.com/) > Manage > [Register An App](https://dev.fitbit.com/apps/new/) > [Log in](https://dev.fitbit.com/login)
	- `Continue with Google` if you use your google account
	- **IMPORTANT**: mark the project `Personal` and use Callback URL `http://127.0.0.1:8080/`
	- [example image](https://miro.medium.com/v2/resize:fit:720/format:webp/1*UJHMOYsFZvrBmpNjFfpBJA.jpeg)

##### Find your ACCESS_TOKEN

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


### Settings

Set personal variables in the `.env` file

```
AIRFLOW_UID=1000
PG_HOST=pgdatabase
PG_USER=root
PG_PASSWORD=root
PG_PORT=5432
PG_DATABASE=fitbit_db
GOOGLE_CREDENTIALS=/home/michael/.google/credentials/google_credentials.json
GCP_PROJECT_ID=dtc-de-446723
GCP_GCS_BUCKET=dtc-de-446723-fitbit-bucket
BIGQUERY_DATASET=fitbit_dataset
```

### OPTIONAL: .gitignore files with personal data
add `fitbit_tokens.json` to the .gitignore file
```bash
echo "fitbit_tokens.json" >> .gitignore
```


Usage
-----------------------


Extending this
-------------------------

If you want to extend this work, here are a few places to start:

* Generate more features in `annotate.py`.
* Switch algorithms in `predict.py`.
* Add in a way to make predictions on future data.
* Try seeing if you can predict if a bank should have issued the loan.
    * Remove any columns from `train` that the bank wouldn't have known at the time of issuing the loan.
        * Some columns are known when Fannie Mae bought the loan, but not before
    * Make predictions.
* Explore seeing if you can predict columns other than `foreclosure_status`.
    * Can you predict how much the property will be worth at sale time?
* Explore the nuances between performance updates.
    * Can you predict how many times the borrower will be late on payments?
    * Can you map out the typical loan lifecycle?

