#!/bin/bash
# cd ./Version_1
# rm -rf out/build CMakelists.txt
# cmake -S . -B out/build
# make -C out/build



# sh """
#     #!/bin/bash
#     sudo ssh -i /path/path/keyname.pem username@serverip << EOF
#     sudo bash /opt/filename.sh
#     exit 0
#     << EOF
# python3 /home/pi/Documents/TELE6530/cda-lab-modules-jeffmachyo/src/test/python/programmingtheiot/part03/integration/connection/MqttClientConnectorTest.py
#     """
scp -i /var/lib/jenkins/.ssh/jeffs_pi -r /var/lib/jenkins/workspace/Greenhouse-Monitor pi@10.42.0.84:/tmp

ssh -i /var/lib/jenkins/.ssh/jeffs_pi pi@10.42.0.84 '
df -h

PYTHONPATH="/home/pi/Documents/TELE6530/cda-lab-modules-jeffmachyo/src/main/python:/home/pi/Documents/TELE6530/cda-lab-modules-jeffmachyo/src/test/python:$PYTHONPATH"
export PYTHONPATH
python3 /home/pi/Documents/TELE6530/cda-lab-modules-jeffmachyo/src/test/python/programmingtheiot/part01/unit/system/SystemCpuUtilTaskTest.py

python3 /home/pi/Documents/TELE6530/cda-lab-modules-jeffmachyo/src/test/python/programmingtheiot/part01/unit/common/ConfigUtilTest.py

'

