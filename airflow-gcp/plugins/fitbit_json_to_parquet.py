import json
import pandas as pd
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def profile_flatten_to_df(profile_data):
    profile = profile_data["user"]
    del profile["features"]
    del profile["topBadges"]
    profile_df = pd.DataFrame([profile])
    
    try:
        profile_df["user_id"] = profile_data["user_id"]
        profile_df["age"] = profile_df["age"].astype(int)
        profile_df["dateOfBirth"] = pd.to_datetime(profile_df["dateOfBirth"])
        profile_df["memberSince"] = pd.to_datetime(profile_df["memberSince"])
        profile_df["weight"] = profile_df["weight"].astype(float)
        profile_df["height"] = profile_df["height"].astype(float)
        profile_df["strideLengthWalking"] = profile_df["strideLengthWalking"].astype(float)
        profile_df["strideLengthRunning"] = profile_df["strideLengthRunning"].astype(float)
    except Exception as e:
        logger.error(f'Error: {e} reading profile.json')
        return pd.DataFrame()

    return profile_df

def sleep_flatten_to_df(sleep_data):
    if sleep_data and len(sleep_data["sleep"]) == 0:
        logger.warning('sleep_data is empty')
        return pd.DataFrame()

    rows = []
    for sleep in sleep_data["sleep"]:
        if not sleep["isMainSleep"]:
            continue

        try:
            row = {
                "user_id": sleep_data["user_id"],
                "dateOfSleep": pd.to_datetime(sleep["dateOfSleep"]),  # example_input: "2025-01-30"
                "startTime": pd.to_datetime(sleep["startTime"]),  # example_input: "2025-01-30T01:05:00.000"
                "endTime": pd.to_datetime(sleep["endTime"]),  # example_input: "2025-01-30T07:33:00.000"
                "duration": int(sleep["duration"]),
                "efficiency": float(sleep["efficiency"])/100,
                "infoCode": int(sleep["infoCode"]),
                "isMainSleep": bool(sleep["isMainSleep"]),
                "logId": int(sleep["logId"]),
                "logType": sleep["logType"],
                "minutesAfterWakeup": int(sleep["minutesAfterWakeup"]),
                "minutesAsleep": int(sleep["minutesAsleep"]),
                "minutesAwake": int(sleep["minutesAwake"]),
                "minutesToFallAsleep": int(sleep["minutesToFallAsleep"]),
                "timeInBed": int(sleep["timeInBed"]),
                "type": sleep["type"],

            
                "deep_count": int(sleep["levels"]["summary"]["deep"]["count"]),
                "deep_minutes": int(sleep["levels"]["summary"]["deep"]["minutes"]),
                "deep_thirtyDayAvgMinutes": int(sleep["levels"]["summary"]["deep"]["thirtyDayAvgMinutes"]),

                "light_count": int(sleep["levels"]["summary"]["light"]["count"]),
                "light_minutes": int(sleep["levels"]["summary"]["light"]["minutes"]),
                "light_thirtyDayAvgMinutes": int(sleep["levels"]["summary"]["light"]["thirtyDayAvgMinutes"]),

                "rem_count": int(sleep["levels"]["summary"]["rem"]["count"]),
                "rem_minutes": int(sleep["levels"]["summary"]["rem"]["minutes"]),
                "rem_thirtyDayAvgMinutes": int(sleep["levels"]["summary"]["rem"]["thirtyDayAvgMinutes"]),

                "wake_count": int(sleep["levels"]["summary"]["wake"]["count"]),
                "wake_minutes": int(sleep["levels"]["summary"]["wake"]["minutes"]),
                "wake_thirtyDayAvgMinutes": int(sleep["levels"]["summary"]["wake"]["thirtyDayAvgMinutes"])
            }
        except Exception as e:
            logger.error(f'Error: {e} reading json file sleep on date: {sleep.get("dateOfSleep")}')
            continue

        rows.append(row)
    
    return pd.DataFrame(rows)


