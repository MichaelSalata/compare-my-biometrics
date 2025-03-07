import requests
from datetime import datetime, timedelta

import json

with open('fitbit_tokens.json', 'r') as file:
    tokens = json.load(file)

headers = {
    # TODO: properly format header tokens
    'Authorization': f'Bearer {tokens["access_token"]}'
}
"""
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}"""

API_website = "https://api.fitbit.com"

profile_endpoints = {
    # "activity": "",
    # "social": "",
    # "location": "",
    # "settings": ""
    "profile": "/1/user/{user_id}/profile.json"
}

# src: https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date/
# example: /1/user/[user-id]/activities/heart/date/[date]/[period].json
biometric_endpoints_day = {
    # "sleep": "/sleep/date/{date}.json",
    # "activity": "/activities/date/{date}.json",
    # "heartrate": "/activities/heart/date/{date}/1d.json",
    "weight": "/1/user/{user_id}/body/log/weight/date/{date}.json"
}

# src: https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date-range/
# example daterange_endpoint: /1/user/[user-id]/activities/heart/date/[start-date]/[end-date].json
biometric_endpoints_daterange = {
    "heartrate": "/1/user/{user_id}/activities/heart/date/{start}/{end}.json",
    # "nutrition": "",
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


def fetch_date_range(endpoint, start, end):
    url = API_website + endpoint.format(user_id=tokens["user_id"], start=start, end=end)
    response = requests.get(url, headers=headers)
    print("attempting", url, '\n')
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("request requires authentication")
        return None
    else:
        print(f"Failed to fetch data for {start} to {end}: response.status_code:{response.status_code}")
        return None
    

end_date = datetime.now()
start_date = end_date - timedelta(days=30)

print(tokens["scope"], biometric_endpoints_daterange.keys())
print(tokens["scope"] & biometric_endpoints_daterange.keys())

for key in tokens["scope"] & biometric_endpoints_daterange.keys():
    data = fetch_date_range(biometric_endpoints_daterange[key], start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if data:
        with open(f'{key}.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)
            print(f'Data for {key} has been saved to {key}.json')


"""
# Fetch data for each day in the past month
data = {key: [] for key in biometric_endpoints_day.keys()}
current_date = start_date
date_str = current_date.strftime("%Y-%m-%d")
for key, endpoint in biometric_endpoints_day.items():
    result = fetch_date(endpoint, date_str)
    if result:
        data[key].append(result)
current_date += timedelta(days=1)


# Print the fetched data
for key, values in data.items():
    print(f"Data for {key}:")
    for value in values:
        print(value)
"""