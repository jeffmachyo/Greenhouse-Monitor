#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# 

import logging
import psutil

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
import programmingtheiot.common.ConfigConst as ConfigConst

class SystemCpuUtilTask(BaseSystemUtilTask):
	"""
	This class is used to conduct the function of system monitoring and therefore obtaining current system 
	parameters. In this case, the CPU percentage is the parameter being monitored and this is facilitated 
	by the psutil library.
	
	"""
	def __init__(self):
		super(SystemCpuUtilTask, self).__init__(name = ConfigConst.CPU_UTIL_NAME, typeID = ConfigConst.CPU_UTIL_TYPE)
	
	def getTelemetryValue(self) -> float:
		return psutil.cpu_percent()
	
		