#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import os

# disable FFREPORT via 'export FFREPORT='

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = "rtsp_transport;udp"
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS'] = str(2**64)


from time import sleep
from datetime import datetime, timezone

import logging
import imutils
import cv2 as cv
import programmingtheiot.common.ConfigConst as ConfigConst

from contextlib import redirect_stderr

from programmingtheiot.data.ImageDataContext import ImageDataContext
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataManager import IDataManager
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.stream.BaseDataStreamTask import BaseDataStreamTask

class CameraStreamMonitorTask(BaseDataStreamTask):
	"""
	Shell representation of class for student implementation.
	
	"""
		
	def __init__(self, configSectionKey = ConfigConst.CONSTRAINED_DEVICE):

		super(CameraStreamMonitorTask,self).__init__(streamMediaTypeID = ConfigConst.CAMERA_STREAM_SENSOR_TYPE,staticMediaTypeID = ConfigConst.CAMERA_MOTION_SENSOR_TYPE)


		logging.info("Initializing camera motion detector stream...")

		self.configSectionKey = configSectionKey

		if not self.configSectionKey:
			self.configSectionKey = ConfigConst.CONSTRAINED_DEVICE

		self.totalFrameCount = 0
		self.motionFrameCount = 0
		self.motionFrameActionCount = 0

		self.isFirstPass=True

		self.enabledImageSnapshot = True
		self.enableMotionDetection = True
		self.enableVideoRecording = False
		self.enableImageStorage = True
		


	def setDataMessageListener(self,listener:IDataMessageListener):

		if listener:
			self.dataMsgListener = listener

	def _startStreamLoop(self):
		self._initVideoStream()

		logging.info("Starting video capture stream loop...")

		retryCycles = 5

		while not self.isStopRequested:
			isActive = self.vs.isOpened()

			if isActive:
				try:
					success, rawframe = self.vs.read()
					
					if success:
						resizedFrame = imutils.resize(rawframe,width=500)
						grayscaleFrame = cv.cvtColor(rawframe,cv.COLOR_BGR2GRAY)

						self._handleMotionDetectionCheck(rawframe,resizedFrame, grayscaleFrame)

						sleep(self.loopWaitVal)

				except:
					isActive=False
					logging.exception('Exception handling motion detection. Will pause re-try: '+str(retryCycles)+ ' seconds')

			else:
				logging.warning('Video feed is no longer open. Waiting then retrying: '+str(retryCycles)+' seconds')

				self._releaseVideoStream()
				sleep(retryCycles)
				self._initVideoStream(True)

			logging.info("Video stream capture loop cancelled - stop requested")
