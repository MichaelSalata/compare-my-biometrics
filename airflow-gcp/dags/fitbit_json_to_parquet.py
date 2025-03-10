import json
import pandas as pd


# def sleep_json_to_parquet(filename):

dimension = "sleep"
filename = f"{dimension}.json"
with open(filename, 'r') as file:
    data = json.load(file)

sleep = pd.json_normalize(data)


# Parse JSON
# data = json.loads(json_data)

# Extract sleep data
sleep_data = data["sleep"]

# Transform into structured format
rows = []
for sleep in sleep_data:
    # levels = sleep["levels"]["summary"]
    if not sleep["isMainSleep"]:
        continue

    # print(sleep["levels"]["summary"])

    # TODO: Modularize the appending of row data
    """
    row = sleep.copy()
    row.drop("levels")
    for k in sleep.keys():
        if k != "levels":
            row[k]:sleep[k]"""

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

# Create DataFrame
df = pd.DataFrame(rows)
df.to_parquet(f"{dimension}.parquet")
print(df)
# df.info()

"""
,
        "deep_count": sleep["levels"]["summary"]["deep"]["count"],
        "deep_minutes": sleep["levels"]["summary"]["deep"]["minutes"],
        "light_count": sleep["levels"]["summary"]["light"]["count"],
        "light_minutes": sleep["levels"]["summary"]["light"]["minutes"],
        "rem_count": sleep["levels"]["summary"]["rem"]["count"],
        "rem_minutes": sleep["levels"]["summary"]["rem"]["minutes"],
        "wake_count": sleep["levels"]["summary"]["wake"]["count"],
        "wake_minutes": sleep["levels"]["summary"]["wake"]["minutes"]
"""

"""
{
    "sleep": [
        {
            "dateOfSleep": "2025-03-07",
            "duration": 16440000,
            "efficiency": 91,
            "endTime": "2025-03-07T02:31:00.000",
            "infoCode": 0,
            "isMainSleep": true,
            "levels": {
                "data": [...],
                "shortData": [...],
                "summary": {
                    "deep": {
                        "count": 2,
                        "minutes": 29,
                        "thirtyDayAvgMinutes": 62
                    },
                    "light": {
                        "count": 14,
                        "minutes": 173,
                        "thirtyDayAvgMinutes": 197
                    },
                    "rem": {
                        "count": 4,
                        "minutes": 36,
                        "thirtyDayAvgMinutes": 69
                    },
                    "wake": {
                        "count": 11,
                        "minutes": 36,
                        "thirtyDayAvgMinutes": 54
                    }
                }
            },
            "logId": 48577547244,
            "logType": "auto_detected",
            "minutesAfterWakeup": 9,
            "minutesAsleep": 238,
            "minutesAwake": 36,
            "minutesToFallAsleep": 0,
            "startTime": "2025-03-06T21:57:00.000",
            "timeInBed": 274,
            "type": "stages"
        }
    ]
}
I have included a portion of the json file I want to parse into a dataframe.
I want to create a dataframe table with columns named after "dateOfSleep", "duration", "efficiency", etc...
I want to reformat the sections on "deep", "light" and "rem" to be columns on their own. e.g. "deep_count", "deep_minutes", etc...
"""



"""
    row = {
        "dateOfSleep": sleep["dateOfSleep"],
        "duration": sleep["duration"],
        "efficiency": sleep["efficiency"],
        "infoCode": sleep["infoCode"],
        "endTime": sleep["endTime"],
        "startTime": sleep["startTime"],
        "minutesAsleep": sleep["minutesAsleep"],
        "minutesAwake": sleep["minutesAwake"],
        "minutesAfterWakeup": sleep["minutesAfterWakeup"],
        "timeInBed": sleep["timeInBed"],

        "deep_count": sleep["levels"]["summary"]["deep"]["count"],
        "deep_minutes": sleep["levels"]["summary"]["deep"]["minutes"],
        "deep_thirtyDayAvgMinutes": sleep["levels"]["summary"]["deep"]["thirtyDayAvgMinutes"],

        "light_count": sleep["levels"]["summary"]["light"]["count"],
        "light_minutes": sleep["levels"]["summary"]["light"]["minutes"],
        "light_thirtyDayAvgMinutes": sleep["levels"]["summary"]["light"]["thirtyDayAvgMinutes"],

        "rem_count": sleep["levels"]["summary"]["rem"]["count"],
        "rem_minutes": sleep["levels"]["summary"]["rem"]["minutes"],
        "rem_thirtyDayAvgMinutes": sleep["levels"]["summary"]["rem"]["thirtyDayAvgMinutes"],

        "wake_count": sleep["levels"]["summary"]["wake"]["count"],
        "wake_minutes": sleep["levels"]["summary"]["wake"]["minutes"],
        "wake_thirtyDayAvgMinutes": sleep["levels"]["summary"]["wake"]["thirtyDayAvgMinutes"]
    }
"""







































# df_name.to_parquet(filename, index=False)


if __name__ == '__main__':
    sleep_json_to_parquet("sleep.json")

