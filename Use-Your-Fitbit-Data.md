By default, the project uses [my example fitbit data](https://github.com/MichaelSalata/compare-my-biometrics/tree/main/airflow-gcp/example_data)  spanning **11-21-2024**  to  **3-16-2025**

Doing this allows the project to download, store and analyze YOUR fitbit data in your BigQuery Dataset
# 1. Get your CLIENT_ID and CLIENT_SECRET
- [dev.fitbit.com](https://dev.fitbit.com/) > Manage > [Register An App](https://dev.fitbit.com/apps/new/) > [Log in](https://dev.fitbit.com/login)
	- `Continue with Google` if you use your google account
	- **IMPORTANT**: mark the project `Personal` and use Callback URL `http://127.0.0.1:8080/`
![fitbit_app_registration image](https://github.com/MichaelSalata/compare-my-biometrics/blob/main/imgs/register_fitbit_app.jpg)

# 2. Get your ACCESS_TOKEN
```bash
cd ./compare-my-biometrics/airflow-gcp/setup_scripts/
```
- RECOMMENDED: setup a python virtual environment here/now. e.g. `python3 -m venv venv`
- replace `CLIENT_ID` and `CLIENT_SECRET` with yours
```bash
pip install -r gather_keys_oauth2_requirements.txt
python3 /gather_keys_oauth2.py CLIENT_ID CLIENT_SECRET
```
- this saves a your Fitbit Http tokens to a variable in your `airflow-gcp/.env` file for Airflow
- If you've ran this before, it will reuse the previously saved values

## ACCESS_TOKENs expire
run it or delete the `AIRFLOW_CONN_FITBIT_CONN` from your `.env` and let it renew it via refresh tokens
