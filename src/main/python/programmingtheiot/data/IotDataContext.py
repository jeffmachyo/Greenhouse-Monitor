#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData
from programmingtheiot.common.ConfigUtil import ConfigUtil

class IotDataContext(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
		
	def __init__(self, typeCategoryID: int=ConfigConst.DEFAULT_TYPE_CATEGORY_ID, typeID: int = ConfigConst.DEFAULT_TYPE_ID, name: str = ConfigConst.NOT_SET, d = None):
		super(IotDataContext, self).__init__(name = name, typeID = typeID, d = d)
		# self.value = ConfigConst.DEFAULT_VAL
		if (d):
			try:
				self.deviceID = d[ConfigConst.DEVICE_ID_PROP]
				self.typeCategoryID = d[ConfigConst.TYPE_CATEGORY_ID_PROP]

			except:
				pass
		else:
			self.typeCategoryID = typeCategoryID
			self.deviceID = ConfigUtil.getProperty(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.DEVICE_ID_PROP)

	def getDeviceID(self):
		return self.deviceID
	
	def getTypeCategoryID(self):
		return self.typeCategoryID
	

	def setDeviceID(self,idStr:str=None):
		if (idStr and len(idStr)>0):
			self.deviceID = idStr
		    
	# def getSensorType(self) -> int:
	# 	"""
	# 	Returns the sensor type to the caller.
		
	# 	@return int
	# 	"""
	# 	return self.sensorType
	
	# def getValue(self) -> float:
	# 	return self.value
	
	# def setValue(self, newVal: float):
	# 	self.updateTimeStamp()
	# 	self.value=newVal
		
	# def _handleUpdateData(self, data):
	# 	if data and isinstance(data,SensorData):
	# 		self.value=data.getValue()
