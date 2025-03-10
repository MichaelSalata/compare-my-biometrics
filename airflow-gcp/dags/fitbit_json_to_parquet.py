import json
import pandas as pd
import glob


# def sleep_json_to_parquet(filename):





dimension = "sleep"
filename = f"{dimension}.json"


def profile_json_to_parquet(filename):
    try:
        with open(filename, 'r') as file:
            profile_data = json.load(file)["user"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename} file: {e}")
        exit(1)
    
    del profile_data["features"]
    del profile_data["topBadges"]
    # print(profile_data)
    profile_df = pd.DataFrame([profile_data])

    profile_df["age"] = profile_df["age"].astype(int)
    profile_df["dateOfBirth"] = pd.to_datetime(profile_df["dateOfBirth"])
    profile_df["memberSince"] = pd.to_datetime(profile_df["memberSince"])
    profile_df["weight"] = profile_df["weight"].astype(float)
    profile_df["height"] = profile_df["height"].astype(float)
    profile_df["strideLengthWalking"] = profile_df["strideLengthWalking"].astype(float)
    profile_df["strideLengthRunning"] = profile_df["strideLengthRunning"].astype(float)

    parquet_filename = filename.replace(".json", ".parquet")
    profile_df.to_parquet(parquet_filename)
    # print(profile_df.info())
    print(profile_df.head())


def sleep_json_to_parquet(filename):
    try:
        with open(filename, 'r') as file:
            sleep_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename} file: {e}")
        exit(1)
    

    rows = []
    for sleep in sleep_data["sleep"]:
        # levels = sleep["levels"]["summary"]
        if not sleep["isMainSleep"]:
            continue

        # print(sleep["levels"]["summary"])

        # TODO: Modularize the appending of row data

        row = {
            "dateOfSleep": pd.to_datetime(sleep["dateOfSleep"]),
            "duration": int(sleep["duration"]),
            "efficiency": float(sleep["efficiency"])/100,
            "endTime": pd.to_datetime(sleep["endTime"]),
            "infoCode": int(sleep["infoCode"]),
            "isMainSleep": bool(sleep["isMainSleep"]),
            "logId": int(sleep["logId"]),
            "logType": sleep["logType"],
            "minutesAfterWakeup": int(sleep["minutesAfterWakeup"]),
            "minutesAsleep": int(sleep["minutesAsleep"]),
            "minutesAwake": int(sleep["minutesAwake"]),
            "minutesToFallAsleep": int(sleep["minutesToFallAsleep"]),
            "startTime": pd.to_datetime(sleep["startTime"]),
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

        rows.append(row)

    sleep_df = pd.DataFrame(rows)
    parquet_filename = filename.replace(".json", ".parquet")
    sleep_df.to_parquet(parquet_filename)
    # print(sleep_df.info())
    print(sleep_df.head())

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
        zname = zone_map[heartrate["value"]["heartRateZones"][0]["name"]]
        row = {
            "dateTime": pd.to_datetime(heartrate["dateTime"]),

            "Zone1_caloriesOut": float(heartrate["value"]["heartRateZones"][0]["caloriesOut"]),
            "Zone1_max_heartrate": int(heartrate["value"]["heartRateZones"][0]["max"]),
            "Zone1_min_heartrate": int(heartrate["value"]["heartRateZones"][0]["min"]),
            "Zone1_minutes": int(heartrate["value"]["heartRateZones"][0]["minutes"]),

            "Zone3_caloriesOut": float(heartrate["value"]["heartRateZones"][1]["caloriesOut"]),
            "Zone3_max_heartrate": int(heartrate["value"]["heartRateZones"][1]["max"]),
            "Zone3_min_heartrate": int(heartrate["value"]["heartRateZones"][1]["min"]),
            "Zone3_minutes": int(heartrate["value"]["heartRateZones"][1]["minutes"]),

            "Zone3_caloriesOut": float(heartrate["value"]["heartRateZones"][2]["caloriesOut"]),
            "Zone3_max_heartrate": int(heartrate["value"]["heartRateZones"][2]["max"]),
            "Zone3_min_heartrate": int(heartrate["value"]["heartRateZones"][2]["min"]),
            "Zone3_minutes": int(heartrate["value"]["heartRateZones"][2]["minutes"]),

            "Zone4_caloriesOut": float(heartrate["value"]["heartRateZones"][3]["caloriesOut"]),
            "Zone4_max_heartrate": int(heartrate["value"]["heartRateZones"][3]["max"]),
            "Zone4_min_heartrate": int(heartrate["value"]["heartRateZones"][3]["min"]),
            "Zone4_minutes": int(heartrate["value"]["heartRateZones"][3]["minutes"])
        }

        rows.append(row)

    heartrate_df = pd.DataFrame(rows)
    parquet_filename = filename.replace(".json", ".parquet")
    heartrate_df.to_parquet(parquet_filename)
    print(heartrate_df.head())

if __name__ == '__main__':
    for filename in glob.glob("sleep*.json"):
        sleep_json_to_parquet(filename)

    for filename in glob.glob("profile*.json"):
        profile_json_to_parquet(filename)

    for filename in glob.glob("heartrate*.json"):
        heartrate_json_to_parquet(filename)

