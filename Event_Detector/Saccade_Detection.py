import numpy
from Library.DataManager import DataManager
import pandas
import plotly

## Variables ## 
data_path = "E:/Eye Tracking Recordings/2022_01_28/004/exports/000"


## main program ##
data_manager = DataManager(data_path)
data_manager.initilizeData()

print(data_manager.gaze_data)