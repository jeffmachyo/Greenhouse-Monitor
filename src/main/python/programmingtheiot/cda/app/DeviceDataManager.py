#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# 

import logging


import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.CoapServerAdapter import CoapServerAdapter
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.cda.connection.RedisPersistenceAdapter import RedisPersistenceAdapter

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

from programmingtheiot.data.DataUtil import DataUtil

class DeviceDataManager(IDataMessageListener):
	"""
	This class serves to co-ordinate the functions of various sub-classes in the system.
	
	"""
	
	def __init__(self):

		self.configs = ConfigUtil()

		self.enableSysPerformance = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_SYSTEM_PERF_KEY, False)
		self.enableActuation = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_ACTUATION_KEY, False)
		self.enableSensing = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_SENSING_KEY, False)

		self.handleTempChangeOnDevice = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
		self.triggerHvacTempFloor = self.configs.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
		self.triggerHvacTempCeiling = self.configs.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)

		self.enableLocalStorage = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_LOCAL_STORAGE_KEY, False)

		self.enableMqttClient = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_MQTT_CLIENT_KEY, False)
		self.enableCoapClient = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_COAP_CLIENT_KEY, False)
		self.clientID = '1'+(ConfigUtil().getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY))
		self.enableCoapServer = self.configs.getBoolean(ConfigConst.CONSTRAINED_DEVICE,ConfigConst.ENABLE_COAP_SERVER_KEY, False)
		

		self.systemPerformanceMgrInstance = None
		self.actuatorAdapterMgrInstance = None
		self.sensorAdapterMgrInstance = None

		self.mqttClient         = None
		self.coapClient         = None
		self.coapServer         = None
		self.redisClient        = None

		self.actuatorResponseCache = {}
		if (self.enableLocalStorage):
			self.redisClient = RedisPersistenceAdapter()

		if (self.enableSysPerformance):
			self.systemPerformanceMgrInstance = SystemPerformanceManager(listener=self)
			logging.info("Local system performance tracking enabled")
		else:
			logging.info("Local system performance tracking disabled")

		if (self.enableActuation):
			self.actuatorAdapterMgrInstance = ActuatorAdapterManager(listener=self)
			logging.info("Local actuation capabilities enabled")
		else:
			logging.info("Local actuation capabilities disabled")
		
		if (self.enableSensing):
			self.sensorAdapterMgrInstance = SensorAdapterManager(listener=self)
			logging.info("Local sensor tracking enabled")
		else:
			logging.info("Local sensor tracking disabled")

		if (self.enableMqttClient):
			self.mqttClient = MqttClientConnector(self.clientID,listener=self)
			# self.mqttClient.setDataMessageListener(self)
			logging.info("MQTT client enabled enabled")
		else:
			logging.info("MQTT client disabled")

		if (self.enableCoapServer):
			self.coapServer = CoapServerAdapter(dataMsgListener = self)
			logging.info("Local CoAP Server enabled")
		else:
			logging.info("Local CoAP server disabled")

		if (self.enableCoapClient):
			self.coapClient = CoapClientConnector(dataMsgListener = self)
			logging.info("Local CoAP Client enabled")
		else:
			logging.info("Local CoAP Client disabled")
		

	
	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Retrieves the named actuator data (response) item from the internal data cache.
		
		@param name
		@return ActuatorData
		"""
		pass
		
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Retrieves the named sensor data item from the internal data cache.
		
		@param name
		@return SensorData
		"""
		pass
	
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Retrieves the named system performance data from the internal data cache.
		
		@param name
		@return SystemPerformanceData
		"""
		pass
	
	def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
		"""
		This callback method will be invoked by the connection that's handling
		an incoming ActuatorData command message.
		
		@param data The incoming ActuatorData command message.
		@return ActuatorData instance
		"""
		logging.info("Actuator data: " + str(data))
	
		if data:
			logging.info("Processing actuator command message.")
			return self.actuatorAdapterMgrInstance.sendActuatorCommand(data)
		else:
			logging.warning("Incoming actuator command is invalid (null). Ignoring.")
			return None
	
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		"""
		This callback method will be invoked by the actuator manager that just
		processed an ActuatorData command, which creates a new ActuatorData
		instance and sets it as a response before calling this method.
		
		@param data The incoming ActuatorData response message.
		@return boolean
		"""
		if data:
			logging.debug("Incoming actuator response received (from actuator manager): " + str(data))
		
		# store the data in the cache
			self.actuatorResponseCache[data.getName()] = data
		
		# convert ActuatorData to JSON and get the msg resource
			actuatorMsg = DataUtil().actuatorDataToJson(data)
			resourceName = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
		
		# delegate to the transmit function any potential upstream comm's
			self._handleUpstreamTransmission(resource = resourceName, msg = actuatorMsg)
		
			return True
		else:
			logging.warning("Incoming actuator response is invalid (null). Ignoring.")
		
			return False
	
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		"""
		This callback method is generic and designed to handle any incoming string-based
		message, which will likely be JSON-formatted and need to be converted to the appropriate
		data type. You may not need to use this callback at all.
		
		@param data The incoming JSON message.
		@return boolean
		"""
		logging.debug("Processing DeviceDataManager incoming message: ")

		return True

	
	def handleSensorMessage(self, data: SensorData) -> bool:
		"""
		This callback method will be invoked by the sensor manager that just processed
		a new sensor reading, which creates a new SensorData instance that will be
		passed to this method.
		
		@param data The incoming SensorData message.
		@return boolean
		"""
		if data:
			logging.debug("Incoming sensor data received (from sensor manager): " + str(data))
			# if (self.redisClient is not None):
			# 	resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
			# 	res = self.redisClient.storeData(resource,data)
			
			self._handleSensorDataAnalysis(data)
			jsonData = DataUtil().sensorDataToJson(data = data)
			self._handleUpstreamTransmission(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = jsonData)

			return True
		else:
			logging.warning("Incoming sensor data is invalid (null). Ignoring.")
			return False
	
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		"""
		This callback method will be invoked by the system performance manager that just
		processed a new sensor reading, which creates a new SystemPerformanceData instance
		that will be passed to this method.
		
		@param data The incoming SystemPerformanceData message.
		@return boolean
		"""
		if data:
			logging.debug("Incoming system performance message received (from sys perf manager): " + str(data))

			jsonData = DataUtil().systemPerformanceDataToJson(data = data)
			self._handleUpstreamTransmission(resource = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, msg = jsonData)
			return True
		else:
			logging.warning("Incoming system performance data is invalid (null). Ignoring.")
			return False
	
	def setSystemPerformanceDataListener(self, listener: ISystemPerformanceDataListener = None):
		pass
			
	def setTelemetryDataListener(self, name: str = None, listener: ITelemetryDataListener = None):
		pass
			
	def startManager(self):
		logging.info("Starting DeviceDataManager...")

		if self.systemPerformanceMgrInstance:
			self.systemPerformanceMgrInstance.startManager()

		else:
			logging.info("No SystemPerformanceManager instance is available")

		if self.sensorAdapterMgrInstance:
			self.sensorAdapterMgrInstance.startManager()
		else:
			logging.info("No SensorAdapterManager instance is available")
		
		if self.redisClient:
			self.redisClient.connectClient()
		else:
			logging.info("No RedisPersistenceAdapter instance is available")

		if self.mqttClient:
			self.mqttClient.connectClient()
			
		else:
			logging.info("No MQTTClient instance is available")

		if self.coapServer:
			self.coapServer.startServer()
		else:
			logging.info("No CoAPServerAdapter instance is available")

		logging.info("Successfuly started DeviceDataManager...")
		
	def stopManager(self):
		logging.info("Stopping DeviceDataManager...")
		if self.sensorAdapterMgrInstance.isRunning:
			self.sensorAdapterMgrInstance.stopManager()

		if self.systemPerformanceMgrInstance.isRunning:
			self.systemPerformanceMgrInstance.stopManager()

		if self.mqttClient:
			self.mqttClient.unsubscribeFromTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)
			self.mqttClient.disconnectClient()

		if self.coapServer:
			self.coapServer.stopServer()

		logging.info("Successfully stopped DeviceDataManager...")
	def _handleIncomingDataAnalysis(self, msg: str):
		"""
		Call this from handleIncomeMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
		2) Convert msg: Use DataUtil to convert if appropriate.
		3) Act on msg: Determine what - if any - action is required, and execute.
		"""
		logging.debug("Handling incoming data analysis: ")
		
	def _handleSensorDataAnalysis(self, data: SensorData):
		"""
		Call this from handleSensorMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Check config: Is there a rule or flag that requires immediate processing of data?
		2) Act on data: If # 1 is true, determine what - if any - action is required, and execute.
		"""
		if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
			logging.info("Handle temp change: %s - type ID: %s", str(self.handleTempChangeOnDevice), str(data.getTypeID()))
			
			ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
			
			if data.getValue() > self.triggerHvacTempCeiling:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempCeiling)
			elif data.getValue() < self.triggerHvacTempFloor:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempFloor)
			else:
				ad.setCommand(ConfigConst.COMMAND_OFF)
				
			self.handleActuatorCommandMessage(ad)
		
	def _handleUpstreamTransmission(self, resource: ResourceNameEnum, msg: str):
		"""
		Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
		to determine if the message should be sent upstream. Steps to take:
		1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
		2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
		"""
		logging.info("Upstream transmission invoked. Checking comm's integration.")
	
		# NOTE: If using MQTT, the following will attempt to publish the message to the broker
		if self.mqttClient:
			if self.mqttClient.publishMessage(resource = resource, msg = msg):
				logging.debug("Published incoming data to resource (MQTT): %s", str(resource))
			else:
				logging.warning("Failed to publish incoming data to resource (MQTT): %s", str(resource))
		
		# NOTE: If using CoAP, the following will attempt to PUT the message to the server
		if self.coapClient:
			if self.coapClient.sendPutRequest(resource = resource, payload = msg):
				logging.debug("Posted incoming message data to resource (CoAP): %s", str(resource))
			else:
				logging.warning("Failed to post incoming message data to resource (CoAP): %s", str(resource))
