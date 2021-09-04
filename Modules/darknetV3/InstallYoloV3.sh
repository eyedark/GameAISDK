#!/bin/sh

# buildYoloV3()
# {
#     cd src;
#     make -j12 || exit 1
#     make install || exit 2
# }

# if [ $# -gt 0 ]; then
#     if [ $1 = GPU ]; then
#         cp Makefile_GPU src/Makefile
#         buildYoloV3
#     elif [ $1 = CPU ]; then
#         cp Makefile_CPU src/Makefile
#         buildYoloV3
#     fi
# else
#     cp Makefile_CPU src/Makefile
#     buildYoloV3

#     cp Makefile_GPU src/Makefile
#     buildYoloV3
# fi

cd src
rm -rf build
mkdir build
cd build
#cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
cmake -DOpenCV_DIR=/usr/local/share/OpenCV -DCMAKE_INSTALL_PREFIX=/usr/local ../
make -j12

if [ $# -gt 0 ]; then
    if [ $1 = GPU ]; then
        cp libdarknet.so ../../lib/libdarknetV3_GPU.so
        cp libdarknet.so ../../lib/libdarknet.so

        cp libdarknet.so ../../../../src/ImgProc/GameRecognize/Lib/libdarknetV3_GPU.so
        cp libdarknet.so ../../../../src/ImgProc/GameRecognize/Lib/libdarknet.so

        cp libdarknet.so ../../../../bin/libdarknetV3_GPU.so
        cp libdarknet.so ../../../../bin/libdarknet.so
    elif [ $1 = CPU ]; then
        cp libdarknet.so ../../lib/libdarknetV3_CPU.so
        cp libdarknet.so ../../../../src/ImgProc/GameRecognize/Lib/libdarknetV3_CPU.so
        cp libdarknet.so ../../../../bin/libdarknetV3_CPU.so
        cp libdarknet.so ../../../../bin/libdarknet.so
    fi
    cp ../include/darknet.h ../../include/
# else
#     cp Makefile_CPU src/Makefile
#     buildYoloV3

#     cp Makefile_GPU src/Makefile
#     buildYoloV3
fi


