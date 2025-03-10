import requests
from datetime import datetime, timedelta

import json

with open('fitbit_tokens.json', 'r') as file:
    tokens = json.load(file)

headers = {
    # TODO: properly format header tokens
    'Authorization': f'Bearer {tokens["access_token"]}'
}

API_website = "https://api.fitbit.com"

static_endpoints = {
    # "activity": "",
    # "social": "",
    # "location": "",
    # "settings": ""
    "profile": "/1/user/{user_id}/profile.json"
}

# src: https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date/
# example: /1/user/[user-id]/activities/heart/date/[date]/[period].json
day_specific_endpoints = {
    # "sleep": "/sleep/date/{date}.json",
    # "activity": "/activities/date/{date}.json",
    # "heartrate": "/activities/heart/date/{date}/1d.json",
    "weight": "/1/user/{user_id}/body/log/weight/date/{date}.json",
    "fat": "/1/user/{user_id}/body/log/fat/date/{date}.json"
}

# src: https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date-range/
# example daterange_endpoint: /1/user/[user-id]/activities/heart/date/[start-date]/[end-date].json
daterange_endpoints = {
    "heartrate": "/1/user/{user_id}/activities/heart/date/{start}/{end}.json",
    # "nutrition": "",

    # "activity": "/1/user/[user-id]/activities/[resource-path]/date/{start}/{end}.json"
    # resource options: https://dev.fitbit.com/build/reference/web-api/activity-timeseries/get-activity-timeseries-by-date-range/#Resource-Options

    "sleep": "/1.2/user/{user_id}/sleep/date/{start}/{end}.json"
}



def fetch_date(endpoint, date):
    url = API_website + endpoint.format(date=date)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("request requires authentication")
        return None
    else:
        print(f"Failed to fetch data for {date}: {response.status_code}")
        return None

def fetch_static(endpoint_suffix):
    url = API_website + endpoint_suffix.format(user_id=tokens["user_id"])
    response = requests.get(url, headers=headers)
    print("attempting download", url, '\n')
    if response.status_code == 200:
        print(f"Downloaded: {url}")
        return response.json()
    elif response.status_code == 401:
        print("request requires authentication")
        return None
    else:
        print(f"{url} download FAILED: response.status_code:{response.status_code}")
        return None


def fetch_date_range(endpoint_suffix, start, end):
    url = API_website + endpoint_suffix.format(user_id=tokens["user_id"], start=start, end=end)
    response = requests.get(url, headers=headers)
    print("attempting", url, '\n')
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("request requires authentication")
        return None
    else:
        print(f"{url} download FAILED for {start} to {end}: response.status_code:{response.status_code}")
        return None
    

end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# print(tokens["scope"], biometric_endpoints_daterange.keys())
# print(tokens["scope"] & biometric_endpoints_daterange.keys())

# save data from static endpoints
print(tokens["scope"])
print(list(static_endpoints.keys()))
for endpoint_name in (tokens["scope"] & static_endpoints.keys()):
    data = fetch_static(static_endpoints[endpoint_name])
    if data:
        with open(f'{endpoint_name}.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)
            print(f'Data for {endpoint_name} has been saved to {endpoint_name}.json')

# get data from date range endpoints
for endpoint_name in tokens["scope"] & daterange_endpoints.keys():
    data = fetch_date_range(daterange_endpoints[endpoint_name], start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
    if data:
        with open(f'{endpoint_name}.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)
            print(f'Data for {endpoint_name} has been saved to {endpoint_name}.json')
