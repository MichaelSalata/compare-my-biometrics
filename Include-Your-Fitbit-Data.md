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
