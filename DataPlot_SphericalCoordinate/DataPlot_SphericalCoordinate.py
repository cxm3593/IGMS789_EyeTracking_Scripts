from unicodedata import name
from matplotlib.axis import XAxis
import plotly
import pandas
from pandas import Series
import numpy
import os

# Variables
DirectoryPath:str = "Data"
TargetFile:str = "gaze_positions.csv"
vector_name:str = "gaze_point_3d"
plot_width:int = 800
plot_height:int = 600
plot_marker_size = 5
plot_opacity = 0.8
plot_layout = dict(
		title='Data plot: Spherical Coordinate data - time',
		width=plot_width,
		height=plot_height,
		yaxis=dict(range=[-100,100], title='angular position (degrees)'),
		xaxis=dict(
			rangeslider=dict(visible=True),
			range=[0,500],
			title='time (miliseconds)'
		)
	)


# Data Input
DataPath:str = os.path.join(DirectoryPath, TargetFile)
data:str = pandas.read_csv(DataPath)

# Data Processing 
def calculateSphericalCoordinate(row: Series, varName: str) -> tuple:
	x = row['{}_x'.format(varName)]
	y = row['{}_y'.format(varName)]
	z = row['{}_z'.format(varName)]

	azimuth = numpy.rad2deg(numpy.arctan(numpy.divide(x,z)))
	elevation = numpy.rad2deg(numpy.arctan(numpy.divide(y,z)))

	return (azimuth, elevation)


SphericalCoordinates:Series = data.apply(lambda rowInterator: calculateSphericalCoordinate(rowInterator, vector_name), axis=1)
data['gaze_az'],data['gaze_el'] = zip(*SphericalCoordinates)

# Plot Data
## First process timestamp
normalized_timestamps = numpy.array(data['gaze_timestamp'] - data['gaze_timestamp'].iloc[0])
time_miliseconds = numpy.arange(len(normalized_timestamps))

## Plot
az_graph:plotly.graph_objects.scattergl = plotly.graph_objects.Scattergl(
	x = time_miliseconds,
	y = data['gaze_az'],
	name = "Gaze Direction in Spherical Coordinate (azimuth)",
	mode='markers',
	marker_size = plot_marker_size,
	opacity = plot_opacity
)

el_graph:plotly.graph_objects.scattergl = plotly.graph_objects.Scattergl(
	x = time_miliseconds,
	y = data['gaze_el'],
	name = "Gaze Direction in Spherical Coordinate (elevation)",
	mode='markers',
	marker_size = plot_marker_size,
	opacity = plot_opacity
)

figure: plotly.graph_objects.Figure = plotly.graph_objects.Figure(
	data = [az_graph, el_graph],
	layout = plot_layout
)

figure.show()

# Testing Area for Debug
#print(type(data.iloc[0]))
#print(data["gaze_timestamp"] - data["gaze_timestamp"].iloc[0])
