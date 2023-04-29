#####
# 
# This class is part of the Programming the Internet of Things project.
# 
#

import logging

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst
from .tools.HTS221 import HTS221

class TemperatureI2cSensorAdapterTask(BaseSensorSimTask):
	"""
	This class is used to facilitate communication between a physical SenseHAT temperature sensor and the Constrained Device Application via I2C 
	
	"""

	def __init__(self):
		
		super(TemperatureI2cSensorAdapterTask, self).__init__(name = ConfigConst.TEMP_SENSOR_NAME, typeID = ConfigConst.TEMP_SENSOR_TYPE)

		self._temp = HTS221(1)
		
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(name = self.getName(), typeID = self.getTypeID())
		sensorVal = self._temp.read_temp()
				
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		
		return sensorData
	
	def getTelemetryValue(self) -> float:
		return self.latestSensorData.getValue()
	