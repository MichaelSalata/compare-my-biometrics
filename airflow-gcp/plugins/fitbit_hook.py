from airflow.hooks.base import BaseHook
import requests
from datetime import datetime, timedelta
import json
import calendar
import logging
import os


class FitbitHook(BaseHook):
    """
    Hook to interact with the Fitbit API.
    Handles authentication and provides methods to fetch data.
    """

    def __init__(self, conn_id="FITBIT_HTTP"):
        super().__init__()
        self.conn_id = conn_id
        self.connection = self.get_connection(conn_id)
        self._client_id = self.connection.login
        self._client_secret = self.connection.password
        self.user_id = self.connection.extra_dejson.get("user_id")
        self._access_token = self.connection.extra_dejson.get("access_token")
        self._refresh_token = self.connection.extra_dejson.get("refresh_token")
        self._scope = self.connection.extra_dejson.get("scope")

        self.max_fetchrange = {
            "sleep": timedelta(days=100)
        }
        
        self.day_specific_endpoints = {
            "azm": "/1/user/{user_id}/activities/active-zone-minutes/date/{date}/{date}/1min.json",    # intraday
            "hr_intraday": "/1/user/{user_id}/activities/heart/date/{date}/{date}/1min.json",    # intraday
            "calories": "/1/user/{user_id}/activities/calories/date/{date}/{date}/1min.json",    # intraday
            "distance": "/1/user/{user_id}/activities/distance/date/{date}/{date}/1min.json",    # intraday
            "elevation": "/1/user/{user_id}/activities/elevation/date/{date}/{date}/1min.json",   # intraday
            "floors": "/1/user/{user_id}/activities/floors/date/{date}/{date}/1min.json",         # intraday
            "steps": "/1/user/{user_id}/activities/steps/date/{date}/{date}/1min.json",    # intraday
            "sleep": "/sleep/date/{date}.json",
            "activity": "/activities/date/{date}.json",
            "heartrate": "/activities/heart/date/{date}/1d.json",
            "weight": "/1/user/{user_id}/body/log/weight/date/{date}.json",
            "fat": "/1/user/{user_id}/body/log/fat/date/{date}.json"
        }

        self.dayrange_endpoints = {
            "heartrate": "/1/user/{user_id}/activities/heart/date/{start}/{end}.json",
            "hrv": "/1/user/{user_id}/hrv/date/{start}/{end}/all.json",
            "spO2": "/1/user/{user_id}/spo2/date/{start}/{end}/all.json",
            "sleep": "/1.2/user/{user_id}/sleep/date/{start}/{end}.json"
        }

        self.static_endpoints = {
            "profile": "/1/user/{user_id}/profile.json"
        }

    def fetch_static(self, endpoint_id: str):
        headers = {
            'Authorization': f'Bearer {self._access_token}'
        }

        endpoint_suffix = self.static_endpoints[endpoint_id]
        url = f"https://api.fitbit.com{endpoint_suffix}"
        logging.info(f"Attempting to download: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logging.info(f"Successfully downloaded: {url}")
            return response.json()
        elif response.status_code == 401:
            raise Exception("Authentication failed")
        else:
            raise Exception(f"HTTP {response.status_code} : Download failed for {url}: ")

    def fetch_from_endpoint(self, endpoint_suffix: str):
        headers = {
            'Authorization': f'Bearer {self._access_token}'
        }
        url = f"https://api.fitbit.com{endpoint_suffix}"
        logging.info(f"Attempting download from {url}")
        response = requests.get(url, headers=headers)
        logging.info(f"HTTP: {response.status_code}, Response: {response}")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            logging.error("Authentication failed. Refresh the token.")
            raise Exception("Authentication failed.")
        else:
            logging.error(f"HTTP {response.status_code}: Failed fetch_from_endpoint from {url}) response.text-> {response.text}")
            raise Exception(f"HTTP {response.status_code}: Failed fetch_from_endpoint from {url}) response.text-> {response.text}")


    def fetch_daterange(self, endpoint_id: str, start: datetime, end: datetime):
        if endpoint_id in self._scope:
            dayrange_suffix_fmt = self.dayrange_endpoints.get(endpoint_id, None)
            if dayrange_suffix_fmt:
                if endpoint_id in self.max_fetchrange:
                    fetch_range_max = self.max_fetchrange.get(endpoint_id)
                    print(f"fetch_range_max: {fetch_range_max}")
                    end = start + min(fetch_range_max, end-start)

                endpoint_suffix = dayrange_suffix_fmt.format(user_id=self.user_id, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
                return self.fetch_from_endpoint(endpoint_suffix)
            
            logging.error(f"Unrecognized dayrange endpoint {endpoint_suffix}")
            return None
        else:
            logging.warning(f"Don't have permissions to download {endpoint_id}")
            return None

        # TODO determine if Intraday endpoint access is affected by self._scope (try downloading intraday data out of _scope)
        # TODO attempt to download from Intraday endpoints, stop download attempts if get a permissions error as intraday is either all or nothing from Personal dev account access


    def refresh_tokens(self):
        # WARNING: FUNCTION IS CURRENTLY UNTESTED
        url = "https://api.fitbit.com/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            tokens = response.json()

            self.user_id = tokens["user_id"]
            self._access_token = tokens["access_token"]
            self._refresh_token = tokens["refresh_token"]
            self._scope = tokens["scope"]

            self.update_connection(tokens)
            return
        else:
            logging.error(f"Failed to refresh self._tokens: {response.text}")
            raise Exception(f"Failed to refresh self._tokens: {response.text}")

    def update_connection(self, tokens):
        # WARNING: FUNCTION IS CURRENTLY UNTESTED
        conn = self.get_connection(self.conn_id)

        tokens.pop("client_id", None)  # Safely remove "client_id" if it exists
        tokens.pop("client_secret", None)  # Safely remove "client_secret" if it exists
        conn.extra=json.dumps(tokens)

        session = self.get_session()
        session.add(conn)
        session.commit()


    def save_data(self, data, endpoint_name: str, start_date: datetime=None, end_date: datetime=None, filename=None):
        if not filename:
            if (not start_date) and (not end_date):
                filename = f'{endpoint_name}.json'
            else:
                # TODO: refactor file naming to append month at file end to better adhere with download schedule and data governance
                filename = f'{endpoint_name}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.json'
        
        data["user_id"] = self.user_id
        with open(filename, 'w') as data_file:
            json.dump(data, data_file, indent=4)
            logging.info(f"{endpoint_name} data saved to {filename}")
            return filename

    def download_past_6_months(self, endpoint_id: str):
        if endpoint_id in self.static_endpoints:
            response = self.fetch_from_endpoint(self.static_endpoints[endpoint_id].format(user_id=self.user_id))
            if not response:
                logging.error(f"Downloading {endpoint_id} failed")
                logging.error(response)
            else:
                return self.save_data(response, endpoint_id)
    
        end_date = datetime.now()
        start_date = end_date.replace(day=1)

        past_month_count = 6
        while past_month_count >= 1:
            response = self.fetch_daterange(endpoint_id, start=start_date, end=end_date)
            if response:
                self.save_data(response, endpoint_id, start_date=start_date, end_date=end_date)
            else:
                logging.warning(f"No data retrieved for {endpoint_id} from {start_date} to {end_date}")
            end_date = start_date - timedelta(days=1)
            start_date = end_date - timedelta(days=calendar.monthrange(end_date.year, end_date.month)[1]-1)
            past_month_count -= 1