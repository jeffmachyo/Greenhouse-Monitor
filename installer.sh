#!/bin/bash


# List of steps that will be carried out by the Jenkins server on the target Raspberry Pi. The idea is 
# to conduct all the tests from the /tmp folder and then once the tests are complete, create a Docker image
# that can be shipped and deploy it on the Raspberry Pi.
scp -i /var/lib/jenkins/.ssh/jeffs_pi -r /var/lib/jenkins/workspace/Greenhouse-Monitor pi@10.42.0.84:/tmp

ssh -i /var/lib/jenkins/.ssh/jeffs_pi pi@10.42.0.84 '

PYTHONPATH="/tmp/Greenhouse-Monitor/src/main/python:/tmp/Greenhouse-Monitor/src/test/python:$PYTHONPATH"
export PYTHONPATH
python3 /tmp/Greenhouse-Monitor/src/test/python/programmingtheiot/part01/unit/system/SystemCpuUtilTaskTest.py
python3 /tmp/Greenhouse-Monitor/src/test/python/programmingtheiot/part01/unit/system/SystemMemUtilTaskTest.py
python3 /tmp/Greenhouse-Monitor/src/test/python/programmingtheiot/part01/unit/common/ConfigUtilTest.py
python3 /tmp/Greenhouse-Monitor/src/test/python/programmingtheiot/part01/integration/system/SystemPerformanceManagerTest.py
python3 /tmp/Greenhouse-Monitor/src/test/python/programmingtheiot/part01/integration/app/ConstrainedDeviceAppTest.py



'