def heartrate_flatten_to_df(heartrate_data):
    rows = []
    for heartrate in heartrate_data["activities-heart"]:
        try:
            row = {
                "user_id": heartrate_data["user_id"],
                "dateTime": pd.to_datetime(heartrate["dateTime"]),

                "Zone1_caloriesOut": float(heartrate["value"]["heartRateZones"][0].get("caloriesOut")),
                "Zone1_max_heartrate": int(heartrate["value"]["heartRateZones"][0]["max"]),
                "Zone1_min_heartrate": int(heartrate["value"]["heartRateZones"][0]["min"]),
                "Zone1_minutes": int(heartrate["value"]["heartRateZones"][0].get("minutes")),

                "Zone2_caloriesOut": float(heartrate["value"]["heartRateZones"][1].get("caloriesOut")),
                "Zone2_max_heartrate": int(heartrate["value"]["heartRateZones"][1]["max"]),
                "Zone2_min_heartrate": int(heartrate["value"]["heartRateZones"][1]["min"]),
                "Zone2_minutes": int(heartrate["value"]["heartRateZones"][1].get("minutes")),

                "Zone3_caloriesOut": float(heartrate["value"]["heartRateZones"][2].get("caloriesOut")),
                "Zone3_max_heartrate": int(heartrate["value"]["heartRateZones"][2]["max"]),
                "Zone3_min_heartrate": int(heartrate["value"]["heartRateZones"][2]["min"]),
                "Zone3_minutes": int(heartrate["value"]["heartRateZones"][2].get("minutes")),

                "Zone4_caloriesOut": float(heartrate["value"]["heartRateZones"][3].get("caloriesOut")),
                "Zone4_max_heartrate": int(heartrate["value"]["heartRateZones"][3]["max"]),
                "Zone4_min_heartrate": int(heartrate["value"]["heartRateZones"][3]["min"]),
                "Zone4_minutes": int(heartrate["value"]["heartRateZones"][3].get("minutes")),

                "restingHeartRate": int(heartrate["value"].get("restingHeartRate"))
            }
        except Exception as e:
            logger.error(f'Error: {e} reading sleep json on date: {heartrate.get("dateTime")}')
            continue

        rows.append(row)

    return pd.DataFrame(rows)


def profile_sleep_heartrate_jsons_to_parquet(base_path="/opt/airflow"):

    flatten_func_map = {
        "heartrate":heartrate_flatten_to_df,
        "profile":profile_flatten_to_df,
        "sleep":sleep_flatten_to_df
    }

    for endpoint, flatten_func in flatten_func_map.items():
        logger.debug(f"Attempting to parse {endpoint} files")
        json_files = glob.glob(f"{base_path}/{endpoint}*.json")
        if len(json_files) == 0:
            logger.warning(f"No {endpoint} files Found -> parsing example data")
            json_files = glob.glob(f"{base_path}/example_data/{endpoint}*.json")

        for json_file in json_files:
            try:
                with open(json_file, 'r') as file:
                    biometric_df = flatten_func(json.load(file))
                    if len(biometric_df) >= 1:
                        parquet_filename = json_file.replace(".json", ".parquet")
                        biometric_df.to_parquet(parquet_filename)
                        logger.info(f'wrote {len(biometric_df)} entries to {parquet_filename}')

            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.error(f"Error loading {json_file} file: {e}")
                raise e
            except Exception as e:
                logger.error(f"Unexpected error processing {json_file}: {e}")
                raise e


def flatten_fitbit_json_file(json_file: str):
    try:
        with open(json_file, 'r') as file:
            fitbit_data = json.load(file)
            flatten_func_map = {
                "activities-heart":(heartrate_flatten_to_df, "heartrate"),
                "user":(profile_flatten_to_df, "profile"),
                "sleep":(sleep_flatten_to_df, "sleep")
            }
            
            for key in fitbit_data.keys():
                if key != "user_id":
                    func_key = key
                    break

            flatten_func, fitbit_data_type = flatten_func_map[func_key]
            biometric_df = flatten_func(fitbit_data)

        if len(biometric_df) >= 1:
            parquet_filename = json_file.replace(".json", ".parquet")
            biometric_df.to_parquet(parquet_filename)
            logger.info(f'wrote {len(biometric_df)} entries to {parquet_filename}')

            return parquet_filename, fitbit_data_type
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading {json_file} file: {e}")
        raise e


def flatten_fitbit_json(endpoint: str, base_path="/opt/airflow"):

    flatten_func_map = {
        "heartrate":heartrate_flatten_to_df,
        "profile":profile_flatten_to_df,
        "sleep":sleep_flatten_to_df
    }

    logger.debug(f"Attempting to parse {endpoint} files")
    json_files = glob.glob(f"{base_path}/{endpoint}*.json")
    if len(json_files) == 0:
        logger.warning(f"No {endpoint} files Found -> parsing example data")
        json_files = glob.glob(f"{base_path}/example_data/{endpoint}*.json")

    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                biometric_df = flatten_func_map[endpoint](json.load(file))
                if len(biometric_df) >= 1:
                    parquet_filename = json_file.replace(".json", ".parquet")
                    biometric_df.to_parquet(parquet_filename)
                    logger.info(f'wrote {len(biometric_df)} entries to {parquet_filename}')

        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading {json_file} file: {e}")
            raise e
        except Exception as e:
            logging.error(f"Unexpected error processing {json_file}: {e}")
            raise e