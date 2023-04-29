#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst

class HvacActuatorSimTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(HvacActuatorSimTask, self).__init__(name = ConfigConst.HVAC_ACTUATOR_NAME, typeID = ConfigConst.HVAC_ACTUATOR_TYPE, simpleName = "HVAC")
		
	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		
		msg = "HVAC ON"
		
		logging.info("Simulating %s actuator ON: %s", self.name, msg)
	
		return 0
	
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		
		msg = "HVAC OFF"
		
		logging.info("Simulating %s actuator OFF: %s", self.name, msg)
				
		return 0
		