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
from datetime import datetime

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.RedisPersistenceAdapter import RedisPersistenceAdapter

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask import TemperatureSensorEmulatorTask

class PersistenceClientAdapterTest(unittest.TestCase):
    """
    This test case class contains integration tests for
	RedisPersistenceAdapter.

    Will use the SenseHAT emulator to test the data storing 
    for now
	
    """
    @classmethod
    def setUpClass(self):                                  
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.INFO)
        logging.info("Testing RedisPersistenceAdapter class...")

        self.clientAdapter = RedisPersistenceAdapter()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConnectClient(self):
        self.clientAdapter.connectClient()
        sleep(5)

    def testStoreSensorData(self):
        self.tEmuTask = TemperatureSensorEmulatorTask()
        resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
        
        i=0
        while (i<3):
            sd1 = self.tEmuTask.generateTelemetry()
            res = self.clientAdapter.storeData(resource,sd1)
            sleep(5)
            i+=1

        if res:
            
            current_date = datetime.now().isoformat()
            day = current_date.replace("-","T").split("T")
            self.du = DataUtil(True)

            j=1

            while (j<4):
                try:
                    topic = resource.value+'/'+str(day[2])+'/'+str(j)
                    json_obj = self.clientAdapter.dbClient.get(topic).decode('utf-8')

            
                    output_obj = self.du.jsonToSensorData(json_obj)
                    self.assertEqual(output_obj.getTypeID(), ConfigConst.TEMP_SENSOR_TYPE)
                    logging.info("Topic: "+topic)
                    logging.info("Sensor Data from database: \n"+str(json_obj))
                    

                except Exception as e:
                    logging.info("No entry of this type in database")
                j+=1
                sleep(1)
    
        sleep(5)

    def testClientDisconnect(self):
        disconnectTestPassed = self.clientAdapter.disconnectClient()
        self.assertTrue(disconnectTestPassed)

if __name__ == "__main__":
    unittest.main()
