#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from threading import Thread

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.MediaData import MediaData
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.stream.IDataStreamTask import IDataStreamTask

from contextlib import redirect_stderr

class BaseDataStreamTask(IDataStreamTask):
	"""
	Shell representation of class for student implementation.
	
	"""
		
	def __init__(self,streamMediaTypeID = ConfigConst.DEFAULT_MEDIA_TYPE,staticMediaTypeID: int = ConfigConst.DEFAULT_MEDIA_TYPE, streamMediaName: str = ConfigConst.NOT_SET,staticMediaName:str = ConfigConst.NOT_SET):
		
		self.createMediaDataClone = True

		self.typeCategoryID = ConfigConst.MEDIA_TYPE_CATEGORY
		self.staticMediaName = staticMediaName
		self.staticMediaTypeID = staticMediaTypeID

		self.latestStaticMediaData = MediaData(name=staticMediaName,typeID=self.staticMediaTypeID)
		self.latestStaticMediaData.setTypeCategoryID(self.typeCategoryID)

		self.streamMediaName = streamMediaName
		self.streamMediaTypeID = streamMediaTypeID

		self.latestStreamMediaData = MediaData(name=self.streamMediaName,typeID=self.streamMediaTypeID)
		self.latestStreamMediaData.setTypeCategoryID(self.typeCategoryID)

		self.streamThread = None
		self.dataMsgListener = None

	def getDataMessageListener(self)->IDataMessageListener:
		return self.dataMsgListener
	
	def getLatestStaticMediaData(self)-> MediaData:
		
		if self.createMediaDataClone:
			mdCopy = MediaData()
			mdCopy.updateData(self.latestStaticMediaData)

			return mdCopy
		
		return self.latestStaticMediaData
	
	def getLatestStreamMediaData(self)-> MediaData:
		
		if self.createMediaDataClone:
			mdCopy = MediaData()
			mdCopy.updateData(self.latestStreamMediaData)

			return mdCopy
		
		return self.latestStreamMediaData
	
	def getStaticMediaName(self) -> str:

		return self.staticMediaName
	
	def getStaticMediaTypeID(self) -> str:

		return self.staticMediaTypeID 
	
	def getStreamMediaName(self) -> str:

		return self.streamMediaName
	
	def getStreamMediaTypeID(self) -> str:

		return self.streamMediaTypeID
	
	def getTypeCategoryID(self) -> str:

		return self.typeCategoryID
	
	def isStreamStarted(self) -> bool:

		return self.isStarted
	
	def setDataMessageListener(self,listener:IDataMessageListener):

		if listener:
			self.dataMsgListener = listener

	def startStream(self) -> bool:


		if not self.isStarted:
			if not self.streamThread:
				self.streamThread = Thread(target=self._startStreamLoop)

				self.streamThread.setDaemon(True)
				self.streamThread.setName(self.getStreamMediaName())

				logging.info("Created stream thread: "+ self.streamThread.getName())
			logging.info("Starting stream thread: "+ self.streamThread.getName())

			with open('CDA_BaseDataStreamTask.Log','w') as stderr, redirect_stderr(stderr):
				self.streamThread.start()
			self.isStarted = True

			logging.info("Started stream thread: "+ self.streamThread.getName())

		else:
			logging.warning("Stream thread already started. Ignoring: "+ self.streamThread.getName())

		return self.isStreamStarted()
	
	def stopStream(self) -> bool:
		pass


	def _getCurrentStaticMediaData(self) -> MediaData:


		return self.latestStaticMediaData
	
	def _getCurrentStreamMediaData(self) -> MediaData:
		
		return self.latestStreamMediaData
	
	def _startStreamLoop(self):

		pass

	def _stopStreamLoop(self):

		pass