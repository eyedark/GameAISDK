AM_CXXFLAGS=-fPIC  -fpermissive -g -O0 -std=c++11 -Wl,-E \
            -I /usr/local/protobuf-3.2.0.so/include \
            -I  ../include \
            -I  ../Comm/Os \
            -I  ../Comm/Utils \
            -I  ../Protobuf \
            -I  Src \
            -I  ../../../Modules/Json/include \
            -I  ../../../Modules/Lua/include \
            -I  ../../../Modules/tbus/libtbus/include \
            -I  ../Comm/ImgReg/Recognizer \
            -I  /usr/include/python3.8 \
            -L  /usr/lib/python3.8/config-3.8-x86_64-linux-gnu/ \
            -L  ../../../Modules/Json/jsoncpp-master/build/release/src/lib_json \
            -I  ../ \
            -L  /usr/local/lib64 \
            -L ../GameRecognize/Lib\
            -D USE_HOG_PREDICTION \
            -D LINUX \
            -D UI_PROCESS=1
AUTOMAKE_OPTIONS = subdir-objects
bin_PROGRAMS=UIRecognize
UIRecognize_SOURCES=../Comm/Utils/TqcCommon.cpp \
                    ../Comm/Utils/Log.cpp \
                    ../Comm/Utils/IniConfig.cpp \
                    ../Comm/Utils/TqcLock.cpp \
                    ../Comm/Utils/JsonConfig.cpp \
                    ../Comm/Utils/TqcString.cpp \
                    ../Comm/Utils/Pool.cpp \
                    ../Comm/Utils/GameUtils.cpp \
                    ../Comm/Os/Linux/TqcLinuxOS.cpp \
                    ../Comm/ImgReg/Recognizer/CLocationReg.cpp \
                    ../Comm/ImgReg/ImgProcess/CColorMatch.cpp \
                    ../Comm/ImgReg/ImgProcess/ImgComn.cpp \
                    ../Comm/ImgReg/ImgProcess/CYOLOAPI.cpp \
                    ../Comm/ImgReg/ImgProcess/CORBMatch.cpp \
                    ../Comm/ImgReg/ImgProcess/CObjDet.cpp \
                    Src/Action/Action.cpp \
                    Src/Action/SendAction.cpp \
                    Src/Communicate/DataManager.cpp \
                    Src/Communicate/PBMsgManager.cpp \
                    Src/GameState/GameOverState.cpp \
                    Src/GameState/GameRunState.cpp \
                    Src/GameState/GameStartState.cpp \
                    Src/GameState/HallState.cpp \
                    Src/UICfg/CommUICfg.cpp \
                    Src/UICfg/GameOverCfg.cpp \
                    Src/UICfg/GameStartCfg.cpp \
                    Src/UICfg/HallCfg.cpp \
                    Src/UICfg/POPUICfg.cpp \
                    Src/UIReg/CommonUIReg.cpp \
                    Src/UIReg/GameOverReg.cpp \
                    Src/UIReg/GameStartReg.cpp \
                    Src/UIReg/HallReg.cpp \
                    Src/UIReg/POPUIReg.cpp \
                    Src/UIFrameWork.cpp \
                    Src/Main.cpp \
                    ../Protobuf/common.pb.cc \
                    ../Protobuf/gameregProtoc.pb.cc


LIBS=-L/usr/local/lib64 $(UIRECOGNIZELIBFLAG) $(LIBDARKNET) -ljsoncpp -L/usr/lib64 -lpython3.8 -lcrypt -lpthread -ldl  -lutil -lm -Wl,-Bdynamic