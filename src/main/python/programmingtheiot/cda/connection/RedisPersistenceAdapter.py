#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# 
#

import logging
import redis
import re

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil

import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query


class RedisPersistenceAdapter(object):
    """
    This class will be used to facilitate connection to the Redis database to facilitate storage and retrieval of system, sensor and actuator data.

    """

    def __init__(self):
        logging.info("RedisPersistenceAdapter instantiated.")
        configUtil=ConfigUtil()
        self.host = configUtil.getProperty(section = ConfigConst.DATA_GATEWAY_SERVICE, key = ConfigConst.HOST_KEY, defaultVal = ConfigConst.DEFAULT_HOST)
        self.port = configUtil.getInteger(section = ConfigConst.DATA_GATEWAY_SERVICE, key = ConfigConst.PORT_KEY, defaultVal = ConfigConst.DEFAULT_DATA_PORT)
        self.connectStatus = False
        self.dbClient = redis.Redis(host=self.host, port=self.port, db=0,decode_responses=False)
        self.connectStatus = self.connectClient()
        self.index = 1
        
        

        if (self.connectStatus):
            logging.info("Redis connect successful.")
        else:
            logging.warning("Redis connection was not successful.")

    def connectClient(self) -> bool:
        """
		Attempts to start the Redis client
		
		@return boolean This denotes the success of the operation.
		"""
        try:
            self.dbClient.ping()
            logging.debug("Redis CheckConnectedStatus passed.")
        except(redis.exceptions.ConnectionError):
            logging.debug("Redis CheckConnectedStatus failed.")
            return False
        return True


    def disconnectClient(self) -> bool:
        """
		Attempts to stop the Redis client
		
		@return boolean This denotes the success of the operation.
		"""
        if (self.connectStatus):
            logging.info("Disconnecting from Redis")
            self.dbClient.connection_pool.disconnect()
            logging.info("Disconnected from Redis")
            self.connectStatus = False

           
        else:
            logging.info("Redis is already disconnected.")
            
        return True 

    def storeData(self, resource: ResourceNameEnum, data: SensorData) -> bool:
        """
		Attempts to store data in the Redis database. Throws an exception if the 
        operation is unsuccessful
		
		@param resource This is the reference topic used to store the data. Topic
                structure is of ResourceNameEnum type to maintain uniformity with
                the GDA.
		@param data This is the SensorData that is required to be stored.
		@return boolean This denotes the success or failure of the operation.
		"""
        if (resource and data):
            self.du = DataUtil(True)
            
            try:
                json_obj = self.du.sensorDataToJson(data)
                day = data.getTimeStamp().replace("-","T").split("T")
                topic = resource.value+'/'+str(day[2])+'/'+str(self.index)
                
                self.dbClient.set(topic,json_obj)
                
                logging.info("Data stored in database successfuly: "+topic)
                logging.debug(data)
                self.index+=1
             
                return True
            except(redis.exceptions.ConnectionError):
                logging.info("Data storage unsuccessful")
                return False

        logging.info("Storage unsuccessful: Resource name or data is null")
       
        return False
