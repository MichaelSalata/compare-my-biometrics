
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
**==NOTE==**: ***Document project steps*** in the [[devlog#Project Step Log]] below

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

- [x] STRETCH: encapsulate dbt core inside a Docker container ✅ 2025-03-22
	- [Airflow with DBT tutorial]](https://www.youtube.com/watch?v=MhCuxTDlVkE)

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


- [ ] ~~get Airflow to automatically start the dag on startup~~

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
- [x] add dev.fitbit project creation image to repo and readme ✅ 2025-03-25
I think t
- add personal data config files to repo
	- [x] add `fitbit_tokens.json` ✅ 2025-03-25
	- [x] add `.env` ✅ 2025-03-25

- [x] add Special Mentions part ✅ 2025-03-26
Thanks to Alexey and his community from [datatalks club](https://datatalks.club/), create this project without the course of [Data Engineering](https://github.com/DataTalksClub/data-engineering-zoomcamp) would have been much more difficult.
- [x] future improvements section ✅ 2025-03-26
	- ~~partition core tables, for performance~~
	- ~~github action for upload spark script to bucket~~
	- Fully normalize the tables as exercise

- [ ] tell user about Partitioning in DBT

### Project Run Instructions
- use [[devlog#Project Step Log]] below
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

- [x] create instructions on how to spin up appropriate GCP resources ✅ 2025-03-24
	- [x] install Terraform, run terraform commands in project terraform directory ✅ 2025-03-24
	- [x] create instructions on launching cloud resources ✅ 2025-03-24

- [x] tell user to download credentials ✅ 2025-03-24
	- What is this used for?
		- point to Terraform IaC
		- point to DBT transformations

- [x] give instructions on ✅ 2025-03-24
	- log with airflow airflow
	- run dag

## PHASE 7 - Better transformations
- [ ] make dag run immediately on start
- [x] download some test intraday data & estimate if that'd warrant PySpark data processing ✅ 2025-03-26
- [ ] look up clustering best practices -> apply them to my schema in DBT
- [ ] create a data mart with intraday transformations 

## Deadlines
### TODOs Submission 1 - 3/31
*aka Goals for 3/31*
### Submission 2 - 4/14
### Interview Ready - 4/30???*

## Rough Edges

- [ ] Create a dag to run immediately on Airflow Startup

- [ ] generate documentation for written functions

- [ ] schedule it to run once a month

- [ ] ensure dbt partitions on dates

- [ ] add data tests in DBT

- [ ] Need a nicer control flow diagram in README
	- [Slack resource discussion](https://datatalks-club.slack.com/archives/C01FABYF2RG/p1743432813320519)
	- Mermaid, JavaScript-based diagramming and charting tool
	- http://draw.io/
	- Lucidchart

- [x] move airflow log-in details to the .env ✅ 2025-03-28

- functionality review/refactor
	- [ ] dag
	- [ ] API download
	- [ ] upload to GCS
	- [ ] docker compose
	- [ ] Dockerfile

- ~~personal data is saved in fitbit_tokens.json and not .env~~
	- 

- [ ] update database dag
	- check latest date in DB
	- download data from that date until now
	- process and update warehouse

- [ ] make pipeline **idempotent

- [x] add more bars to the barchart ✅ 2025-03-24

- [ ] research desired metrics and graphics to visualize
	- look at Google Fit Metrics
	- correlation matrixes?
	- how I used my jupyter notebooks
	- graphics on **[fitbit-web-ui-app](https://github.com/arpanghosh8453/fitbit-web-ui-app)** - github
	- graphics on https://dashboard.exercise.quest/

- [ ] dynamically use user-id in created GCP project/bucket/bigquery dataset with Terraform

- [ ] learn how to cost estimate pipeline
	- gcp financial reports?

- [ ] look at how costs are tracked in GCP
	- add to talking points

## FEATURES
*stuff I don't know how to do yet*
*stuff that requires research/learning/documentation reading*

- [ ] STRETCH: optimize BigQuery Tables
	- Datatalks - wk 3 HW
	- PARTITION, CLUSTER, index?, etc...
	- update dbt references

- [ ] **==look up how I can create a create a service account json with a monetary processing restriction==**
	- add these instructions into the README

- [ ] create a users table with foreign IDs to staged data

- [ ] move stack to cloud

- [ ] integrate Batch Processing with Spark
	- get more Data
		- intraday data
	- [[DataTalks DE Zoomcamp 2025 Syllabus#*Module* 5 Batch Processing - *Spark*]]
	- [DataTalksClub](https://github.com/DataTalksClub)/ [data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)/ [05-batch](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/05-batch "05-batch")
	- [ManuelGuerra1987](https://github.com/ManuelGuerra1987) /  [data-engineering-zoomcamp-notes](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes)  / [5_Batch-Processing-Spark](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/tree/main/5_Batch-Processing-Spark "5_Batch-Processing-Spark")
	- [Spark + Airflow](https://medium.com/doubtnut/github-actions-airflow-for-automating-your-spark-pipeline-c9dff32686b)
	- generate a GB of data and benchmark performance
		- lol this is a spark job in of itself
	- [ ] get a larger dataset analyzed
		- utilize PySpark
		- intraday data
		- find some sort of sleep or heartrate study

- [ ] Make ==Idempotent==
	- [make dbt models incremental](https://docs.getdbt.com/docs/build/incremental-models)
	- dynamic dag to update DB
		- checks if DB empty
			- if so, uploads data since user profile sign-up date to now and processes it
		- if not, check last seen date in DB -> injects/processes data from that date to now
		- ==is this the best practice for Idempotency?==


- [ ] implement CI/CD
	- [Helpful Links from DataTalks](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/projects#helpful-links)
		- [Unit Tests + CI for Airflow](https://www.astronomer.io/events/recaps/testing-airflow-to-bulletproof-your-code/)
		- [CI/CD for Airflow (with Gitlab & GCP state file)](https://engineering.ripple.com/building-ci-cd-with-airflow-gitlab-and-terraform-in-gcp)
		- [CI/CD for Airflow (with GitHub and S3 state file)](https://programmaticponderings.com/2021/12/14/devops-for-dataops-building-a-ci-cd-pipeline-for-apache-airflow-dags/)
		- [CD for Terraform](https://towardsdatascience.com/git-actions-terraform-for-data-engineers-scientists-gcp-aws-azure-448dc7c60fcc)

- Apache Cloudbyte?

# [[Resources]]
# Talking Points
- lack of data governance
## Project Challenges
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
## Cost Tracking
## Design Process
1. develop a schema based on the Data API and Analysis needs
2. incrementally read each technology's documentation and build pipeline
3. implement pipeline steps with key metrics in mind
4. learn from feedback from the course peer review process
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