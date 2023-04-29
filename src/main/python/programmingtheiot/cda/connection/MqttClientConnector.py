#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is used as a wrapper for the paho MQTT library
#

import logging
import paho.mqtt.client as mqttClient
import ssl

from programmingtheiot.data.DataUtil import DataUtil
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient
import time

class MqttClientConnector(IPubSubClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, clientID: str = None,listener: IDataMessageListener=None):
		"""
		Default constructor. This will set remote broker information and client connection
		information based on the default configuration file contents.
		
		@param clientID Defaults to None. Can be set by caller. If this is used, it's
		critically important that a unique, non-conflicting name be used so to avoid
		causing the MQTT broker to disconnect any client using the same name. With
		auto-reconnect enabled, this can cause a race condition where each client with
		the same clientID continuously attempts to re-connect, causing the broker to
		disconnect the previous instance.
		"""
		self.config = ConfigUtil()
		self.dataMsgListener = listener
		
		self.host = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
		
		self.port = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
		
		self.keepAlive = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.defaultQos = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)

		self.enableEncryption = self.config.getBoolean(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.ENABLE_CRYPT_KEY)
		self.enableAuth = self.config.getBoolean(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.ENABLE_AUTH_KEY)

		self.enableCleanSession = self.config.getBoolean(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.ENABLE_CLEAN_SESSION_KEY)

		# self.mqttClient.subscribeToTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, callback = None, qos = ConfigConst.DEFAULT_QOS)
		
		self.mqttClient = None
		self.clientID = clientID
		self.buf = None
		self.pingSent = False
		self.pingReceived = False

		if not self.clientID:
			self.clientID = self.config.getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY)
		
		if (self.enableEncryption):
			self.port = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.SECURE_PORT_KEY, ConfigConst.DEFAULT_MQTT_SECURE_PORT)

		logging.info('\tMQTT Client ID:   ' + self.clientID)
		logging.info('\tMQTT Broker Host: ' + self.host)
		logging.info('\tMQTT Broker Port: ' + str(self.port))
		logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))

	def connectClient(self) -> bool:
		"""
		Used to facilitate the connection of the client via MQTT as well as define 
		other parameters such as callbacks
		
		@return bool Returns true if the client connection is successful.
		
		"""
		if not self.mqttClient:
		
			self.mqttClient = mqttClient.Client(client_id = self.clientID, clean_session = self.enableCleanSession)

			try:
				if (self.enableEncryption):
					logging.info("Enabling TLS encryption...")
					
					if (self.enableAuth):
						self.caCertFile = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.CERT_FILE_KEY)
						self.clientCertFile = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.CRED_FILE_KEY)
						self.clientCertKey = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.CRED_KEY_KEY)
					
						self.mqttClient.tls_set(ca_certs=self.caCertFile,certfile=self.clientCertFile,keyfile=self.clientCertKey,tls_version = ssl.PROTOCOL_TLSv1_2)
						# self.mqttClient.tls_set(ca_certs='/home/jeff/Documents/TELE6530/mosquitto/client_certs/ca.crt',certfile='/home/jeff/Documents/TELE6530/mosquitto/client_certs/client.crt',keyfile='/home/jeff/Documents/TELE6530/mosquitto/client_certs/client.key',tls_version = ssl.PROTOCOL_TLSv1_2)
					else:

						self.mqttClient.tls_set(self.caCertFile,tls_version = ssl.PROTOCOL_TLSv1_2)
					
			except Exception as e:
				logging.warning("Failed to enable TLS encryption. Using unencrypted connection.")
				logging.warning(e)
			
			self.mqttClient.on_connect = self.onConnect
			self.mqttClient.on_disconnect = self.onDisconnect
			self.mqttClient.on_message = self.onMessage
			self.mqttClient.on_publish = self.onPublish
			self.mqttClient.on_subscribe = self.onSubscribe
			self.mqttClient.on_log = self.onLog

		if not self.mqttClient.is_connected():
			logging.info('MQTT client connecting to broker at host: ' + self.host + ' ID: '+self.clientID)
			self.mqttClient.connect(self.host, self.port, self.keepAlive)
			self.mqttClient.loop_start()
			
			time.sleep(0.5)
			return True
		else:
			logging.warning('MQTT client is already connected. Ignoring connect request.')
			
			return False
	def disconnectClient(self) -> bool:
		"""
		Used to facilitate the disconnection of the MQTT client
		
		@return bool Returns true if the client disconnection is successful.
		
		"""
		if self.mqttClient.is_connected():
			logging.info('Disconnecting MQTT client from broker: ' + self.host)
			self.mqttClient.loop_stop()
			self.mqttClient.disconnect()
		
			return True
		else:
			logging.warning('MQTT client already disconnected. Ignoring.')
			
			return False


		
	def onConnect(self, client, userdata, flags, rc):
		"""
		This is a callback that is called once a successful MQTT connection is made .
		In this case it logs a connect successful message.
		
		"""
		logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))
	
		# NOTE: Be sure to set `self.defaultQos` during instantiation!
		self.mqttClient.subscribe(topic = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, qos = self.defaultQos)
		
		self.mqttClient.message_callback_add(sub = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, callback = self.onActuatorCommandMessage)
		
	def onDisconnect(self, client, userdata, rc):
		"""
		This is a callback that is called once a successful MQTT disconnection is occurs.
		In this case it logs a disconnecton message.
		
		"""
		logging.info('MQTT client disconnected from broker: ' + str(client))
		
	def onMessage(self, client, userdata, msg):
		"""
		This is a callback that is called once a new MQTT message arrives. In this case,
		it logs that a message was received. 
		
		"""
		payload = msg.payload
	
		if (payload):
			logging.info('MQTT message received with payload: ' + str(payload.decode("utf-8")))
		else:
			logging.info('MQTT message received with no payload: ' + str(msg))
			
	def onPublish(self, client, userdata, mid):
		"""
		This is a callback that is called once a new MQTT message is published. In this case,
		it logs that a message was published. 
		
		"""
		# logging.debug('MQTT message published: ' + str(client))
	
	def onSubscribe(self, client, userdata, mid, granted_qos):
		"""
		This is a callback that is called once a new MQTT message is published. In this case,
		it logs that a message was published. 
		
		"""
		logging.info('MQTT client subscribed: ' + str(client))

	def onLog(self,client,userdata,level,buf):
		"""
		This is a callback that is called once a new MQTT log message is published. In this case,
		it looks for a PINGREQ and a PINGRESP in the logs and sets a @self.pingSent and @self.pingResponse
		variables to True 
		@param client The client reference context.
		@param userdata The user reference context.
		@param level The debug level to filter
		@param buf The buffer in which the debug messages will be stored
		
		"""
		self.buf = buf
		request = 'PINGREQ'
		response = 'PINGRESP'

		if (request in buf):
			self.pingSent = True
		elif (response in buf):
			self.pingReceived = True
	
	def onActuatorCommandMessage(self, client, userdata, msg):
		"""
		This callback is defined as a convenience, but does not
		need to be used and can be ignored.
		
		It's simply an example for how you can create your own
		custom callback for incoming messages from a specific
		topic subscription (such as for actuator commands).
		
		@param client The client reference context.
		@param userdata The user reference context.
		@param msg The message context, including the embedded payload.
		"""
		logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
	
		if self.dataMsgListener:
			try:
				# assumes all data is encoded using UTF-8 (between GDA and CDA)
				actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode('utf-8'))
				
				self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
			except:
				logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")
	
	def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS):
		"""
		This implements the MQTT publish message scheme. 
		@param resource The resource topic to be published to.
		@param msg the message to be published.
		@param qos the Quality of Service to be used.
		@return bool True if the publish was a success
		"""
		# check validity of resource (topic)
		if not resource:
			logging.warning('No topic specified. Cannot publish message.')
			return False
		
		# check validity of message
		if not msg:
			logging.warning('No message specified. Cannot publish message to topic: ' + resource.value)
			return False
		
		# check validity of QoS - set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
		
		# publish message, and wait for publish to complete before returning
		msgInfo = self.mqttClient.publish(topic = resource.value, payload = msg, qos = qos)
		# msgInfo.wait_for_publish()
		
		return True
	
	def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS):
		"""
		This implements the MQTT subscribe to topic scheme. 
		@param resource The resource topic to be subscribed to.
		@param callback the callback to be invoked after the subscribe is called.
		@param qos the Quality of Service to be used.
		@return bool True if the subscribe was a success
		"""
		# check validity of resource (topic)
		if not resource:
			logging.warning('No topic specified. Cannot subscribe.')
			return False
		
		# check validity of QoS - set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
		
		# subscribe to topic
		logging.info("Subscribed to topic: "+resource.value)
		self.mqttClient.subscribe(resource.value, qos)
		
		return True
	
	def unsubscribeFromTopic(self, resource: ResourceNameEnum = None):
		"""
		This implements the MQTT unsubscribe to topic scheme. 
		@param resource The resource topic to be subscribed to.
		@return bool True if the unsubscribe was a success
		"""
		# check validity of resource (topic)
		if not resource:
			logging.warning('No topic specified. Cannot unsubscribe.')
			return False
		
		logging.info("Unsubscribed from topic: "+resource.value)
		self.mqttClient.unsubscribe(resource.value)
		
		return True
		
	
	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		if listener:
			self.dataMsgListener = listener
