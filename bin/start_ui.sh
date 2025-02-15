#!/bin/sh

PWD=`pwd`
export PATH=$PATH:$PWD/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/lib:/usr/local/lib64

echo "Run UI Service"


#Start MC process
python3 manage_center.py --runType=UI >/dev/null 2>&1 &
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


#Start UIRecognize process
./UIRecognize >/dev/null 2>&1 &
sleep 1

#Check UIRecognize process
ps -fe | grep 'UIRecognize' | grep -v grep
if [ $? -ne 0 ]; then
	echo "No UIRecognize process"
	exit 2
fi


exit 0
