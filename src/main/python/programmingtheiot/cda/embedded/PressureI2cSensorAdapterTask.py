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
from .tools.LPS25H import LPS25H


class PressureI2cSensorAdapterTask(BaseSensorSimTask):
	"""
	This class is used to facilitate communication between a physical SenseHAT pressure sensor and the Constrained Device Application via I2C 
	
	"""

	def __init__(self):
		
		super(PressureI2cSensorAdapterTask, self).__init__(name = ConfigConst.PRESSURE_SENSOR_NAME, typeID = ConfigConst.PRESSURE_SENSOR_TYPE)

		self._pressure = LPS25H(1)
		
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(name = self.getName(), typeID = self.getTypeID())
		sensorVal = self._pressure.read_pressure()
				
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		
		return sensorData
	
	def getTelemetryValue(self) -> float:
		return self.latestSensorData.getValue()
	