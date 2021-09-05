
########### next target ###############
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
SET(UIRecognize_SRCS
   ../Comm/Utils/TqcCommon.cpp
   ../Comm/Utils/TqcCommon.h
   ../Comm/Utils/Log.cpp
   ../Comm/Utils/IniConfig.cpp
   ../Comm/Utils/TqcLock.cpp
   ../Comm/Utils/JsonConfig.cpp
   ../Comm/Utils/TqcString.cpp
   ../Comm/Utils/Pool.cpp
   ../Comm/Utils/GameUtils.cpp
   ../Comm/Os/Linux/TqcLinuxOS.cpp
   ../Comm/ImgReg/Recognizer/CLocationReg.cpp
   ../Comm/ImgReg/ImgProcess/CColorMatch.cpp
   ../Comm/ImgReg/ImgProcess/ImgComn.cpp
   ../Comm/ImgReg/ImgProcess/CYOLOAPI.cpp
   ../Comm/ImgReg/ImgProcess/CORBMatch.cpp
   ../Comm/ImgReg/ImgProcess/CObjDet.cpp
   Src/Action/Action.cpp
   Src/Action/SendAction.cpp
   Src/Communicate/DataManager.cpp
   Src/Communicate/PBMsgManager.cpp
   Src/GameState/GameOverState.cpp
   Src/GameState/GameRunState.cpp
   Src/GameState/GameStartState.cpp
   Src/GameState/HallState.cpp
   Src/UICfg/CommUICfg.cpp
   Src/UICfg/GameOverCfg.cpp
   Src/UICfg/GameStartCfg.cpp
   Src/UICfg/HallCfg.cpp
   Src/UICfg/POPUICfg.cpp
   Src/UIReg/CommonUIReg.cpp
   Src/UIReg/GameOverReg.cpp
   Src/UIReg/GameStartReg.cpp
   Src/UIReg/HallReg.cpp
   Src/UIReg/POPUIReg.cpp
   Src/UIFrameWork.cpp
   Src/Main.cpp
   ../Protobuf/common.pb.cc
   ../Protobuf/gameregProtoc.pb.cc
)

include_directories("../")
include_directories("../../../")
include_directories("../../../Modules/darknetV3/include")
include_directories("../../../Modules/Json/include")
include_directories("/usr/include/python3.8")
include_directories("../../../Modules/tbus/libtbus/include")
link_directories("../../../Modules/Json/Linux/")
link_directories("/usr/local/lib64")
link_directories("../../../bin")
add_compile_definitions(UI_PROCESS=1)
add_compile_definitions(USE_HOG_PREDICTION)

add_executable(UIRecognize ${UIRecognize_SRCS})

target_link_libraries(UIRecognize jsoncpp boost_system boost_thread dl opencv_core opencv_features2d opencv_highgui opencv_imgcodecs opencv_imgproc opencv_photo opencv_video opencv_videoio protobuf pthread tbus darknet python3.8)

install(TARGETS UIRecognize DESTINATION bin)


########### install files ###############




#original Makefile.am contents follow:

#AM_CXXFLAGS=-fPIC  -fpermissive -g -O0 -std=c++11 -Wl,-E \
#            -I /usr/local/protobuf-3.2.0.so/include \
#            -I  ../include \
#            -I  ../Comm/Os \
#            -I  ../Comm/Utils \
#            -I  ../Protobuf \
#            -I  Src \
#            -I  ../../../Modules/Json/include \
#            -I  ../../../Modules/Lua/include \
#            -I  ../../../Modules/tbus/libtbus/include \
#            -I  ../Comm/ImgReg/Recognizer \
#            -I  /usr/include/python3.8 \
#            -L  /usr/lib/python3.8/config-3.8-x86_64-linux-gnu/ \
#            -L  ../../../Modules/Json/jsoncpp-master/build/release/src/lib_json \
#            -I  ../ \
#            -L  /usr/local/lib64 \
#            -L ../GameRecognize/Lib\
#            -D USE_HOG_PREDICTION \
#            -D LINUX \
#            -D UI_PROCESS=1
#AUTOMAKE_OPTIONS = subdir-objects
#bin_PROGRAMS=UIRecognize
#UIRecognize_SOURCES=../Comm/Utils/TqcCommon.cpp \
#                    ../Comm/Utils/Log.cpp \
#                    ../Comm/Utils/IniConfig.cpp \
#                    ../Comm/Utils/TqcLock.cpp \
#                    ../Comm/Utils/JsonConfig.cpp \
#                    ../Comm/Utils/TqcString.cpp \
#                    ../Comm/Utils/Pool.cpp \
#                    ../Comm/Utils/GameUtils.cpp \
#                    ../Comm/Os/Linux/TqcLinuxOS.cpp \
#                    ../Comm/ImgReg/Recognizer/CLocationReg.cpp \
#                    ../Comm/ImgReg/ImgProcess/CColorMatch.cpp \
#                    ../Comm/ImgReg/ImgProcess/ImgComn.cpp \
#                    ../Comm/ImgReg/ImgProcess/CYOLOAPI.cpp \
#                    ../Comm/ImgReg/ImgProcess/CORBMatch.cpp \
#                    ../Comm/ImgReg/ImgProcess/CObjDet.cpp \
#                    Src/Action/Action.cpp \
#                    Src/Action/SendAction.cpp \
#                    Src/Communicate/DataManager.cpp \
#                    Src/Communicate/PBMsgManager.cpp \
#                    Src/GameState/GameOverState.cpp \
#                    Src/GameState/GameRunState.cpp \
#                    Src/GameState/GameStartState.cpp \
#                    Src/GameState/HallState.cpp \
#                    Src/UICfg/CommUICfg.cpp \
#                    Src/UICfg/GameOverCfg.cpp \
#                    Src/UICfg/GameStartCfg.cpp \
#                    Src/UICfg/HallCfg.cpp \
#                    Src/UICfg/POPUICfg.cpp \
#                    Src/UIReg/CommonUIReg.cpp \
#                    Src/UIReg/GameOverReg.cpp \
#                    Src/UIReg/GameStartReg.cpp \
#                    Src/UIReg/HallReg.cpp \
#                    Src/UIReg/POPUIReg.cpp \
#                    Src/UIFrameWork.cpp \
#                    Src/Main.cpp \
#                    ../Protobuf/common.pb.cc \
#                    ../Protobuf/gameregProtoc.pb.cc
#
#
#LIBS=-L/usr/local/lib64 $(UIRECOGNIZELIBFLAG) $(LIBDARKNET) -ljsoncpp -lpython3.8 -lcrypt -lpthread -ldl  -lutil -lm -Wl,-Bdynamic
