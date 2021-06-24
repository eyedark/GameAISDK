#!/bin/sh

echo "------------------------------------- build cpp programe start -------------------"

if [ $# -lt 1 ]; then
	echo "useage: GPU|CPU"
	exit 1
fi

cd ../src/ImgProc

export CPATH=$CPATH:/usr/local/include:/usr/include/python3.7m
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/lib

if [ $# -gt 0 ]; then
    param=""
    if [ $1 = GPU ]; then
        param="--enable-GPU"
    elif [ $1 = CPU ]; then
        param=""
    fi

    aclocal
    autoconf
    autoheader
    automake --add-missing
    ./configure ${param} || exit 4
    make || exit 5

    mv UI/UIRecognize ../../bin/ || exit 6
    mv GameRecognize/GameReg ../../bin/ || exit 7
fi

cd -

echo "------------------------------------- build cpp programe end -------------------\n"