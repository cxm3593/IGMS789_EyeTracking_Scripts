import pandas
import numpy
import os
from pandas import DataFrame

GAZE_FILENAME:str = "gaze_positions.csv"
PUPIL_FILENAME:str = "pupil_positions.csv"

class DataManager:
	'''
	A Data manager could load and store gaze and pupil data
	'''
	def __init__(
		self,
		data_path:str
	):
		print("Creating DataManager")
		self.data_path:str = data_path
		self.gaze_path:str = None
		self.pupil_path:str = None
		self.gaze_data:DataFrame = None
		self.pupil_data:DataFrame = None
		print("DataManager created.")

	def initilizeData(self):
		"""Load both gaze and pupil data with pandas"""
		print("Initializing Data...")
		self.gaze_path = os.path.join(self.data_path, GAZE_FILENAME)
		self.pupil_path = os.path.join(self.data_path, PUPIL_FILENAME)
		self.gaze_data = pandas.read_csv(self.gaze_path)
		self.pupil_data = pandas.read_csv(self.pupil_path)
		print("Done.")
