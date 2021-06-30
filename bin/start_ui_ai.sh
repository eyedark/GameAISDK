#!/bin/sh

PWD=`pwd`
export PATH=$PATH:$PWD/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/lib/
export AI_SDK_PROJECT_FILE_PATH=${1}/${2}.prj
export AI_SDK_PROJECT_FULL_PATH=${1}
echo ${AI_SDK_PROJECT_FILE_PATH}


echo "Run UI+AI Service"


#Start MC process
python3 manage_center.py --runType=UI+AI >/dev/null 2>&1 &
sleep 1

#Check MC process
ps -fe | grep 'python3 manage_center.py' | grep -v grep
if [ $? -ne 0 ]; then
	echo "No MC process"
	exit 4
fi


#Start IO process
python3 io_service.py >/dev/null 2>&1 &
sleep 1

#Check IO process
ps -fe | grep 'python3 io_service.py' | grep -v grep
if [ $? -ne 0 ]; then
	echo "No IO process"
	exit 5
fi


#Start Agent process
python3 agentai.py --cfgpath ${1}/${2}.prj >/dev/null 2>&1 &
sleep 10

#Check Agent process
ps -fe | grep 'python3 agentai.py ' | grep -v grep
if [ $? -ne 0 ]; then
	echo "No Agent process"
	exit 1
fi


#Start UIRecognize process
./UIRecognize mode SDKTool cfgpath ${1} >/dev/null 2>&1 &
sleep 1

#Check UIRecognize process
ps -fe | grep 'UIRecognize' | grep -v grep
if [ $? -ne 0 ]; then
	echo "No UIRecognize process"
	exit 2
fi


#Start GameReg process
./GameReg mode SDKTool cfgpath ${1}/cfg/task/gameReg/Task.json >/dev/null 2>&1 &
sleep 1

#Check GameReg process
ps -fe | grep 'GameReg' | grep -v grep
if [ $? -ne 0 ]; then
	echo "No GameReg process"
	exit 3
fi


exit 0
