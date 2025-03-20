import json
import pandas as pd
import glob



def profile_json_to_parquet(filename):
    try:
        with open(filename, 'r') as file:
            profile_data = json.load(file)
            profile = profile_data["user"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename} file: {e}")
        exit(1)
    
    del profile["features"]
    del profile["topBadges"]
    profile_df = pd.DataFrame([profile])
    
    try:
        profile_df["user_id"] = profile_data["user_id"]
        profile_df["age"] = profile_df["age"].astype(int)
        profile_df["dateOfBirth"] = pd.to_datetime(profile_df["dateOfBirth"]) # example_input: "1989-08-30"
        profile_df["memberSince"] = pd.to_datetime(profile_df["memberSince"]) # example_input: "2024-11-21"
        profile_df["weight"] = profile_df["weight"].astype(float)
        profile_df["height"] = profile_df["height"].astype(float)
        profile_df["strideLengthWalking"] = profile_df["strideLengthWalking"].astype(float)
        profile_df["strideLengthRunning"] = profile_df["strideLengthRunning"].astype(float)
    except Exception as e:
        print(f'Error: {e} reading json file {filename}:')
        # print(sleep)
        return

    parquet_filename = filename.replace(".json", ".parquet")
    profile_df.to_parquet(parquet_filename)
    # print(profile_df.info())
    print(f"Converted {filename} to {parquet_filename}")


def sleep_json_to_parquet(filename):
    try:
        with open(filename, 'r') as file:
            sleep_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename} file: {e}")
        exit(1)
    
    if len(sleep_data["sleep"]) == 0:
        print(f'{filename} is empty')
        return

    rows = []
    for sleep in sleep_data["sleep"]:
        # levels = sleep["levels"]["summary"]
        if not sleep["isMainSleep"]:
            continue

        # print(sleep["levels"]["summary"])

        # TODO: Modularize the appending of row data
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
            print(f'Error: {e} reading json file {filename} on date: {sleep.get("dateOfSleep")}:')
            # print(sleep)
            continue

        rows.append(row)

    if len(rows) >= 1:
        sleep_df = pd.DataFrame(rows)
        parquet_filename = filename.replace(".json", ".parquet")
        sleep_df.to_parquet(parquet_filename)
        print(f'wrote {len(rows)} entries to {parquet_filename}')
    # print(sleep_df.info())
    # print(sleep_df.head())

def heartrate_json_to_parquet(filename):
    try:
        with open(filename, 'r') as file:
            heartrate_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file} file: {e}")
        exit(1)


    zone_map = {
        "Out of Range":"Zone1",
        "Fat Burn":"Zone2",
        "Cardio":"Zone3",
        "Peak":"Zone4"
    }

    rows = []
    for heartrate in heartrate_data["activities-heart"]:
        # zname = zone_map[heartrate["value"]["heartRateZones"][0]["name"]]
        try:
            row = {
                "user_id": heartrate_data["user_id"],
                "dateTime": pd.to_datetime(heartrate["dateTime"]),  # example_input: "2025-02-01"

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
            print(f'Error: {e} reading json file {filename} on date: {heartrate.get("dateOfSleep")}:')
            # print(sleep)
            continue

        rows.append(row)

    if len(rows) >= 1:
        heartrate_df = pd.DataFrame(rows)
        parquet_filename = filename.replace(".json", ".parquet")
        heartrate_df.to_parquet(parquet_filename)
        print(f'wrote {len(rows)} entries to {parquet_filename}')
    # print(heartrate_df.head())

def profile_sleep_heartrate_jsons_to_parquet():
    for filename in glob.glob("sleep*.json"):
        sleep_json_to_parquet(filename)

    for filename in glob.glob("profile*.json"):
        profile_json_to_parquet(filename)

    for filename in glob.glob("heartrate*.json"):
        heartrate_json_to_parquet(filename)

