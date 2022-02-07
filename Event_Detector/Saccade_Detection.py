import numpy
from Library.EventDetector import IDT_Detector
from Library.DataManager import DataManager
from Library.DataPlotter import DataPlotter
import pandas
import plotly

## Variables ## 
data_path = "E:/Eye Tracking Recordings/2022_01_28/004/exports/000"

### Important values
# and dispersion should be 0.5deg-1deg in dispersion angle. In this IDT we use spherical coordinate instead of xy coordinate
dispersion_threshold =  1#

# window size: the window should be about 100ms, this will be calculated based on sample rate
window_size = 0

## main program ##
data_manager = DataManager(data_path)
data_manager.initilizeData()

gaze_sample_rate = data_manager.find_gaze_SampleRate()
window_size = int(gaze_sample_rate * (1/10))

# IDT
idt_detector = IDT_Detector(data_manager.gaze_data, window_size, dispersion_threshold)
idt_detector.process_data()
idt_detector.detect()

# Data Plot
plotter = DataPlotter(
	["gaze_az", "gaze_el"],
	idt_detector.gaze_data
)
plotter.plot(idt_detector.fixation)