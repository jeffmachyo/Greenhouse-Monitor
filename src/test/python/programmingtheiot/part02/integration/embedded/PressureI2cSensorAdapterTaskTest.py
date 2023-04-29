#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.embedded.PressureI2cSensorAdapterTask import PressureI2cSensorAdapterTask

class PressureI2cSensorAdapterTaskTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	PressureI2cSensorAdapterTaskTest. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	
	NOTE: This test requires the physical senseHAT on a Raspberry Pi
	
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing PressureI2cSensorAdapterTask class [using SenseHAT on a Raspberry Pi]...")
		self.pressureSensingTask = PressureI2cSensorAdapterTask()
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testReadEmulator(self):
		sd1 = self.pressureSensingTask.generateTelemetry()
		
		if sd1:
			self.assertEqual(sd1.getTypeID(), ConfigConst.PRESSURE_SENSOR_TYPE)
			logging.info("SensorData: %f - %s", sd1.getValue(), str(sd1))
			
			# wait 5 seconds
			sleep(5)
		else:
			logging.warning("FAIL: SensorData is None.")
			
		sd2 = self.pressureSensingTask.generateTelemetry()
		
		if sd2:
			self.assertEqual(sd2.getTypeID(), ConfigConst.PRESSURE_SENSOR_TYPE)
			logging.info("SensorData: %f - %s", sd2.getValue(), str(sd2))
			
			# wait 5 seconds
			sleep(5)
		else:
			logging.warning("FAIL: SensorData is None.")
			
if __name__ == "__main__":
	unittest.main()
	