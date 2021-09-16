#!/bin/bash
CURENT_DIR=`pwd`
if [[ -z "${ANDROID_NDK_HOME}" ]]; then
  echo "ANDROID_NDK_HOME is not set"
  exit -1
fi
if [[ -z "${ANDROID_SDK_ROOT}" ]]; then
  echo "ANDROID_SDK_ROOT is not set"
  exit -1
fi
export PATH=$ANDROID_NDK_HOME:$PATH
function build_minicap(){
    git clone https://github.com:DeviceFarmer/minicap.git
    cd minicap
    git submodule init
    git submodule update
    ndk-build || exit -1
    #copy file 
    DST_DIR=$CURENT_DIR/../tools/SDKTool/src/WrappedDeviceAPI/deviceAPI/mobileDevice/android/PlatformMinicap/vendor/minicap/jni/minicap-shared/aosp/libs
    rm -rf $DST_DIR/*
    cp -R jni/minicap-shared/aosp/libs/* $DST_DIR/
    #clone Vecter_Issus for Xiaomi, Vivo, LG
    cd $CURENT_DIR/../tools/SDKTool/src/WrappedDeviceAPI/deviceAPI/mobileDevice/android/PlatformMinicap/vendor/minicap/jni
    git clone https://github.com:varundtsfi/Xiaomi_Vector_issue.git
    # fix issus https://github.com/varundtsfi/Xiaomi_Vector_issue/issues/7 
    cd Xiaomi_Vector_issue
    cp Xiaomi/android-30/arm64-v8a/minicap.so Xiaomi/android-30/arm64-v8a/minicap32.so
    cp Xiaomi/android-30/arm64-v8a/nw_minicap.so Xiaomi/android-30/arm64-v8a/minicap.so
    cd $CURENT_DIR
}

function build_minitouch(){
  cd $CURENT_DIR
  git clone https://github.com:openstf/minitouch.git
  cd minitouch
  git submodule init
  git submodule update
  ndk-build || exit -1
  cp -R libs/* $CURENT_DIR/../tools/SDKTool/src/WrappedDeviceAPI/deviceAPI/mobileDevice/android/PlatformMinicap/vendor/minitouch/libs/
}
function buidl_stf_services(){
  cd $CURENT_DIR
  #fix issus for android sdk 29
  git clone https://github.com:openstf/STFService.apk.git
  cd STFService.apk
  ./gradlew assembleDebug || exit -1
  cp app/build/outputs/apk/debug/app-debug.apk $CURENT_DIR/../tools/SDKTool/src/WrappedDeviceAPI/deviceAPI/mobileDevice/android/PlatformMinicap/vendor/stf_services.apk
}
build_minicap
build_minitouch
buidl_stf_services