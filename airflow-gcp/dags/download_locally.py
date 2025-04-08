import requests
from datetime import datetime, timedelta
import json
import calendar
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# example documentation: https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date/
# day_specific_endpoints = {
#     "azm": "/1/user/{user_id}/activities/active-zone-minutes/date/{date}/{date}/1min.json",    # intraday
#     "hr_intraday": "/1/user/{user_id}/activities/heart/date/{date}/{date}/1min.json",    # intraday
#     "calories": "/1/user/{user_id}/activities/calories/date/{date}/{date}/1min.json",    # intraday
#     "distance": "/1/user/{user_id}/activities/distance/date/{date}/{date}/1min.json",    # intraday
#     "elevation": "/1/user/{user_id}/activities/elevation/date/{date}/{date}/1min.json",   # intraday
#     "floors": "/1/user/{user_id}/activities/floors/date/{date}/{date}/1min.json",         # intraday
#     "steps": "/1/user/{user_id}/activities/steps/date/{date}/{date}/1min.json",    # intraday
#     "sleep": "/sleep/date/{date}.json",
#     "activity": "/activities/date/{date}.json",
#     "heartrate": "/activities/heart/date/{date}/1d.json",
#     "weight": "/1/user/{user_id}/body/log/weight/date/{date}.json",
#     "fat": "/1/user/{user_id}/body/log/fat/date/{date}.json"
# }

def fetch_static(endpoint_suffix, tokens):
    API_base_url = "https://api.fitbit.com"
    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}'
    }

    url = API_base_url + endpoint_suffix.format(user_id=tokens["user_id"])
    logger.info(f"Attempting to download: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logger.info(f"Successfully downloaded: {url}")
        return response.json()
    elif response.status_code == 401:
        logger.error("Authentication failed")
        return None
    else:
        logger.error(f"HTTP {response.status_code} : Download failed for {url}: ")
        return None


def fetch_date_range(endpoint_suffix, start, end, tokens):
    API_base_url = "https://api.fitbit.com"
    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}'
    }

    url = API_base_url + endpoint_suffix.format(user_id=tokens["user_id"], start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
    logger.info(f"Attempting to download: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        logger.error("Authentication failed")
        return None
    else:
        logger.error(f"HTTP {response.status_code} : Download failed from {url} (from {start} to {end}): ")
        return None


def download_the_past_month():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    download_date_range(start_date, end_date)


def save_data(data, endpoint_name, user_id, start_date=None, end_date=None, filename=None):
    if not filename:
        if (not start_date) and (not end_date):
            filename = f'{endpoint_name}.json'
        else:
            filename = f'{endpoint_name}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.json'
    
    data["user_id"] = user_id
    with open(filename, 'w') as data_file:
        json.dump(data, data_file, indent=4)
        logger.info(f"Data from {endpoint_name} has been saved to {filename}")


def download_static_data(endpoint_name, tokens):
    static_endpoints = {
        "profile": "/1/user/{user_id}/profile.json"
    }

    if endpoint_name:
        if endpoint_name not in tokens["scope"]:
            logger.warning(f"Scope doesn't permit this data source : {endpoint_name}")
            return
        
        if endpoint_name in static_endpoints.keys():
            data = fetch_static(static_endpoints[endpoint_name], tokens=tokens)
            if data:
                save_data(data, endpoint_name, user_id=tokens["user_id"])
        else:
            logger.warning(f"URL is not a known static endpoint for the Fitbit API: '{endpoint_name}'")
        return
    
    # if no endpoint_name is specified, download from all endpoints that you have permissions(tokens) for
    # Save data from static endpoints
    for endpoint_name in (tokens["scope"] & static_endpoints.keys()):
        data = fetch_static(static_endpoints[endpoint_name], tokens=tokens)
        if data:
            save_data(data, endpoint_name, user_id=tokens["user_id"])


def download_date_range(start_date, end_date, tokens, filename=None, endpoint_name=None):
    daterange_endpoints = {
        "heartrate": "/1/user/{user_id}/activities/heart/date/{start}/{end}.json",
        "hrv": "/1/user/{user_id}/hrv/date/{start}/{end}/all.json",
        "spO2": "/1/user/{user_id}/spo2/date/{start}/{end}/all.json",
        "sleep": "/1.2/user/{user_id}/sleep/date/{start}/{end}.json"
    }

    # if an endpoint_name is specified, ONLY download from that endpoint
    if endpoint_name:
        if endpoint_name not in tokens["scope"]:
            logger.warning(f"Endpoint '{endpoint_name}' is not in the permissions scope")
            return
        
        if endpoint_name in daterange_endpoints.keys():
            data = fetch_date_range(daterange_endpoints[endpoint_name], start=start_date, end=end_date, tokens=tokens)
            if data:
                save_data(data, endpoint_name, user_id=tokens["user_id"], start_date=start_date, end_date=end_date, filename=filename)
        else:
            logger.warning(f"URL is not a known daterange endpoint for the Fitbit API: '{endpoint_name}'")
        return

    # if no endpoint_name is specified, download from all endpoints that you have permissions(tokens) for
    # Get data from date range endpoints
    for endpoint_name in tokens["scope"] & daterange_endpoints.keys():
        data = fetch_date_range(daterange_endpoints[endpoint_name], start=start_date, end=end_date, tokens=tokens)
        if data:
            save_data(data, endpoint_name, user_id=tokens["user_id"], start_date=start_date, end_date=end_date, filename=filename)


def download_past_6_months(tokens_path="."):
    try:
        with open(f"{tokens_path}/fitbit_tokens.json", 'r') as file:
            tokens = json.load(file)
    except FileNotFoundError:
        logger.error(f"Token file not found at {tokens_path}/fitbit_tokens.json")
        exit(1)
    
    if "example" in tokens["client_id"]:
        logger.info("Fitbit access tokens are not valid. Download skipped. Using example data.")
        return

    download_static_data("profile", tokens=tokens)

    end_date = datetime.now()
    start_date = end_date.replace(day=1)

    past_month_count = 6
    while past_month_count >= 1:
        download_date_range(start_date=start_date, end_date=end_date, tokens=tokens)
        end_date = start_date - timedelta(days=1)
        start_date = end_date - timedelta(days=calendar.monthrange(end_date.year, end_date.month)[1]-1)
        past_month_count -= 1
