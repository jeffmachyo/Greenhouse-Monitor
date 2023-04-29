
import logging
import unittest

import time

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData 
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData 
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientControlPacketTest(unittest.TestCase):
	NS_IN_MILLIS = 1000000
	

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Executing the MqttClientControlPacketTest class...")
		
		self.cfg = ConfigUtil()
		
		# NOTE: Be sure to use a DIFFERENT clientID than that which is used
		# for your CDA when running separately from this test
		# 
		# The clientID shown below is an example only - please use your own
		# unique value for this test
		self.mcc = MqttClientConnector(clientID = "MqttClientControlPacketTest")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	# @unittest.skip("Ignore for now.")
	def testConnectAndDisconnect(self):
		startTime = time.time_ns()
		
		self.assertTrue(self.mcc.connectClient())
		time.sleep(0.5)
		self.assertTrue(self.mcc.disconnectClient())
		
		endTime = time.time_ns()
		elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
		
		logging.info("Connect and Disconnect: " + str(elapsedMillis) + " ms")
		
    
	# @unittest.skip("Ignore for now.")
	def testServerPing(self):
		
		self.mcc.connectClient()
		time.sleep(65)
		self.assertTrue(self.mcc.pingSent)
		self.assertTrue(self.mcc.pingReceived)
	
	# @unittest.skip("Ignore for now")
	def testPubSub(self):
		
		
		qos = 2
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos = qos)
		time.sleep(5)
		
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg = "TEST1: This is the CDA message payload.", qos = 1)
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg = "TEST2: This is the CDA message payload.", qos = qos)
		time.sleep(5)
		
		self.mcc.unsubscribeFromTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
		time.sleep(5)
		
		time.sleep(delay)
		
		self.mcc.disconnectClient()

if __name__ == "__main__":
	unittest.main()