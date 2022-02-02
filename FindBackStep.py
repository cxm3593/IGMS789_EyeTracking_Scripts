import pandas as pd

data_link = "E:/Eye Tracking Recordings/2022_01_12_IMGS789-FirstRecording/exports/001/gaze_positions.csv"

df = pd.read_csv(data_link)

hold = df["gaze_timestamp"][0]
for i in range(0, len(df["gaze_timestamp"])):
    if i > 0:
        hold = df["gaze_timestamp"][i-1]
        if df["gaze_timestamp"][i] < hold:
            print(df["gaze_timestamp"][i], df["base_data"][i])