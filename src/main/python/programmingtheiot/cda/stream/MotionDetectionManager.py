#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.IotDataContext import IotDataContext
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataManager import IDataManager
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.stream.CameraStreamMonitorTask import CameraStreamMonitorTask

class MediaData(IDataManager):
	"""
	Shell representation of class for student implementation.
	
	"""
		
	def __init__(self):

		self.enableAdapter = True
		self.dataMsgListener = None

		logging.info("Importing CameraStreamMonitorTaskModule...")

		self.camMonitorTask = CameraStreamMonitorTask()
		self.isStarted = False

		logging.info("Instantiated CameraStreamMonitorTask class...")

	# def getRateInSeconds(self) -> int:

	# 	return self.rateinSec
	def isStreamStarted(self) -> bool:

		return self.isStarted
	
	def setDataMessageListener(self, listener: IDataMessageListener = None):
		
		if listener:
			self.dataMsgListener = listener
			self.camMonitorTask.setDataMessageListener(listener)

	def setEnableAdapterFlag(self,enable):

		self.enableAdapter = enable

	def startManager(self) -> bool:
		logging.info("Starting camera stream monitor...")

		if (not self.camMonitorTask.isStreamStarted()):
			self.isStarted = self.camMonitorTask.startStream()
			logging.info("Camera stream monitor now started...") 

			return True
		
		else:
			logging.warning("Camera stream already started. Ignoring...")


			return False
		
	def stopManager(self) -> bool:
		logging.info("Stopping camera stream monitor...")

		try:
			pass

		except Exception as e:
			print(e.with_traceback())
	
	