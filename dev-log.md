
# Motivations - Why
- my wellness report was broken
- visualize changes in biometrics between timeframe - facilitate the health impact of life changes
	- ADHD meds
	- moving
	- exercising
- practice tech involved the DataTalks bootcamp
- fits in my tight deadline
	- I understand how meetings and gathering data for a novel project can balloon out the time commitment

## Desired Visualizations or Metrics


- Sleep Phases
	- stacked bar chart or line chart over window
	- pie chart
- STRETCH: Heart Rate Exercise Zone Rates
	- stacked bar chart or line chart over window
	- pie chart?
- STRETCH: visualize notable dates
	- notable dates will be put on the graphs as vertical lines

# TODOs
**==NOTE==**: ***Document project steps*** in the [[development-log#Project Step Log]] below

## PHASE 1 - proof of concept
- [x] get ANY data downloaded ✅ 2025-03-08
	- ==hardcore necessary fitbit data to query fitbit api==
		- ~~recreate AWS threaded download/upload script but for fitbit API:~~
			- `/home/michael/Documents/projects/datatalks-data-engineering-hw-notes/04-analytics-engineering/load_taxi_data_4analytics.py` 
			- `ec2_load_taxi_data_4analytics.py`

## PHASE 2 - get the RIGHT Data
- [x] download LOTS of data ✅ 2025-03-13
	- multiple months worth
	- multiple dimensions
	- fact table data
- [x] format .json data into something Big Query can handle  (.csv, .parquet) ✅ 2025-03-09
- [ ] ensure I have data similar to ny_taxi data
	- df.info() for ny_taxi_data
	- check data types of key Visualizations and DBT aggregations
- ~~upload the data onto EC2 server~~

## PHASE 3 - move data to new GCP project, Bucket & BigQuery
- [x] move data to ECS ✅ 2025-03-12
- [ ] setup new GCP *account*, project, Bucket & BigQuery
- [x] setup a Terraform  config to launch, apply, destroy it ✅ 2025-03-12

- [x] upload the data ✅ 2025-03-12

## PHASE 4 - Process the Data
 [data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main) / [03-data-warehouse](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse)
ManuelGuerra - [data-engineering-zoomcamp-notes](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/tree/main) /  [3_Data-Warehouse](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/tree/main/3_Data-Warehouse)
[[SQL Resource#BigQuery]]

- [x] Big Query commands to make tables from the data in Bucket ✅ 2025-03-13
- [ ] STRETCH: optimize BigQuery Tables
	- PARTITION, CLUSTER, index?, etc...
	- update dbt references

- [x] setup DBT account ✅ 2025-03-13
- [x] attach DBT to cloned git repo ✅ 2025-03-13
- [x] copy DBT folder to project folder ✅ 2025-03-13

- [x] look at data and plan schema ✅ 2025-03-17
	- what kinda charts do I want?
	- what kinda charts were showcased?

- STRETCH: migrate to dbt-core
	- [ ] install - [website instructions](https://docs.getdbt.com/docs/core/installation-overview)
	- [ ] install BigQuery Adapter
		- [website instructions](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup)

- [ ] STRETCH: encapsulate dbt core inside a Docker container

- [ ] STRETCH: integrate dbt into airflow - [Airflow with DBT tutorial]](https://www.youtube.com/watch?v=MhCuxTDlVkE)

- [x] update dbt_resources to incorporate sleep & heartrate tables ✅ 2025-03-17
	- [x] dbt_project.yml ✅ 2025-03-17
	- [x] stage files ✅ 2025-03-17

- [x] properly cast data from sleep & heartrate ✅ 2025-03-17

- [x] combine data into fact table ✅ 2025-03-17

- [ ] STRETCH: create datamart for visualization


## PHASE 5 - Looker Studio Visualizations

->  [data-engineering-zoomcamp-notes](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes) / [4_Analytics-Engineering](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/tree/main/4_Analytics-Engineering#visualising-the-transformed-data)

- [x] stacked bar chart for sleep stages ✅ 2025-03-17
- [x] aggregated statistics on heartrate over the time period ✅ 2025-03-17

- [x] stacked bar chart heartrate zones ✅ 2025-03-17

- [ ] create distribution visualization
## PHASE 5.5 - Stretch Orchestration
- [x] fix broken DAG error ✅ 2025-03-18

- Goal
	- adapt existing Airflow orchestration to compare-my-biometrics pipeline
	- ***aka*** generalize existing Airflow scripts to read from environment variables

request_biometrics  |  `upload_to_datalake >> data_warehouse_transfer`

- [x] encapsulate Airflow in Docker ✅ 2025-03-18

- [x] fix download_locally script not finding fitbit_tokens ✅ 2025-03-20
- [x] generalize hardcoded fitbit credentials mounting on Docker container


- [ ] get Airflow to automatically start the dag on startup

### for each stage
- get variables needed
	- encode variables in environment or json file
	- hard code variables not able to be passed
- determine packages necessary to run  stage/Airflow Operators

- test script on example fitbit data

- [x] download_locally ✅ 2025-03-20
- [x] upload ✅ 2025-03-20
- [x] transfer to warehouse (BigQuery) ✅ 2025-03-20
- [x] transfer to warehouse (BigQuery) ✅ 2025-03-20
#### download_locally needs
- MY fitbit_tokens.json
	- user_id
	- client_id
	- client_secret
	- access_token
	- scope
- recognize example data?
	- put "example" in like fitbit_tokens.json : user_id
	- have fitbit_tokens_example.json?

- [x] remove demo from bucket and dataset ✅ 2025-03-20
- [x] remove extra dependencies for running the airflow container ✅ 2025-03-20
### STRETCH STRETCH - orchestrate dbt core
request_biometrics  |  `upload_to_datalake >> data_warehouse_transfer >> dbt_transformations`

- [ ] see how other people orchestrate dbt
	- how do they handle dbt files being in other directories?
		- mount???????
- [x] add bash operator import ✅ 2025-03-20
from airflow.operators.bash import BashOperator
#### [steam-data-engineering](https://github.com/VicenteYago/steam-data-engineering/tree/main)
- steam-data=engineering
	- bash command - [steam ingest reviews](https://github.com/VicenteYago/steam-data-engineering/blob/main/airflow/dags/custom_dags/reviews_ingest_dag.py)
		- DBT_DIR = os.path.join(AIRFLOW_HOME, "dbt")
		- BashOperator

```python
	run_dbt_task = BashOperator(
	task_id='run_dbt',
	bash_command=f'cd {DBT_DIR} && dbt run --profile airflow',
	trigger_rule="all_success"
	)
```

- requirements.txt has
	- apache-airflow-providers-google
	- pyarrow
	- kaggle
	- dbt-bigquery
	- pandas?????
-  volumes:
	- ./dags:/opt/airflow/dags
	- ./logs:/opt/airflow/logs
	- ./plugins:/opt/airflow/plugins
	- ../dbt:/opt/airflow/dbt
	- /home/vyago-gcp/.google/credentials/:/.google/credentials:ro
	- /home/vyago-gcp/.dbt:/home/airflow/.dbt:ro
#### [ShowPulse_Ticketmaster](https://github.com/nburkett/ShowPulse_Ticketmaster/tree/main)

- compose volumns
	- ../dbt:/dbt
    - ~/.dbt:/home/airflow/.dbt:ro
- requirements
	- apache-airflow-providers-google
	- pyarrow
	- pandas
	- dbt-bigquery

#### OTHER
lixx21 repo - [airflow-dbt-gcp](https://github.com/lixx21/airflow-dbt-gcp)
ng-hiep repo - [airflow-dbt-gcp-datapipeline](https://github.com/ng-hiep/airflow-dbt-gcp-datapipeline)

- [x] get dbt the profile info ✅ 2025-03-21
- [x] pip install dbt & it's requirements ✅ 2025-03-21
- [x] only orchestrate on trigger_rule="all_success" ✅ 2025-03-21
    

### get dbt to run in Airflow image


## PHASE 6 - Assemble the README

- [ ] RESOURCES:
	- [jorge's README](https://github.com/JorgeAbrego/weather_stream_project) as a blueprint
	- manuel's README
	- data proj draft README

**WHAT PROBLEM DOES IT SOLVE**? - course project req
- [ ] add dev.fitbit project creation image to repo and readme

- add personal data config files to repo
	- [ ] add `fitbit_tokens.json`
	- [ ] add `.env` 

- [ ] add Special Mentions part 
Thanks to Alexey and his community from [datatalks club](https://datatalks.club/), create this project without the course of [Data Engineering](https://github.com/DataTalksClub/data-engineering-zoomcamp) would have been much more difficult.
- [ ] future improvements section
	- ~~partition core tables, for performance~~
	- Add a cost analysis of a full pipeline run
	- extract more value from steam reviews --> new dashboard ?
	- USE CASE: matrix factorization for recommendations
	- ~~github action for upload spark script to bucket~~
	- More tests on the pipeline
	- Fully normalize the tables as exercise


- [ ] tell user about Partitioning in DBT

### Project Run Instructions
- use [[development-log#Project Step Log]] below
- Terraform
- Docker
- GCP creation & permissions for (project, bucket, dataset)
- test instructions

- [x] add example data to project ✅ 2025-03-23
	- [x] anonymize example data ✅ 2025-03-23
	- [x] env ✅ 2025-03-24
	- [x] fitbit_tokens ✅ 2025-03-23
- [x] tell user about date range for example data ✅ 2025-03-23
- [x] instruct user on running the gather_tokens script in the hardcoded location ✅ 2025-03-24

- [x] instructions on how the docker command to run it ✅ 2025-03-24

- [ ] create instructions on how to spin up appropriate GCP resources
	- [ ] install Terraform, run terraform commands in project terraform directory
	- [ ] create instructions on launching cloud resources

- [ ] tell user to put their google credentials in xyz location
	- What is this used for?
		- point to Terraform IaC
		- point to DBT transformations

- [ ] give instructions on
	- log with airflow airflow
	- run dag

### STRETCH
- [ ] make dag run immediately on start
	- remove instructions on logging into Airflow
	- OPTIONAL: Log in and explore airlfow, explore Data in your BigQuery Database with Looker Studio 

- [ ] **==look up how I can create a create a service account json with a monetary processing restriction==**
	- add these instructions into the README

## PHASE 7 - STRETCH post README -> more DBT transformations
?
- [ ] look up clustering best practices -> apply them to my schema in DBT
- [ ] find useful data ratios I can visualize
- [ ] create a data mart -> useful data transformations 

## STRETCH Goals 
*aka Goals:  README-completion _to_ 4/14*
*aka technical debt*

- [ ] add more bars to the barchart

- [ ] add data test in DBT

- integrate Batch Processing with Spark
	- [[DataTalks DE Zoomcamp 2025 Syllabus#*Module* 5 Batch Processing - *Spark*]]
	-  [DataTalksClub](https://github.com/DataTalksClub)/ [data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)/ [05-batch](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/05-batch "05-batch")
	-  [ManuelGuerra1987](https://github.com/ManuelGuerra1987) /  [data-engineering-zoomcamp-notes](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes)  / [5_Batch-Processing-Spark](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/tree/main/5_Batch-Processing-Spark "5_Batch-Processing-Spark")

- [ ] pipeline
	- map `data` directory to Airflow Docker Container
		- change download script to download to data folder
	- [ ] create/reuse upload script most compatible with Airflow
	- request_biometrics >> upload_data_lake >> data_warehouse >> dbt_processing >> looker_studio_dashboard

- [ ] research good graphics
	- look at Google Fit Metrics
	- how I used my jupyter notebooks
	- graphics on **[fitbit-web-ui-app](https://github.com/arpanghosh8453/fitbit-web-ui-app)** - github
	- graphics on https://dashboard.exercise.quest/

- [ ] make pipeline **idempotent
- [ ] schedule it to run once a month**

- [ ] dynamically use user-id in created GCP project/bucket/bigquery dataset with Terraform

- [ ] learn how to cost estimate pipeline
	- gcp financial reports?

# Resources
 [getting fitbit CLIENT_ID and CLIENT_SECRET - gpt](https://chatgpt.com/c/67945566-6294-8008-963e-90d98c8ffd08)

Google Fit has some good charts of emulate
Someone already did a Fitibit Visualization for their Data Engineering Zoomcamp Project

## Fitbit API

[documentation](https://python-fitbit.readthedocs.io/en/latest/#fitbit-api)

[python-fitbit](https://github.com/orcasgit/python-fitbit/tree/master) -  ==[gather_keys_oauth2.py](https://github.com/orcasgit/python-fitbit/blob/master/gather_keys_oauth2.py)==

https://python-fitbit.readthedocs.io/en/latest/#fitbit-api

### [Fitbit OAuth 2.0 Tutorial](https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/)


## [Fitpipe](https://github.com/rickyriled/data_engineering_project_1/tree/main) DE Project
[pt.py](https://github.com/rickyriled/data_engineering_project_1/blob/main/pt.py)


fitbit's CLIENT_ID, CLIENT_SECRET  >  Oauth2 token  >  ACCESS_TOKEN, REFRESH_TOKEN  >  Client


```python
with open("fitbit_login_info.json", "r") as openfile:
    fitbit_info=json.load(openfile)

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(
							 CLIENT_ID,
							 CLIENT_SECRET,
							 oauth2=True, 
							 access_token=ACCESS_TOKEN, 
							 refresh_token=REFRESH_TOKEN)


```

## Fitbit Dashboard by [jlai](https://github.com/jlai)[Jason](https://github.com/jlai)
[dashboard.exercise.quest](https://dashboard.exercise.quest/)
[fitness-dashboard](https://github.com/jlai/fitness-dashboard) - github
[reddit post](https://www.reddit.com/r/fitbit/comments/1eaccv3/fitness_dashboard_an_unofficial_web_dashboard_for/)

## **[fitbit-web-ui-app](https://github.com/arpanghosh8453/fitbit-web-ui-app)** - github
https://fitbit-report.arpan.app/

[online fitbit wellness report website without premium](https://fitbit-report.arpan.app/)
src: [reddit page](https://www.reddit.com/r/fitbit/comments/15igabx/update_i_made_a_website_for_all_fitbit_owners/)  [page2](https://www.reddit.com/r/fitbit/comments/18kq520/i_made_a_website_for_all_fitbit_owners_where_you/)

### dev.fitbit.com
[Fitbit OAuth 2.0 Tutorial](https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/?clientEncodedId=23R3K5&redirectUri=https://localhost:8000/&applicationType=PERSONAL)
[Web API Reference](https://dev.fitbit.com/build/reference/web-api/)

[Collect Your Own Fitbit Data with Python](https://medium.com/towards-data-science/collect-your-own-fitbit-data-with-python-ff145fa10873) - [Stephen Hsu](https://medium.com/@shsu14?source=post_page---byline--ff145fa10873---------------------------------------) medium article

## Device Connect - Google
https://cloud.google.com/device-connect
[github](https://github.com/GoogleCloudPlatform/deviceconnect)

```python
FITBIT_OAUTH_CLIENT_ID = ''                          # fitbit client id (from dev.fitbit.com)
FITBIT_OAUTH_CLIENT_SECRET = ''                  # fitbit secret (from dev.fitbit.com)
```

# Project Challenges
- getting airflow to work??????
- API
	- learning about api's
	- coding the request myself
	- refactoring it
- flattening JSON
- NO INTERNET
- datetime formatting
- maintaining passion through harsh life events
- maintaining data quality with fluctuating project requirements
	- adding in user_id
	- user_id going null
	- datetime format changing
# Progress Log
- Clone [ny-taxi-pipeline](https://github.com/MichaelSalata/ny-taxi-pipeline)
- `gh auth login`
- `git remote set-url origin https://github.com/MichaelSalata/compare-fitbit-periods.git`
- dev.fitbit.com > Manage > [Register An App](https://dev.fitbit.com/apps/new/) > [Log in](https://dev.fitbit.com/login)
	- `Continue with Google` if you use your google account
	- **IMPORTANT**: the project `Personal` and using Callback URL `http://127.0.0.1:8080/`
- ![example app](https://miro.medium.com/v2/resize:fit:720/format:webp/1*UJHMOYsFZvrBmpNjFfpBJA.jpeg)
- insert the sensitive fitbit API tokens into the `fitbit_tokens.json` file
- `pip install fitbit`
- run gather_keys script
- run download_data script
- run format_to_parquet script

- uploading to GCS requires
	- **PROJECT_ID**
		- example .env line:  `GCP_PROJECT_ID=dtc-de-446723`
	- **BUCKET**
		- example .env line:  `GCP_GCS_BUCKET=dtc-de-446723-terraform-demo-bucket

- bigquery_external_table_task
	- requires a dataset
		- example .env line:  `BIGQUERY_DATASET=demo_dataset

- use terraform to....
	- create project, bucket, big query dataset

- moved in terraform folder
- updated google credentials name/location in .tfs
- switched variable names to new project names

- put the data into BigQuery
```PostgreSQL
CREATE OR REPLACE EXTERNAL TABLE dtc-de-446723.fitbit_dataset.external_heartrate

OPTIONS (

format = 'PARQUET',

uris = ['gs://dtc-de-446723-fitbit-bucket/heartrate*.parquet']

);
```

```PostgreSQL
CREATE OR REPLACE EXTERNAL TABLE dtc-de-446723.fitbit_dataset.external_sleep

OPTIONS (

format = 'PARQUET',

uris = ['gs://dtc-de-446723-fitbit-bucket/sleep*.parquet']

);
```

- create a new DBT Cloud project
	- Project subdirectory: dbt_resources
	- Repository
	- git://github.com/MichaelSalata/compare-my-biometrics.git
	- Development connection - BigQuery

- removed a bunch of example files
- added columns and descriptions to schema

- coded staging
- coded fact merging

- create Looker Studio project

- Airflow
	- got download & formatting working with fitbit Auth
	- got BQ upload & SQL injection working with fitbit Auth download
	- got Airflow to find & use example data when no download


- installing dbt-core per [their website instructions](https://docs.getdbt.com/docs/core/installation-overview)

- Looker Studio -> Create -> BigQuery -> project/dataset/table -> Create Report

- found [dbt-bigquer docker image](https://github.com/dbt-labs/dbt-bigquery/pkgs/container/dbt-bigquery)
- pulled dbt-bigquery docker image with `docker pull ghcr.io/dbt-labs/dbt-bigquery:1.9.latest`

- took the docker build files from [dbt-bigquery official repo](https://github.com/dbt-labs/dbt-adapters/tree/main/dbt-bigquery/docker)

- installed dbt-bigquery
	- pip install dbt-core dbt-bigquery
- setup and link ~/.dbt/profile.yml to project and injected SQL code into bq

- airflow orchestrating every step