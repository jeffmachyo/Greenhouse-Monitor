#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# 
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData



class SystemPerformanceManager(object):
	"""
	This class will be used to control the system tools that will be required by the Constrained Device Application. 
	It will be used to control the systemCpuUtil task and the SystemMemUtilTask classes. It is also tasked with invoking 
	an apscheduler that will continuously update the system parameters that are being monitored.
	
	"""

	def __init__(self,listener:IDataMessageListener = None):
		configUtil=ConfigUtil()
		self.pollRate = configUtil.getInteger(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		self.locationID = configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		if (self.pollRate <= 0):
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		self.dataMsgListener = listener
		
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
	
		self.cpuUtilTask = SystemCpuUtilTask()
		self.memUtilTask = SystemMemUtilTask()

		

		self._managerRunning = False

	def handleTelemetry(self):
		self.cpuUtilTelemetry = self.cpuUtilTask.getTelemetryValue()
		self.memUtilTelemetry = self.memUtilTask.getTelemetryValue()

		logging.debug('CPU utilization is %s percent, and memory utilization is %s percent.', str(self.cpuUtilTelemetry), str(self.memUtilTelemetry))
	
		sysPerfData = SystemPerformanceData()
		sysPerfData.setLocationID(self.locationID)
		sysPerfData.setCpuUtilization(self.cpuUtilTelemetry)
		sysPerfData.setMemoryUtilization(self.memUtilTelemetry)
	
		if (self.dataMsgListener):
			self.dataMsgListener.handleSystemPerformanceMessage(data = sysPerfData)
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		self.dataMsgListener = listener
	
	def startManager(self):
		logging.info("Started SystemPerformanceManager.")
		
		if (not self.scheduler.running):
			self.isRunning = True
			self.scheduler.start()
			logging.info("Started SystemPerformanceManager.")
		else:
			logging.warning("SystemPerformanceManager scheduler already started. Ignoring.")
		
	def stopManager(self):
		logging.info("Stopping SystemPerformanceManager.")
		
		try:
			self.scheduler.shutdown()
			self.isRunning = False
			logging.info("Stopped SystemPerformanceManager.")
		except:
			logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring.")

	@property
	def isRunning(self) -> bool:
		return self._managerRunning

	@isRunning.setter
	def isRunning(self,val):
		self._managerRunning = val