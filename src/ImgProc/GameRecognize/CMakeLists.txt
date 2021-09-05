
########### next target ###############
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
SET(GameReg_SRCS
   src/main.cpp
   src/GameRegFrameWork.cpp
   src/IniConfClass.cpp
   src/NetWorkManager.cpp
   src/SerializeProtobuf.cpp
   src/TaskMgr/TaskContext.cpp
   src/TaskMgr/TaskDataDeal.cpp
   src/TaskMgr/TaskManager.cpp
   src/TaskMgr/TaskMessage.cpp
   src/TaskMgr/TaskMultiResMgr.cpp
   src/TaskMgr/TaskResult.cpp
   ../Comm/ImgReg/Recognizer/CBloodLengthReg.cpp
   ../Comm/ImgReg/Recognizer/CBloodLengthReg.cpp
   ../Comm/ImgReg/Recognizer/CDeformBloodReg.cpp
   ../Comm/ImgReg/Recognizer/CDeformObjReg.cpp
   ../Comm/ImgReg/Recognizer/CFixBloodReg.cpp
   ../Comm/ImgReg/Recognizer/CFixObjReg.cpp
   ../Comm/ImgReg/Recognizer/CKingGloryBloodReg.cpp
   ../Comm/ImgReg/Recognizer/CLocationReg.cpp
   ../Comm/ImgReg/Recognizer/CMapReg.cpp
   ../Comm/ImgReg/Recognizer/CMultColorVarReg.cpp
   ../Comm/ImgReg/Recognizer/CNumReg.cpp
   ../Comm/ImgReg/Recognizer/CPixReg.cpp
   ../Comm/ImgReg/Recognizer/CShootGameBloodReg.cpp
   ../Comm/ImgReg/Recognizer/CShootGameHurtReg.cpp
   ../Comm/ImgReg/Recognizer/CStuckReg.cpp
   ../Comm/ImgReg/Recognizer/CMapDirectionReg.cpp
   ../Protobuf/common.pb.cc
   ../Protobuf/gameregProtoc.pb.cc
   ../Comm/ImgReg/ImgProcess/CColorBinMatch.cpp
   ../Comm/ImgReg/ImgProcess/CColorDet.cpp
   ../Comm/ImgReg/ImgProcess/CColorMatch.cpp
   ../Comm/ImgReg/ImgProcess/CEdgeMatch.cpp
   ../Comm/ImgReg/ImgProcess/CGradMatch.cpp
   ../Comm/ImgReg/ImgProcess/CObjDet.cpp
   ../Comm/ImgReg/ImgProcess/CORBMatch.cpp
   ../Comm/ImgReg/ImgProcess/CYOLOAPI.cpp
   ../Comm/ImgReg/ImgProcess/ImgComn.cpp
   ../Comm/Utils/GameTime.cpp
   ../Comm/Utils/IniConfig.cpp
   ../Comm/Utils/JsonConfig.cpp
   ../Comm/Utils/TqcCommon.cpp
   ../Comm/Utils/TqcMemoryPool.cpp
   ../Comm/Utils/TqcThreadPool.cpp
   ../Comm/Utils/Log.cpp
   ../Comm/Utils/TqcLock.cpp
   ../Comm/Utils/TqcString.cpp
   ../Comm/Os/Linux/TqcLinuxOS.cpp
)

include_directories("../")
include_directories("../../../")
include_directories("../../../Modules/darknetV3/include")
include_directories("../../../Modules/Json/include")
link_directories("../../../Modules/Json/Linux/")
link_directories("/usr/local/lib64")
link_directories("../../../bin")

add_executable(GameReg ${GameReg_SRCS})

target_link_libraries(GameReg jsoncpp boost_system boost_thread dl opencv_core opencv_features2d opencv_highgui opencv_imgcodecs opencv_imgproc opencv_photo opencv_video opencv_videoio protobuf pthread tbus darknet)

install(TARGETS GameReg DESTINATION bin)


########### install files ###############




#original Makefile.am contents follow:

