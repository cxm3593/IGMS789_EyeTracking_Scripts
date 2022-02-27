import pandas
import numpy

class DataFilter:
	def __init__(self, dataFrame:pandas.DataFrame) -> None:
		self.dataFrame = dataFrame



	def applyWindowAverage(self, window_size:int, dataName:str):
		outputDataName = dataName + "_WAfilter"
		self.dataFrame[outputDataName] = self.dataFrame[dataName].rolling(window_size, min_periods=1).mean()

	def applyMedianFilter(self, window_size:int, dataName:str):
		outputDataName = dataName + "_MedianFilter"
		self.dataFrame[outputDataName] = self.dataFrame[dataName].rolling(window_size, min_periods=1, center=True).median()
