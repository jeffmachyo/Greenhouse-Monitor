#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# 
#

import logging
import psutil

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
import programmingtheiot.common.ConfigConst as ConfigConst

class SystemMemUtilTask(BaseSystemUtilTask):
	"""
	This class is used to conduct the function of system monitoring and therefore obtaining current system 
	parameters. In this case, the amount of RAM available is the parameter being monitored and this is facilitated 
	by the psutil library.
	
	"""
	def __init__(self):
		super(SystemMemUtilTask, self).__init__(name = ConfigConst.MEM_UTIL_NAME, typeID = ConfigConst.MEM_UTIL_TYPE)
		
	def getTelemetryValue(self) -> float:
		return psutil.virtual_memory().percent

	
		