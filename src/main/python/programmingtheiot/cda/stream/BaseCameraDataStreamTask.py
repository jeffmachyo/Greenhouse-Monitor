#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import os

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

from programmingtheiot.cda.stream.BaseDataStreamTask import BaseDataStreamTask

class CameraStreamMonitorTask(BaseDataStreamTask):
	"""
	Shell representation of class for student implementation.
	
	"""
		
	def __init__(self, staticMediaTypeID = ConfigConst.CAMERA_MOTION_SENSOR_TYPE):

		super(CameraStreamMonitorTask,self).__init__(streamMediaTypeID = ConfigConst.CAMERA_MOTION_SENSOR_TYPE,staticMediaTypeID = staticMediaTypeID)

		logging.info("Initializing camera stream monitoring task...")

		self.totalFrameCount = 0
		self.motionFrameCount = 0
		self.motionFrameActionCount = 0