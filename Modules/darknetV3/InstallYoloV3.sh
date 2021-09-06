

cd src
rm -rf build
mkdir build
cd build
if [ $# -gt 0 ]; then
    if [ $1 = GPU ]; then
        #cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
        cmake -DOpenCV_DIR=/usr/local/share/OpenCV -DCMAKE_INSTALL_PREFIX=/usr/local ../
        make -j12
        cp libdarknet.so ../../lib/libdarknetV3_GPU.so
        cp libdarknet.so ../../lib/libdarknet.so

        cp libdarknet.so ../../../../src/ImgProc/GameRecognize/Lib/libdarknetV3_GPU.so
        cp libdarknet.so ../../../../src/ImgProc/GameRecognize/Lib/libdarknet.so

        cp libdarknet.so ../../../../bin/libdarknetV3_GPU.so
        cp libdarknet.so ../../../../bin/libdarknet.so
    elif [ $1 = CPU ]; then
        cmake -DENABLE_CUDA=0 -DENABLE_OPENCV=0 -DCMAKE_INSTALL_PREFIX=/usr/local ../
        make -j12
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


