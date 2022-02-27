import pandas
import numpy

class EventDetector:
	'''The base class of a various detectors'''
	def __init__(self, gaze_data:pandas.DataFrame) -> None:
		self.gaze_data:pandas.DataFrame = gaze_data
		self.fixation:list = []
		self.saccade:list = []


	def _calculateSphericalCoordinate(self, row: pandas.Series, varName: str) -> tuple:
		x = row['{}_x'.format(varName)]
		y = row['{}_y'.format(varName)]
		z = row['{}_z'.format(varName)]

		azimuth = numpy.rad2deg(numpy.arctan(numpy.divide(x,z)))
		elevation = numpy.rad2deg(numpy.arctan(numpy.divide(y,z)))

		return (azimuth, elevation)

	def process_data(self) -> None:
		'''Process and generate data needed by this detector'''
		# normalize time
		self.gaze_data["vidTimeStamp"] = self.gaze_data['gaze_timestamp'] - self.gaze_data['gaze_timestamp'].iloc[0]
		SphericalCoordinates:pandas.Series = self.gaze_data.apply(lambda rowInterator: self._calculateSphericalCoordinate(rowInterator, "gaze_point_3d"), axis=1)
		self.gaze_data['gaze_az'],self.gaze_data['gaze_el'] = zip(*SphericalCoordinates)

class IDT_Detector(EventDetector):
	'''The event detector class using IDT algorithm'''
	def __init__(self, gaze_data:pandas.DataFrame, window_size:int, dispersion_threshold:float) -> None:
		super().__init__(gaze_data)
		self.window_size:int = window_size # defines how many rows of data that a window contains.
		self.dispersion_threshold:float = dispersion_threshold # defines the threshold for classification
		self.window = [0, window_size] # the end index is not included
	
	def window_move(self) -> bool:
		'''move the window right by 1 step. Return True if success'''
		# if the ending index does not exceed the data ending index
		new_start = self.window[0] + 1
		new_end = self.window[1] + 1
		if new_end < self.gaze_data.shape[0]:
			self.window[0] = new_start
			self.window[1] = new_end
			return True
		else:
			print("Move Reached the end of the data set")
			#print("Debug: ", self.window)
			return False

	def window_expand(self) -> bool:
		'''expand the window right by 1 step, Return True if success'''
		new_end = self.window[1] + 1
		if new_end < self.gaze_data.shape[0]:
			self.window[1] = new_end
			return True
		else:
			print("Expand Reached the end of the data set")
			#print("Debug: ", self.window)
			return False

	def window_reset(self) -> bool:
		'''Reset window after finding a fixation'''
		new_start:int = self.window[1] + 1
		new_end:int = self.window[1] + 1 + self.window_size
		if new_start >= self.gaze_data.shape[0]:
			print("Reset reached the end of the data set")
			#print("Debug: ", self.window)
			return False
		elif new_start < self.gaze_data.shape[0] and new_end >= self.gaze_data.shape[0]:
			print("Reset reached the end of the data set")
			#print("Debug: ", self.window)
			self.window = [new_start, self.gaze_data.shape[0]]
			return True
		else:
			self.window = [new_start, new_end]
			return True

	def calculateDispersion(self) -> float:
		'''Calculate the D, D=[max(x) - min(x)] + [max(y) - min(y)]'''
		minAz = self.gaze_data["gaze_az"][self.window[0]:self.window[1]].min() # beware that [0:a) not including a.
		maxAz = self.gaze_data["gaze_az"][self.window[0]:self.window[1]].max()
		minEl = self.gaze_data["gaze_el"][self.window[0]:self.window[1]].min()
		maxEl = self.gaze_data["gaze_el"][self.window[0]:self.window[1]].max()

		D = (maxAz - minAz) + (maxEl - minEl)
		return D

	def detect(self) -> None:
		'''Start detection'''
		print("Starting IDT Detection..")
		dispersion = self.calculateDispersion()
		while True:
			dispersion = self.calculateDispersion()
			#print("Debug: window", self.window)
			if dispersion < self.dispersion_threshold:
				#print("Debug: Found a fixation, now testing its length..", self.window)
				# if this is a fixation
				expand_end = False
				while dispersion < self.dispersion_threshold and expand_end != True:
					## expand and calcualte dispersion until dispersion exceed the threshold
					expand_result = self.window_expand()
					if expand_result != False:
						dispersion = self.calculateDispersion()
					else:
						expand_end = True
				# then add this window period to the fixation list, and reset window
				self.fixation.append(self.window.copy())
				#print("Debug: a Fixation set", self.window)
				reset_result = self.window_reset()
				if reset_result == False:
					break
				else:
					pass
					#print("Debug: reseting window to", self.window)
			else:
				move_result:bool = self.window_move()
				if move_result == False:
					break
		print("IDT Detection Finished.")

class IVT_Detector(EventDetector):

	def __init__(self, gaze_data: pandas.DataFrame, velocity_threshold:float) -> None:
		super().__init__(gaze_data)
		self.velocity_threshold = velocity_threshold


	def calculateVelocity(self):
		self.gaze_data["displace_az"] = self.gaze_data["gaze_az"].diff()
		self.gaze_data["displace_el"] = self.gaze_data["gaze_el"].diff()
		self.gaze_data["delta_time"] = self.gaze_data["vidTimeStamp"].diff()

		# self.gaze_data["velocity_az"] = self.gaze_data["displace_az"] / self.gaze_data["delta_time"]
		# self.gaze_data["velocity_el"] = self.gaze_data["displace_el"] / self.gaze_data["delta_time"]

		self.gaze_data["displace"] = numpy.sqrt(
			self.gaze_data["displace_az"] * self.gaze_data["displace_az"] +
			self.gaze_data["displace_el"] * self.gaze_data["displace_el"]
			)


		self.gaze_data["velocity"] = self.gaze_data["displace"] / self.gaze_data["delta_time"]
		#self.gaze_data["velocity"] = self.gaze_data["velocity_az"] + self.gaze_data["velocity_el"]


		#print(self.gaze_data["displace"])
		#print(self.gaze_data["delta_time"])
		#print(self.gaze_data["velocity"])

	def detect(self):
		saccade_start:int = 0
		saccade_end:int = 0
		inSaccade:bool = False
		for i in range(0, self.gaze_data.shape[0]) :
			if self.gaze_data["velocity"].iloc[i] > self.velocity_threshold and inSaccade == False: # if find a saccade start
				saccade_start = i
				inSaccade = True
			elif self.gaze_data["velocity"].iloc[i] < self.velocity_threshold and inSaccade == True: # if find a saccade end
				saccade_end = i
				inSaccade = False
				self.saccade.append([saccade_start, saccade_end])

