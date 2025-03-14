
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

# Available Health Metrics/Data
- Height
- Weight
- Body Fat
- Heart rate
- Resting Heart rate
- Sleep
- Activity
	- Distance
	- Elevation Gain
	- Exercise
	- Floors Climbed
	- Speed
	- Steps
	- Total calories burned

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

- [ ] look at data and plan schema
	- what kinda charts do I want?
	- what kinda charts were showcased?

- [ ] update dbt_resources to incorporate sleep & heartrate tables
	- [ ] packages.yml
	- [ ] dbt_project.yml
	- [ ] stage files

- [ ] properly cast data from sleep & heartrate

- [ ] combine data into fact table

- [ ] create datamart for visualization

## PHASE 5 - Looker Studio Visualizations

->  [data-engineering-zoomcamp-notes](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes) / [4_Analytics-Engineering](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/tree/main/4_Analytics-Engineering#visualising-the-transformed-data)

- [ ] stacked bar chart for sleep stages
- [ ] aggregated statistics on heartrate over the time period

- [ ] stacked bar chart heartrate zones
- [ ] aggregated statistics on heartrate over the time period


## PHASE 6 - Assemble the README
RESOURCE: utilize [jorge's README](https://github.com/JorgeAbrego/weather_stream_project) as a blueprint

### Project Assembly instructions
- use [[development-log#Project Step Log]] below
- Terraform
- Docker
- GCP creation & permissions for (project, bucket, dataset)
- test instructions

## STRETCH Goals 
*aka Goals:  3/24 -to- 4/21*
*aka technical debt*

- [ ] pipeline
	- map `data` directory to Airflow Docker Container
		- change download script to download to data folder
	- [ ] create/reuse upload script most compatible with Airflow
	- request_biometrics >> upload_data_lake >> data_warehouse >> dbt_processing >> looker_studio_dashboard

- [ ] **run upload script with an Airflow pipeline**
	- make it **idempotent**
	- schedule it to run once a month

- [ ] dynamically use user-id in created GCP project/bucket/bigquery dataset with Terraform

- [ ] research good graphics
	- look at Google Fit Metrics
	- how I used my jupyter notebooks
	- graphics on **[fitbit-web-ui-app](https://github.com/arpanghosh8453/fitbit-web-ui-app)** - github
	- graphics on https://dashboard.exercise.quest/

- integrate Batch Processing with Spark
	- [[DataTalks DE Zoomcamp 2025 Syllabus#*Module* 5 Batch Processing - *Spark*]]
	-  [DataTalksClub](https://github.com/DataTalksClub)/ [data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)/ [05-batch](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/05-batch "05-batch")
	-  [ManuelGuerra1987](https://github.com/ManuelGuerra1987) /  [data-engineering-zoomcamp-notes](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes)  / [5_Batch-Processing-Spark](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/tree/main/5_Batch-Processing-Spark "5_Batch-Processing-Spark")



## Rough Outline
PRE: 
- [x] setup for repo of data proj template for it ✅ 2025-03-04
- [x] add design doc ✅ 2025-03-04


- [ ] prototype py script: connect and download from fitbit/google health data API  
heart

- [ ] get minimalist Airflow working
1. API req my google data
2. Clean the data
	- SQL
	- pandas
3. Copy

- [ ] get minimalist Airflow working on EC2

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

## Device Connect
https://cloud.google.com/device-connect
[github](https://github.com/GoogleCloudPlatform/deviceconnect)

```python
FITBIT_OAUTH_CLIENT_ID = ''                          # fitbit client id (from dev.fitbit.com)
FITBIT_OAUTH_CLIENT_SECRET = ''                  # fitbit secret (from dev.fitbit.com)
```


# Project Step Log
- Clone [ny-taxi-pipeline](https://github.com/MichaelSalata/ny-taxi-pipeline)
- `gh auth login`
- `git remote set-url origin https://github.com/MichaelSalata/compare-fitbit-periods.git`
- dev.fitbit.com > Manage > Register An App > Log in
	- `Continue with Google`
- ![example app](https://miro.medium.com/v2/resize:fit:720/format:webp/1*UJHMOYsFZvrBmpNjFfpBJA.jpeg)
- insert the sensitive fitbit API tokens into the `.env` file
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
