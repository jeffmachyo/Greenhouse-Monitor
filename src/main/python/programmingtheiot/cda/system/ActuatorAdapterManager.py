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

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self,listener:IDataMessageListener = None):
		configUtil=ConfigUtil()

		self.useSimulatorConfig = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_SIMULATOR_KEY, False)
		self.useEmulatorConfig = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_EMULATOR_KEY, False)
		self.useSenseHatConfig = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_SENSE_HAT_KEY, False)

		self.locationID = configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)

		self.deviceID = configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_ID_KEY, defaultVal = ConfigConst.NOT_SET)

		self.iDataMessageListener = listener

		self.hvacAdapter = None
		self.humidifierAdapter = None
		self.ledDisplayAdapter = None

		if self.useEmulatorConfig and self.useSimulatorConfig and self.useSenseHatConfig:
			logging.warning("Emulator, Simulator and Physical SenseHAT use enabled. Need to pick one...")
		
		elif ((self.useEmulatorConfig or self.useSenseHatConfig) and not self.useSimulatorConfig):
			if ((self.useEmulatorConfig and not self.useSenseHatConfig) or (not self.useEmulatorConfig and self.useSenseHatConfig)):
				
				humidifierModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidiferEmulatorTask')
				humidifierEmulatorModule = getattr(humidifierModule, 'HumidifierEmulatorTask')
				self.humidifierAdapter = humidifierEmulatorModule()
				
				# create the HVAC actuator emulator
				hvacModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
				hvacEmulatorModule = getattr(hvacModule, 'HvacEmulatorTask')
				self.hvacAdapter = hvacEmulatorModule()
				
				# create the LED display actuator emulator
				ledDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
				ledDisplayEmulatorModule = getattr(ledDisplayModule, 'LedDisplayEmulatorTask')
				self.ledDisplayAdapter = ledDisplayEmulatorModule()

			else:
				logging.warning("Both Physical SenseHAT and Emulator enabled. Need to pick one..")

		elif (self.useSimulatorConfig and not self.useEmulatorConfig):
			logging.info("Simulator actuator use enabled...")
			self.hvacAdapter = HvacActuatorSimTask()
			self.humidifierAdapter = HumidifierActuatorSimTask()

		else:
			logging.warning("No simulator or emulator enabled...")


	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		response = None
		if data and isinstance(data,ActuatorData):
			if not data.isResponseFlagEnabled():
				if data.getLocationID() == self.locationID:
					logging.info("Actuator command received for location ID "+ data.getLocationID()+". Processing..." )
					deviceType = data.getTypeID()

					if deviceType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierAdapter:
						response = self.humidifierAdapter.updateActuator(data)
					elif deviceType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacAdapter:
						response = self.hvacAdapter.updateActuator(data)
					elif deviceType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayAdapter:
						response = self.ledDisplayAdapter.updateActuator(data)					
					else:
						logging.warning("No valid actuator type. Ignoring actuation for type: "+ str(data.getTypeID()))

				else:
					logging.warning("The location id specified: "+str(data.getLocationID())+" is not in the configs")
			else:
				logging.warning("The ActuataData response flag is set to: "+str(data.isResponseFlagEnabled()))
		else:
			logging.warning("Actuator input data is not valid.")
		
		return response

	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		self.iDataMessageListener = IDataMessageListener
		return True

	

