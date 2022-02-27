from matplotlib.pyplot import figure
import plotly
import pandas
from pandas import DataFrame, Series
import numpy
import os

class DataPlotter:
	plot_width:int = 1280
	plot_height:int = 720
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

	def __init__(self, plot_namelist:str, data:DataFrame) -> None:
		self.plot_namelist = plot_namelist
		self.data:DataFrame = data

	def _drawHighLight(
			self,
			index_pairs,
			time:numpy.ndarray, 
			figure:plotly.graph_objects.Figure,
			color:str = "LightSalmon"
		):
		'''Given [[i1, i2], [i3, i4]...], draw patch on the plot'''
		for pair in index_pairs:
			start_index = pair[0]
			end_index = pair[1]
			start_time = time[start_index]
			end_time = time[end_index]

			figure.add_vrect(
				x0=start_time, x1=end_time,
				fillcolor=color, opacity=0.5,
				layer="below", line_width=0,
			)


	def plot(self, index_pairs = None, color:str = "LightSalmon", timeColumnName = "gaze_timestamp") -> None:


		normalized_timestamps:numpy.ndarray = numpy.array(self.data[timeColumnName] - self.data[timeColumnName].iloc[0])

		#time:numpy.ndarray = numpy.arange(len(normalized_timestamps))
		time:numpy.ndarray = normalized_timestamps

		graph_list = []
		for data_name in self.plot_namelist:
			graph:plotly.graph_objects.scattergl = plotly.graph_objects.Scattergl(
				x = time,
				y = self.data[data_name],
				name = data_name,
				mode='markers',
				marker_size = DataPlotter.plot_marker_size,
				opacity = DataPlotter.plot_opacity
			)
			graph_list.append(graph)
		
		figure: plotly.graph_objects.Figure = plotly.graph_objects.Figure(
			data = graph_list,
			layout = DataPlotter.plot_layout
		)

		if index_pairs != None:
			self._drawHighLight(index_pairs, time, figure)

		figure.show()




