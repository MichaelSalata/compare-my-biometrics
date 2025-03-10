import json
import pandas as pd


# def sleep_json_to_parquet(filename):





dimension = "sleep"
filename = f"{dimension}.json"


def profile_json_to_parquet(filename):
    try:
        with open(filename, 'r') as file:
            profile_data = json.load(file)["user"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file} file: {e}")
        exit(1)
    
    del profile_data["features"]
    del profile_data["topBadges"]
    print(profile_data)
    profile_df = pd.DataFrame([profile_data])

    # Create DataFrame
    
    parquet_filename = filename.replace(".json", ".parquet")
    profile_df.to_parquet(parquet_filename)
    # print(profile_df.info())
    # print(profile_df.head())


def sleep_json_to_parquet(filename):
    try:
        with open(filename, 'r') as file:
            sleep_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file} file: {e}")
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
    # print(sleep_df.head())

if __name__ == '__main__':
    sleep_json_to_parquet("sleep.json")
    profile_json_to_parquet("profile.json")
