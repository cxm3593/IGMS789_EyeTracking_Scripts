import pandas as pd
import matplotlib.pyplot as plt

data_link = "E:/Eye Tracking Recordings/2022_01_12_IMGS789-FirstRecording/exports/001/gaze_positions.csv"

df = pd.read_csv(data_link)

timestamps = df["gaze_timestamp"]

def normalizeTimeStamps(timestamps):
	base_stamp = timestamps[0]
	for i in range(0, len(timestamps)):
		timestamps[i] = timestamps[i] - base_stamp

def sliceDataByTime(start_time, end_time, data, normalized_timestamps):
	clip_start = 0
	clip_start_find = False
	clip_end = len(data)
	clip_end_find = False
	for i in range(0, len(data)):
		if normalized_timestamps[i] >= start_time and clip_start_find == False:
			clip_start = i
			clip_start_find = True
			print("Debug: clipstart = ", i, "time = ", normalized_timestamps[i])
		elif normalized_timestamps[i] >= end_time and clip_end_find == False:
			clip_end = i
			clip_end_find = True
			print("Debug: clipend = ", i, "time = ", normalized_timestamps[i])
			break
	print("Debug: time period:", timestamps[clip_start], timestamps[clip_end])
	return data[clip_start: clip_end]

normalizeTimeStamps(timestamps)
#plt.plot(timestamps, df["confidence"]) # time against confidence

# Plot y to x over period 0'39'' to 1'49''
period_x = sliceDataByTime(39, 109, df["norm_pos_x"], timestamps)
period_y = sliceDataByTime(39, 109, df["norm_pos_y"], timestamps)
plt.plot(period_x, period_y)
plt.show()