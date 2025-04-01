
 [getting fitbit CLIENT_ID and CLIENT_SECRET - gpt](https://chatgpt.com/c/67945566-6294-8008-963e-90d98c8ffd08)

Google Fit has some good charts of emulate
Someone already did a Fitibit Visualization for their Data Engineering Zoomcamp Project

## Fitbit API

[API documentation](https://python-fitbit.readthedocs.io/en/latest/#fitbit-api)

[python-fitbit github](https://github.com/orcasgit/python-fitbit/tree/master) -  ==[gather_keys_oauth2.py](https://github.com/orcasgit/python-fitbit/blob/master/gather_keys_oauth2.py)==

https://python-fitbit.readthedocs.io/en/latest/#fitbit-api

### [Fitbit OAuth 2.0 Tutorial](https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/)

# Similar Projects
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


# Other Projects - Airflow Spark BigQuery
[Github Search](https://github.com/search?q=Airflow+Spark+Dataproc&type=repositories&s=stars&o=desc)


## Batch Processing on DataProc

## [steam-data-engineering](https://github.com/VicenteYago/steam-data-engineering)
by [VicenteYago](https://github.com/VicenteYago)

## [dezoomcamp-project](https://github.com/toludaree/dezoomcamp-project)
by [toludaree](https://github.com/toludaree)
- fair instructions on setting up the google cloud infrastructure
- processes json file using a schema in [spark_job.py](https://github.com/toludaree/dezoomcamp-project/blob/main/dataproc/spark_job.py)
- ran in [gharchive_dag.py](https://github.com/toludaree/dezoomcamp-project/blob/e8a6d7f095640ba6039551eb77793e2218b94d77/airflow/dags/gharchive_dag.py#L90)
- batch processing with [Google DataProc](https://cloud.google.com/dataproc)

## [JorgeAbrego](https://github.com/JorgeAbrego)
great infrastructure setup
## [weather_stream_project](https://github.com/JorgeAbrego/weather_stream_project)
by [JorgeAbrego](https://github.com/JorgeAbrego)
- docker encapsulates spark but I don't see him using it........................
## [capital_bikeshare_project](https://github.com/JorgeAbrego/capital_bikeshare_project)
by [JorgeAbrego](https://github.com/JorgeAbrego)
- good infraestructure management with terraform
- wtf no spark


## Spark Streaming SQL queries

## [streamify](https://github.com/ankurchavda/streamify)
by [ankurchavda](https://github.com/ankurchavda)
- does streaming
- calls an SQL query on a json file??
- `from pyspark.sql.functions import from_json`

## [ShowPulse_Ticketmaster](https://github.com/nburkett/ShowPulse_Ticketmaster)
by [nburkett](https://github.com/nburkett)
- [**Kafka**](https://kafka.apache.org/), [**Spark Streaming**](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
- `from pyspark.sql.functions import from_json`

## [GCP_Streaming-Crypto-ETL](https://github.com/ghiles10/GCP_Streaming-Crypto-ETL)
by [ghiles10](https://github.com/ghiles10)
- Data Processing	PySpark, Spark Streaming
- The data is fetched from the Kucoin API, streamed through Kafka, processed using Spark Streaming on a DataProc cluster,
## Other

## [data_engineer_api_pipeline](https://github.com/VanAltrades/data_engineer_api_pipeline)
by [VanAltrades](https://github.com/VanAltrades)/
- **==cloud managed Airflow==**
- no spark on the repo?
- is it somehow hidden in the cloud managed Airflow ???
ETL API data workflow using Google Cloud Platform's Cloud Composer and Databricks services. Introduction to cloud managed Airflow and Spark orchestration.

## [Bandcamp-DE-project](https://github.com/ta-brook/Bandcamp-DE-project)
by [ta-brook](https://github.com/ta-brook)
- TECHNICALLY uses spark locally in [spark.py](https://github.com/ta-brook/Bandcamp-DE-project/blob/main/airflow/dags/script/spark.py)

## [airflow-spark-gcp-docker](https://github.com/archie-cm/airflow-spark-gcp-docker)
by [archie-cm](https://github.com/archie-cm)
- appears to use spark locally with postgres db
## [BigQuery-ELT](https://github.com/vishu-tyagi/BigQuery-ELT)
by [vishu-tyagi](https://github.com/vishu-tyagi)
- uses taxi data, no spark uses


## [Debussy](https://github.com/debussy-labs/debussy_concert/tree/master)
opinionated Data Architecture and Engineering framework