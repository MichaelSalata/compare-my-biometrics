By default, the project uses [my example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data)  spanning **11-21-2024**  to  **3-16-2025**

Doing this allows the project to download, store and analyze YOUR fitbit data in your BigQuery Dataset
# 1. Get your CLIENT_ID and CLIENT_SECRET
- [dev.fitbit.com](https://dev.fitbit.com/) > Manage > [Register An App](https://dev.fitbit.com/apps/new/) > [Log in](https://dev.fitbit.com/login)
	- `Continue with Google` if you use your google account
	- **IMPORTANT**: mark the project `Personal` and use Callback URL `http://127.0.0.1:8080/`
![fitbit_app_registration image](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/register_fitbit_app.jpg)

# 2. Get your ACCESS_TOKEN
OPTION 1:
```bash
python3 /dags/gather_keys_oauth2.py CLIENT_ID CLIENT_SECRET
```
- this saves a `/dags/fitbit_tokens.json` file in the dag directory
- replace CLIENT_ID and CLIENT_SECRET with what was shown on your app
	- If you've ran this before, the `CLIENT_ID` and `CLIENT_SECRET` are unnecessary (they're saved in the `fitbit_tokens.json`)

## ACCESS_TOKENs expire
run it again
```bash
python3 /dags/gather_keys_oauth2.py
```
it reuses `CLIENT_ID` and `CLIENT_SECRET` which were stored in your first `dags/fitbit_tokens`
