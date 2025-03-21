import requests
from datetime import datetime, timedelta
import json
import calendar


# example documentation: https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date/
# day_specific_endpoints = {
#     # "sleep": "/sleep/date/{date}.json",
#     # "activity": "/activities/date/{date}.json",
#     # "heartrate": "/activities/heart/date/{date}/1d.json",
#     "weight": "/1/user/{user_id}/body/log/weight/date/{date}.json",
#     "fat": "/1/user/{user_id}/body/log/fat/date/{date}.json"
# }

def fetch_static(endpoint_suffix, tokens):
    API_base_url = "https://api.fitbit.com"
    headers = {
        # TODO: properly format header tokens
        'Authorization': f'Bearer {tokens["access_token"]}'
    }

    url = API_base_url + endpoint_suffix.format(user_id=tokens["user_id"])
    response = requests.get(url, headers=headers)
    print("attempting download", url, '\n')
    if response.status_code == 200:
        print(f"Downloaded: {url}")
        return response.json()
    elif response.status_code == 401:
        print("authentication failed")
        return None
    else:
        print(f"{url} download FAILED: response.status_code:{response.status_code}")
        return None


def fetch_date_range(endpoint_suffix, start, end, tokens):
    API_base_url = "https://api.fitbit.com"
    headers = {
        # TODO: properly format header tokens
        'Authorization': f'Bearer {tokens["access_token"]}'
    }

    url = API_base_url + endpoint_suffix.format(user_id=tokens["user_id"], start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
    response = requests.get(url, headers=headers)
    print("attempting download", url, '\n')
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("authentication failed")
        return None
    else:
        print(f"{url} download FAILED for {start} to {end}: response.status_code:{response.status_code}")
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
        print(f'Data for {endpoint_name} has been saved to {filename}')

def download_static_data(endpoint_name, tokens):
    static_endpoints = {
        # "activity": "",
        # "social": "",
        # "location": "",
        # "settings": "",
        "profile": "/1/user/{user_id}/profile.json"
    }

    # if an endpoint_name is specified, ONLY download from that endpoint
    if endpoint_name:
        if endpoint_name not in tokens["scope"]:
            print("don't have permissions for that endpoint")
        
        if endpoint_name in static_endpoints.keys():
            data = fetch_static(static_endpoints[endpoint_name], tokens=tokens)
            if data:
                save_data(data, endpoint_name, user_id=tokens["user_id"])
        else:
            print("don't know a url for that endpoint")
            
        return
    
    # if no endpoint_name is specified, download from all endpoints that you have permissions(tokens) for
    # Save data from static endpoints
    for endpoint_name in (tokens["scope"] & static_endpoints.keys()):
        data = fetch_static(static_endpoints[endpoint_name], tokens=tokens)
        if data:
            save_data(data, endpoint_name, user_id=tokens["user_id"])
    

def download_date_range(start_date, end_date, tokens, filename=None, endpoint_name=None):
    # example documentation: https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date-range/
    daterange_endpoints = {
        "heartrate": "/1/user/{user_id}/activities/heart/date/{start}/{end}.json",
        # "nutrition": "",

        # "activity": "/1/user/[user-id]/activities/[resource-path]/date/{start}/{end}.json"
        # resource options: https://dev.fitbit.com/build/reference/web-api/activity-timeseries/get-activity-timeseries-by-date-range/#Resource-Options

        "sleep": "/1.2/user/{user_id}/sleep/date/{start}/{end}.json"
    }

    # if an endpoint_name is specified, ONLY download from that endpoint
    if endpoint_name:
        if endpoint_name not in tokens["scope"]:
            print("don't have permissions for that endpoint")
            
        if endpoint_name in daterange_endpoints.keys():
            data = fetch_date_range(daterange_endpoints[endpoint_name], start=start_date, end=end_date, tokens=tokens)
            if data:
                save_data(data, endpoint_name, user_id=tokens["user_id"], start_date=start_date, end_date=end_date, filename=filename)
        else:
            print("don't know a url for that endpoint")
        
        return

    # if no endpoint_name is specified, download from all endpoints that you have permissions(tokens) for
    # Get data from date range endpoints
    for endpoint_name in tokens["scope"] & daterange_endpoints.keys():
        data = fetch_date_range(daterange_endpoints[endpoint_name], start=start_date, end=end_date, tokens=tokens)
        if data:
            save_data(data, endpoint_name, user_id=tokens["user_id"], start_date=start_date, end_date=end_date, filename=filename)



def download_past_6_months(tokens_path="."):
    with open(f"{tokens_path}/fitbit_tokens.json", 'r') as file:
        print(f"token file found at {tokens_path}/fitbit_tokens.json")
        tokens = json.load(file)
    
    if "example" in tokens["client_id"]:
        print("fitbit access tokens aren't valid -> download skipped -> using example data")
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
