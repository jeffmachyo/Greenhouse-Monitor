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
#     """


ssh -i /var/lib/jenkins/.ssh/jeffs_pi pi@10.42.0.84 '

python3 /home/pi/Documents/TELE6530/cda-lab-modules-jeffmachyo/src/test/python/programmingtheiot/part01/integration/system/SystemPerformanceManagerTest.py

'

