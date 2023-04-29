#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# 
#

import logging

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst
from .tools.HTS221 import HTS221


class HumidityI2cSensorAdapterTask(BaseSensorSimTask):
	"""
	This class is used to facilitate communication between a physical SenseHAT humidity sensor and the Constrained Device Application via I2C 
	
	"""

	def __init__(self):
		
		super(HumidityI2cSensorAdapterTask, self).__init__(name = ConfigConst.HUMIDITY_SENSOR_NAME, typeID = ConfigConst.HUMIDITY_SENSOR_TYPE)

		self._humidity = HTS221(1)
		
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(name = self.getName(), typeID = self.getTypeID())
		sensorVal = self._humidity.read_humidity()
				
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		
		return sensorData
	
	def getTelemetryValue(self) -> float:
		return self.latestSensorData.getValue()
	