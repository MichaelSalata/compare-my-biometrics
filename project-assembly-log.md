
# Motivations - Why
- my wellness report was broken
- Gather metrics and visualize large life changes on life changes
	- ADHD meds
	- moving
	- exercising
- learn about about the tech involved the DataTalks bootcamp
- fits in my tight deadline
	- I understand how meetings and gathering data for a novel project can balloon out the time commitment

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

# Features - WHY
- compare multiple health metrics across a date range

- Desired Visualizations or Metrics
	- Heart Rate Exercise Zone Rates
		- stacked barchart or line chart over window
		- pie chart?
	- Sleep zones
		- stacked barchart or line chart over window
		- pie chart?
- create a list of notable dates
	- notable dates will be put on the graphs as vertical lines

# TODOs
- [ ] research good graphics
	- look at Google Fit Metrics
	- how I used my jupyter notebooks
	- graphics on **[fitbit-web-ui-app](https://github.com/arpanghosh8453/fitbit-web-ui-app)** - github
	- graphics on https://dashboard.exercise.quest/
- [ ] find code to download data
	- hard code my google auth


## Project Steps
- PHASE 1 - proof of concept
	- [ ] get ANY data downloaded
		- ==hardcore necessary fitbit data to query fitbit api==
			- ~~recreate AWS threaded download/upload script but for fitbit API:~~
				- `/home/michael/Documents/projects/datatalks-data-engineering-hw-notes/04-analytics-engineering/load_taxi_data_4analytics.py` 
				- `ec2_load_taxi_data_4analytics.py`
	- [ ] research API output most similar to ny_taxi data
	- [ ] get data uploaded to GCP and migrated to Bigquery
- PHASE 2 - automate
	- [ ] automate API access token retrieval for querying fitbit api
	- [ ] create a scheduled airflow job
- PHASE 3 - hosting
	- [ ] move job scheduling to a cloud service

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

# MY project development overview
- fast prototype
	- get ANY data from API
		- working on place without internet, ensure I had the data
		- reading API and following instructions
			- create a dev.fitbit.com project
			- using published code to get ACCESS token and USER ID
				- getting a CLIENT_ID, CLIENT_SECRET
				- learn about using OAuth2 to log in
				- catching the response in a server
				- parsing ACCESS token and USER ID
		- 
- 