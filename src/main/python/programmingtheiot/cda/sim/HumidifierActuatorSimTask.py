#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst

class HumidifierActuatorSimTask(BaseActuatorSimTask):
	"""
	This is a simple wrapper for an Actuator abstraction - it provides
	a container for the actuator's state, value, name, and status. A
	command variable is also provided to instruct the actuator to
	perform a specific function (in addition to setting a new value
	via the 'val' parameter.
	
	"""

	def __init__(self):
		super(
			HumidifierActuatorSimTask, self).__init__(
				name = ConfigConst.HUMIDIFIER_ACTUATOR_NAME,
				typeID = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE,
				simpleName = "HUMIDIFIER")
	
	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		
		msg = "Humidifier ON"
		
		logging.info("Simulating %s actuator ON: %s", self.name, msg)
	
		return 0
	
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		
		msg = "Humidifier OFF"
		
		logging.info("Simulating %s actuator OFF: %s", self.name, msg)
				
		return 0