#AM_CXXFLAGS=-DLINUX -D_GNU_SOURCE -D$(GPUDEF) \
#            -Wno-deprecated -fPIC -std=c++11 -g -pipe -DDEBUG -Woverloaded-virtual -Wpointer-arith -fno-strict-aliasing  -D__STDC_FORMAT_MACROS -Wno-write-strings \
#            -I../../../Modules/Json/include -I/opt/cuda/include -I/usr/local/include \
#            -I../ -I../../../ \
#            -I../../../Modules/darknetV3/include \
#            -L./Lib -L../../../Modules/Json/jsoncpp-master/build/release/src/lib_json -L/usr/local/lib64 -O0
#AUTOMAKE_OPTIONS = subdir-objects
#bin_PROGRAMS=GameReg
#GameReg_SOURCES=src/main.cpp \
#                src/GameRegFrameWork.cpp \
#                src/IniConfClass.cpp \
#                src/NetWorkManager.cpp \
#                src/SerializeProtobuf.cpp \
#                src/TaskMgr/TaskContext.cpp \
#                src/TaskMgr/TaskDataDeal.cpp \
#                src/TaskMgr/TaskManager.cpp \
#                src/TaskMgr/TaskMessage.cpp \
#                src/TaskMgr/TaskMultiResMgr.cpp \
#                src/TaskMgr/TaskResult.cpp \
#                ../Comm/ImgReg/Recognizer/CBloodLengthReg.cpp \
#                ../Comm/ImgReg/Recognizer/CDeformBloodReg.cpp \
#                ../Comm/ImgReg/Recognizer/CDeformObjReg.cpp \
#                ../Comm/ImgReg/Recognizer/CFixBloodReg.cpp \
#                ../Comm/ImgReg/Recognizer/CFixObjReg.cpp \
#                ../Comm/ImgReg/Recognizer/CKingGloryBloodReg.cpp \
#                ../Comm/ImgReg/Recognizer/CLocationReg.cpp \
#                ../Comm/ImgReg/Recognizer/CMapReg.cpp \
#                ../Comm/ImgReg/Recognizer/CMultColorVarReg.cpp \
#                ../Comm/ImgReg/Recognizer/CNumReg.cpp \
#                ../Comm/ImgReg/Recognizer/CPixReg.cpp \
#                ../Comm/ImgReg/Recognizer/CShootGameBloodReg.cpp \
#                ../Comm/ImgReg/Recognizer/CShootGameHurtReg.cpp \
#                ../Comm/ImgReg/Recognizer/CStuckReg.cpp \
#                ../Comm/ImgReg/Recognizer/CMapDirectionReg.cpp \
#                ../Protobuf/common.pb.cc \
#                ../Protobuf/gameregProtoc.pb.cc \
#                ../Comm/ImgReg/ImgProcess/CColorBinMatch.cpp \
#                ../Comm/ImgReg/ImgProcess/CColorDet.cpp \
#                ../Comm/ImgReg/ImgProcess/CColorMatch.cpp \
#                ../Comm/ImgReg/ImgProcess/CEdgeMatch.cpp \
#                ../Comm/ImgReg/ImgProcess/CGradMatch.cpp \
#                ../Comm/ImgReg/ImgProcess/CObjDet.cpp \
#                ../Comm/ImgReg/ImgProcess/CORBMatch.cpp \
#                ../Comm/ImgReg/ImgProcess/CYOLOAPI.cpp \
#                ../Comm/ImgReg/ImgProcess/ImgComn.cpp \
#                ../Comm/Utils/GameTime.cpp \
#                ../Comm/Utils/IniConfig.cpp \
#                ../Comm/Utils/JsonConfig.cpp \
#                ../Comm/Utils/TqcCommon.cpp \
#                ../Comm/Utils/TqcMemoryPool.cpp \
#                ../Comm/Utils/TqcThreadPool.cpp \
#                ../Comm/Utils/Log.cpp \
#                ../Comm/Utils/TqcLock.cpp \
#                ../Comm/Utils/TqcString.cpp \
#                ../Comm/Os/Linux/TqcLinuxOS.cpp
#
#
#LIBS=$(GAMEREGLIBFLAG) $(LIBDARKNET) -ljsoncpp -Wl,-Bdynamic
