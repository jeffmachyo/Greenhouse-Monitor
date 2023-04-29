import logging
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.DataUtil import DataUtil


class HandleActuatorEvent():
	"""
	Standard resource that will handle an incoming actuation response.
	
	"""
	def __init__(self, \
			listener: IDataMessageListener = None, \
			resource: ResourceNameEnum = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, \
			requests = None):
		
		self.listener = listener
		self.resource = resource
		self.observeRequests = requests
		
		if not self.resource:
			self.resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
			
	def handleActuatorResponse(self, response):
		"""
		Validates the response, converts response to ActuatorData object
		and then sends it down to the listener for appropriate
		handling.
		@param JSON object
		"""
		if response:
			jsonData = response.payload
			
			self.observeRequests[self.resource] = response
			
			logging.info("Received actuator command response to resource %s: %s", str(self.resource), jsonData)
			
			if self.listener:
				try:
					data = DataUtil().jsonToActuatorData(jsonData = jsonData)
					self.listener.handleActuatorCommandMessage(data = data)
				except:
					logging.warning("Failed to decode actuator data. Ignoring: %s", jsonData)