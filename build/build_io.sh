#!/bin/sh

echo "------------------------------------- build io start -------------------"

rm -rf ../bin/pyIOService
python3 CompilePy3Pyc.py ../src/IOService/pyIOService/  ../bin/pyIOService/ || exit 1
cp -f ../src/IOService/*.py  ../bin/ || exit 2

echo "------------------------------------- build io end -------------------\n"

echo "------------------------------------- build AIClient start -------------------"

rm -rf ../tools/AIClient 
python3 CompilePy3Pyc.py ../src/AIClient/  ../tools/AIClient/ || exit 1
rm -rf ../tools/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/touchserver || exit 2
rm -rf ../tools/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/input || exit 2
cp -f ../src/AIClient/demo.py  ../tools/AIClient/ || exit 2
cp -R ../src/AIClient/aiclient/cfg  ../tools/AIClient/aiclient/ || exit 2
cp -R ../src/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/cloudscreen ../tools/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/ || exit 2
cp -R ../src/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/input ../tools/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/ || exit 2
# cp -R ../src/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/pb ../tools/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/ || exit 2
# cp -R ../src/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/apk/* ../tools/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/apk/ || exit 2
cp -R ../src/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/touchserver ../tools/AIClient/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/ || exit 2
cp ../src/AIClient/aiclient/cfg/resource_result.json  ../tools/AIClient/tools/resource_result.json || exit 2


echo "------------------------------------- build AIClient end -------------------\n"