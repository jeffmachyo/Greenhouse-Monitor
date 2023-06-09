#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData

class CoapClientConnectorTest(unittest.TestCase):
	"""
	This test case class contains very basic integration tests for
	CoapClientConnector using a separately running CoAP server.
	
	It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	
	NOTE: This is different from CoapServerAdapterTest in that it depends
	upon an external CoAP server (e.g., the GDA's CoAP server).
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.INFO)
		logging.info("Testing CoapClientConnector class...")
		
		self.dataMsgListener = DefaultDataMessageListener()
		
		self.pollRate = ConfigUtil().getInteger(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.POLL_CYCLES_KEY, ConfigConst.DEFAULT_POLL_CYCLES)
		
		self.coapClient = CoapClientConnector(self.dataMsgListener)
		
	@classmethod
	def tearDownClass(self):
		pass
	
	def setUp(self):
		pass

	def tearDown(self):
		pass

	# @unittest.skip("Ignore for now.")
	def testConnectAndDiscover(self):
		"""
		Comment the annotation to test Connect and Discover
		"""
		self.coapClient.sendDiscoveryRequest(timeout = 5)
		
		sleep(5)

	# @unittest.skip("Ignore for now.")
	def testGetActuatorCommandCon(self):
		"""
		Comment the annotation to test CON GET
		"""
		logging.info("GET actuator message CON")
		self.coapClient.sendGetRequest( \
			resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, enableCON = True, timeout = 5)
		
	# @unittest.skip("Ignore for now.")
	def testGetActuatorCommandNon(self):
		"""
		Comment the annotation to test NON GET
		"""
		logging.info("GET actuator message NON")
		self.coapClient.sendGetRequest( \
			resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, enableCON = False, timeout = 5)
		
	# @unittest.skip("Ignore for now.")
	def testDeleteSensorMessageCon(self):
		"""
		Comment the annotation to test CON DELETE
		"""
		logging.info("DELETE sensor message CON: ")
		self.coapClient.sendDeleteRequest( \
			resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON = True, timeout = 5)
	
	# @unittest.skip("Ignore for now.")
	def testDeleteSensorMessageNon(self):
		"""
		Comment the annotation to test NON DELETE
		"""
		logging.info("DELETE sensor message NON: ")
		self.coapClient.sendDeleteRequest( \
			resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON = False, timeout = 5)

	# @unittest.skip("Ignore for now.")
	def testPostSensorMessageCon(self):
		"""
		Comment the annotation to test CON POST
		"""
		data = SensorData()
		jsonData = DataUtil().sensorDataToJson(data = data)
		logging.info("POST sensor message CON: "+ jsonData)
		
		self.coapClient.sendPostRequest( \
			resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON = True, payload = jsonData, timeout = 5)
	
	# @unittest.skip("Ignore for now.")
	def testPostSensorMessageNon(self):
		"""
		Comment the annotation to test NON POST
		"""
		data = SensorData()
		jsonData = DataUtil().sensorDataToJson(data = data)
		
		logging.info("POST sensor message NON: "+ jsonData)
		self.coapClient.sendPostRequest( \
			resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON = False, payload = jsonData, timeout = 5)
	
	# @unittest.skip("Ignore for now.")
	def testPutSensorMessageCon(self):
		"""
		Comment the annotation to test CON PUT
		"""
		data = SensorData()
		jsonData = DataUtil().sensorDataToJson(data = data)

		logging.info("PUT sensor message CON: "+ jsonData)
		
		self.coapClient.sendPutRequest( \
			resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON = True, payload = jsonData, timeout = 5)
	
	# @unittest.skip("Ignore for now.")
	def testPutSensorMessageNon(self):
		"""
		Comment the annotation to test NON PUT
		"""
		data = SensorData()
		jsonData = DataUtil().sensorDataToJson(data = data)
		
		logging.info("PUT sensor message NON: "+ jsonData)
		self.coapClient.sendPutRequest( \
			resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON = False, payload = jsonData, timeout = 5)

	# @unittest.skip("Ignore for now.")
	def testActuatorCommandObserve(self):
		"""
		Comment the annotation to test Observe
		"""
		self._startObserver()
		sleep(60)
		self._stopObserver()
		
	def _startObserver(self):
		self.coapClient.startObserver(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)

	def _stopObserver(self):
		self.coapClient.stopObserver(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)

if __name__ == "__main__":
	unittest.main()
	