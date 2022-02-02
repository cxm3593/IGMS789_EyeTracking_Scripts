import pandas as pd

data_link = "E:/Eye Tracking Recordings/2022_01_12_IMGS789-FirstRecording/exports/001/pupil_positions.csv"
df = pd.read_csv(data_link)



# eye0_samples = df[(df.eye_id==1)].shape[0]
# eye0_time = df[(df.eye_id==1)]["pupil_timestamp"].iloc[-1] - df[(df.eye_id==1)]["pupil_timestamp"].iloc[0]

eye0_samples = df.shape[0]
eye0_time = df["pupil_timestamp"].iloc[-1] - df["pupil_timestamp"].iloc[0]

print("total eye0 samples:", eye0_samples) # print rows for eye0
print("total eye0 time:", eye0_time) 
print("eye0 sample rate: ", eye0_samples / eye0_time)


