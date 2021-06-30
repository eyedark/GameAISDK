#!/bin/sh

PWD=`pwd`
#./start.sh UI+AI /home/xdien/workspace/GameAISDK/project/LQ3/ LQ3
export PATH=$PATH:$PWD/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/opencv3.4.2/lib
if [ $# -gt 0 ]; then
    if [ $1 = AI ]; then
        ./start_ai.sh
        exit 1
    elif [ $1 = UI+AI ]; then
        ./start_ui_ai.sh ${2} ${3}
        exit 2
    elif [ $1 = TRAIN ]; then
        ./start_im_train.sh ${2} ${3}
        exit 3
    elif [ $1 = UI ]; then
        ./start_ui.sh ${2} ${3}
        exit 4
    fi
else
    ./start_ai.sh
    exit 1
fi

exit 0
