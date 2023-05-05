#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.IotDataContext import IotDataContext
from programmingtheiot.common.ConfigUtil import ConfigUtil

class MediaData(IotDataContext):
	"""
	Shell representation of class for student implementation.
	
	"""
		
	def __init__(self, typeCategoryID: int=ConfigConst.MEDIA_DEVICE_TYPE, typeID: int = ConfigConst.MEDIA_DEVICE_TYPE, name: str = ConfigConst.NOT_SET, d = None):
		super(MediaData, self).__init__(name = name, typeID = typeID, d = d)
		
		self.actionID = ConfigConst.DEFAULT_ACTION_ID
		self.dataURI = ConfigConst.NOT_SET
		self.encodingName = ConfigConst.NOT_SET
		self.message = ConfigConst.NOT_SET
		self.rawData = ""
		self.seqNo = ConfigConst.INITIAL_SEQUENCE_NUMBER
		self.seqNoTotal = -1
		self.useSeqNo = False

	def getActionID(self)-> int:
		return self.actionID
	
	def getDataURI(self)-> str:
		return self.dataURI
	
	def getEncodingName(self)-> str:
		return self.encodingName
	
	def getMessage(self)-> str:
		return self.message
	
	def getRawData(self)-> str:
		return self.rawData
	
	def getSequenceNumber(self)-> int:
		return self.seqNo
	
	def getSequenceNumberTotal(self)-> int:
		return self.seqNoTotal
	

	def setActionID(self,val):
		self.updateTimeStamp()

		if val:
			self.actionID = val

	def setDataURI(self,val:str):
		self.updateTimeStamp()

		if val:
			self.dataURI = val

	def setEncodingName(self,val:str):
		self.updateTimeStamp()

		if val:
			self.encodingName = val

	def setMessage(self,val: str):

		if val:
			self.updateTimeStamp()
			self.message = val

	def setRawData(self,val:str):
		"""
		Sets the value of RawData based on a string input
		
		@param str val: This is the value that will be set
		"""
		if val:
			self.updateTimeStamp()
			self.rawData = val

	def setSequenceNumber(self, val:int):
		self.updateTimeStamp()
		self.seqNo = val

	def setSequenceNumberTotal(self, val:int):
		self.updateTimeStamp()
		self.seqNoTotal = val

	def setUseSequenceNumber(self,enable:bool):
		"""
		Sets the value of useSeqNo based on a boolean input
		
		@param bool enable: This is the value that will be set
		"""
		self.updateTimeStamp()
		self.useSeqNo = enable

	def useSequenceNumber(self) ->bool:
		return self.useSeqNo

	def __str__(self):
		s = IotDataContext.__str__(self) + ',{}={},{}={},{}={},{}={},{}={},{}={},{}={},{}={}'
		return s.format(ConfigConst.ACTION_ID_PROP,self.actionID,ConfigConst.DATA_URI_PROP,self.dataURI,ConfigConst.MESSAGE_PROP,self.message,ConfigConst.ENCODING_NAME_PROP,self.encodingName,ConfigConst.RAW_DATA_PROP,len(self.rawData),ConfigConst.SEQUENCE_NUMBER_PROP,self.seqNo,ConfigConst.SEQUENCE_NUMBER_TOTAL_PROP,self.seqNoTotal,ConfigConst.USE_SEQUENCE_NUMBER_PROP,self.useSeqNo)
	
	def _handleUpdateData(self,data):
		
		if data and isinstance(data,MediaData):
			self.setActionID(data.getActionID())
			self.setDataURI(data.getDataURI())
			self.setMessage(data.getMessage())
			self.setEncodingName(data.getEncodingName())
			self.setRawData(data.getRawData())
			self.setSequenceNumber(data.getSequenceNumber())
			self.setSequenceNumberTotal(data.getSequenceNumberTotal())
			self.setUseSequenceNumber(data.useSequenceNumber())

		
			
			