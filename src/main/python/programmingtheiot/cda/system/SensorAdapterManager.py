#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self,listener:IDataMessageListener = None):
		configUtil=ConfigUtil()

		self.useSimulatorConfig = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_SIMULATOR_KEY, False)
		self.useEmulatorConfig = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_EMULATOR_KEY, False)
		self.useSenseHatConfig = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_SENSE_HAT_KEY, False)

		self.pollRate = configUtil.getInteger(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		self.locationID = configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)

		if (self.useSimulatorConfig):

			self.tempCeiling =  configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_CEILING_KEY, SensorDataGenerator.MAX_ENV_TEMP, False)
			self.tempFloor =  configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_FLOOR_KEY, SensorDataGenerator.MIN_ENV_TEMP, False)

			self.humidityCeiling =  configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_CEILING_KEY,SensorDataGenerator.MAX_ENV_HUMIDITY, False)
			self.humidityFloor =  configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_FLOOR_KEY, SensorDataGenerator.MIN_ENV_HUMIDITY, False)

			self.pressureCeiling =  configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_CEILING_KEY, SensorDataGenerator.MAX_ENV_PRESSURE, False)
			self.pressureFloor =  configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_FLOOR_KEY , SensorDataGenerator.MIN_ENV_PRESSURE, False)

		
			sensorDataGenerator = SensorDataGenerator(alignGeneratorToDay = True)
		
			self.tempData = sensorDataGenerator.generateDailyIndoorTemperatureDataSet(noiseLevel = 15, minValue = self.tempFloor, maxValue = self.tempCeiling,useSeconds = False)
		
			self.humidityData = sensorDataGenerator.generateDailyEnvironmentHumidityDataSet(noiseLevel = 10, minValue = self.humidityFloor, maxValue = self.humidityCeiling,useSeconds = False)
		
			self.pressureData = sensorDataGenerator.generateDailyEnvironmentPressureDataSet(noiseLevel = 1, minValue = self.pressureFloor, maxValue = self.pressureCeiling,useSeconds = False)


		
		if (self.pollRate <= 0):
			logging.debug("The poll rate defined: "+str(self.pollRate)+" cannot be used here. Transitioning to default: "+str(ConfigConst.DEFAULT_POLL_CYCLES))
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES

		else:
			logging.debug("The poll rate defined is: "+str(self.pollRate))
			
		self.dataMsgListener = listener

		
		self.humidityAdapter = None
		self.pressureAdapter = None
		self.tempAdapter     = None
		
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
		self._managerRunning = False

		#If we have enabled an emulator
		if (self.useEmulatorConfig):
			logging.info("Emulator use enabled..")
			humiditySensorModule = import_module('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask', 'HumiditySensorEmulatorTask')
			humiditySensorEmulatorAdapter = getattr(humiditySensorModule, 'HumiditySensorEmulatorTask')
			self.humidityAdapter = humiditySensorEmulatorAdapter()
			
			pressureSensorModule = import_module('programmingtheiot.cda.emulated.PressureSensorEmulatorTask', 'PressureSensorEmulatorTask')
			pressureSensorEmulatorAdapter = getattr(pressureSensorModule, 'PressureSensorEmulatorTask')
			self.pressureAdapter = pressureSensorEmulatorAdapter()
			
			temperatureSensorModule = import_module('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask', 'TemperatureSensorEmulatorTask')
			temperatureSensorEmulatorAdapter = getattr(temperatureSensorModule, 'TemperatureSensorEmulatorTask')
			self.tempAdapter = temperatureSensorEmulatorAdapter()

		#If we have enabled a simulator
		elif (self.useSimulatorConfig):
			logging.info("Simulator use enabled...")
			self.humidityAdapter = HumiditySensorSimTask(self.humidityData)
			self.pressureAdapter = PressureSensorSimTask(self.pressureData)
			self.tempAdapter     = TemperatureSensorSimTask(self.tempData)

		#If we have enable the Physical SenseHAT
		elif (self.useSenseHatConfig):
			logging.info("Physical SenseHAT use enabled..")
			humiditySensorModule = import_module('programmingtheiot.cda.embedded.HumidityI2cSensorAdapterTask', 'HumidityI2cSensorAdapterTask')
			humiditySensorEmulatorAdapter = getattr(humiditySensorModule, 'HumidityI2cSensorAdapterTask')
			self.humidityAdapter = humiditySensorEmulatorAdapter()
			
			pressureSensorModule = import_module('programmingtheiot.cda.embedded.PressureI2cSensorAdapterTask', 'PressureI2cSensorAdapterTask')
			pressureSensorEmulatorAdapter = getattr(pressureSensorModule, 'PressureI2cSensorAdapterTask')
			self.pressureAdapter = pressureSensorEmulatorAdapter()
			
			temperatureSensorModule = import_module('programmingtheiot.cda.embedded.TemperatureI2cSensorAdapterTask', 'TemperatureI2cSensorAdapterTask')
			temperatureSensorEmulatorAdapter = getattr(temperatureSensorModule, 'TemperatureI2cSensorAdapterTask')
			self.tempAdapter = temperatureSensorEmulatorAdapter()


		else:
			logging.warning("No simulator, emulator or physical senseHAT enabled...")
		

	def handleTelemetry(self):
		humidityData = self.humidityAdapter.generateTelemetry()
		pressureData = self.pressureAdapter.generateTelemetry()
		tempData     = self.tempAdapter.generateTelemetry()
		
		humidityData.setLocationID(self.locationID)
		pressureData.setLocationID(self.locationID)
		tempData.setLocationID(self.locationID)
		
		logging.debug('Generated humidity data: '+ str(humidityData))
		logging.debug('Generated pressure data: ' + str(pressureData))
		logging.debug('Generated temp data: ' + str(tempData))
		
		if self.dataMsgListener:
			self.dataMsgListener.handleSensorMessage(humidityData)
			self.dataMsgListener.handleSensorMessage(pressureData)
			self.dataMsgListener.handleSensorMessage(tempData)
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		self.dataMsgListener = listener

	
	def startManager(self):
		logging.info("Started SensorAdapterManager.")
	
		if not self.scheduler.running:
			self.isRunning = True
			self.scheduler.start()
			return True
		else:
			logging.info("SensorAdapterManager scheduler already started. Ignoring.")
			return False
		
	def stopManager(self):
		logging.info("Stopped SensorAdapterManager.")
	
		try:
			self.scheduler.shutdown()
			self.isRunning = False
			return True
		except:
			logging.info("SensorAdapterManager scheduler already stopped. Ignoring.")
			return False

	@property
	def isRunning(self) -> bool:
		return self._managerRunning

	@isRunning.setter
	def isRunning(self,val):
		self._managerRunning = val