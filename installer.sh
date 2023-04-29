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

ls -al

'

