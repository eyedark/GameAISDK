# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/pb/cloudscreen/CloudscreenPkgPB_pb2.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 69994 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='cloudscreen/CloudscreenPkgPB.proto', package='com.tencent.wetest.pb.cloudscreen', syntax='proto3', serialized_options=_b('\n!com.tencent.wetest.pb.cloudscreenB\x10CloudscrennPkgPB'), serialized_pb=_b('\n"cloudscreen/CloudscreenPkgPB.proto\x12!com.tencent.wetest.pb.cloudscreen"=\n\x15CloudscreenVersionRes\x12\x13\n\x0bversioncode\x18\x01 \x01(\x05\x12\x0f\n\x07version\x18\x02 \x01(\t"r\n\x11CloudscreenResult\x12J\n\terrorcode\x18\x01 \x01(\x0e27.com.tencent.wetest.pb.cloudscreen.CloudscreenErrorCode\x12\x11\n\terrordesc\x18\x02 \x01(\t"\x90\x02\n\x14DisplayDeviceInfoRes\x12D\n\x06result\x18\x01 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.CloudscreenResult\x12\r\n\x05width\x18\x02 \x01(\x05\x12\x0e\n\x06height\x18\x03 \x01(\x05\x12\x0b\n\x03fps\x18\x04 \x01(\x02\x12\x0f\n\x07density\x18\x05 \x01(\x02\x12\x0c\n\x04xdpi\x18\x06 \x01(\x02\x12\x0c\n\x04ydpi\x18\x07 \x01(\x02\x12I\n\x0borientation\x18\x08 \x01(\x0e24.com.tencent.wetest.pb.cloudscreen.ScreenOrientation\x12\x0e\n\x06secure\x18\t \x01(\x08"ñ\x01\n\x10ScreenCaptureReq\x12\r\n\x05index\x18\x01 \x01(\x05\x12O\n\x11screenCaptureMode\x18\x02 \x01(\x0e24.com.tencent.wetest.pb.cloudscreen.ScreenCaptureMode\x12I\n\x0bcaptureType\x18\x03 \x01(\x0e24.com.tencent.wetest.pb.cloudscreen.ScreenCaptureType\x12\x0e\n\x06height\x18\x04 \x01(\x05\x12\x0f\n\x07quality\x18\x05 \x01(\x05\x12\x11\n\talignment\x18\x06 \x01(\x08"\x9f\x02\n\x10ScreenCaptureRes\x12D\n\x06result\x18\x01 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.CloudscreenResult\x12\r\n\x05index\x18\x02 \x01(\x05\x12I\n\x0bcaptureType\x18\x03 \x01(\x0e24.com.tencent.wetest.pb.cloudscreen.ScreenCaptureType\x12\r\n\x05width\x18\x04 \x01(\x05\x12\x0e\n\x06height\x18\x05 \x01(\x05\x12\x0e\n\x06stride\x18\x06 \x01(\x05\x12\x0b\n\x03bpp\x18\x07 \x01(\x05\x12\x13\n\x0borientation\x18\x08 \x01(\x05\x12\x0b\n\x03len\x18\t \x01(\x05\x12\r\n\x05datas\x18\n \x01(\x0c"l\n\x11StartH264VideoReq\x12\x11\n\tlandscape\x18\x01 \x01(\x08\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\x0f\n\x07bitrate\x18\x03 \x01(\x03\x12\x16\n\x0eiFrameInterval\x18\x04 \x01(\x05\x12\x0b\n\x03fps\x18\x05 \x01(\x05"Á\x01\n\x11StartH264VideoRes\x12D\n\x06result\x18\x01 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.CloudscreenResult\x12\x11\n\tlandscape\x18\x03 \x01(\x08\x12\r\n\x05width\x18\x04 \x01(\x05\x12\x0e\n\x06height\x18\x05 \x01(\x05\x12\x0f\n\x07bitrate\x18\x06 \x01(\x03\x12\x16\n\x0eiFrameInterval\x18\x07 \x01(\x05\x12\x0b\n\x03fps\x18\x08 \x01(\x05"+\n\nH264Config\x12\r\n\x05width\x18\x01 \x01(\x05\x12\x0e\n\x06height\x18\x02 \x01(\x05"Í\x02\n\x14H264VideoFrameNotify\x12D\n\x06result\x18\x01 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.CloudscreenResult\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x0b\n\x03pts\x18\x03 \x01(\x03\x12\r\n\x05delay\x18\x04 \x01(\x05\x12\x13\n\x0borientation\x18\x05 \x01(\x05\x12\x0f\n\x07pkgSize\x18\x06 \x01(\x05\x12\r\n\x05datas\x18\x07 \x01(\x0c\x12H\n\tframeType\x18\x08 \x01(\x0e25.com.tencent.wetest.pb.cloudscreen.H264VideoFrameType\x12A\n\nh264Config\x18\t \x01(\x0b2-.com.tencent.wetest.pb.cloudscreen.H264Config"v\n\x18ScreenCapturePushModeReq\x12\x0e\n\x06height\x18\x01 \x01(\x05\x12\x0f\n\x07quality\x18\x02 \x01(\x05\x12\x13\n\x0bminInterval\x18\x03 \x01(\x05\x12\x11\n\tlandscape\x18\x04 \x01(\x08\x12\x11\n\talignment\x18\x05 \x01(\x08"`\n\x18ScreenCapturePushModeRes\x12D\n\x06result\x18\x01 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.CloudscreenResult"¿\x01\n\x18ScreenCaptureFrameNotify\x12D\n\x06result\x18\x01 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.CloudscreenResult\x12\r\n\x05index\x18\x02 \x01(\x05\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\x12\x13\n\x0borientation\x18\x05 \x01(\x05\x12\x0b\n\x03len\x18\x06 \x01(\x05\x12\r\n\x05datas\x18\x07 \x01(\x0c"\'\n\x12DeviceTimestampRes\x12\x11\n\ttimestamp\x18\x01 \x01(\x03"\x82\x01\n\x11CloudscreenHeader\x12\x12\n\nsequenceId\x18\x01 \x01(\x03\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12F\n\x07command\x18\x03 \x01(\x0e25.com.tencent.wetest.pb.cloudscreen.CloudscreenCommand"È\x07\n\x0fCloudscreenBody\x12W\n\x15cloudscreenVersionRes\x18\x01 \x01(\x0b28.com.tencent.wetest.pb.cloudscreen.CloudscreenVersionRes\x12U\n\x14displayDeviceInfoRes\x18\x02 \x01(\x0b27.com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes\x12M\n\x10screenCaptureReq\x18\x03 \x01(\x0b23.com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq\x12M\n\x10screenCaptureRes\x18\x04 \x01(\x0b23.com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes\x12O\n\x11startH264VideoReq\x18\x05 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.StartH264VideoReq\x12O\n\x11startH264VideoRes\x18\x06 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.StartH264VideoRes\x12U\n\x14h264VideoFrameNotify\x18\x07 \x01(\x0b27.com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify\x12]\n\x18screenCapturePushModeReq\x18\x08 \x01(\x0b2;.com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeReq\x12]\n\x18screenCapturePushModeRes\x18\t \x01(\x0b2;.com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeRes\x12]\n\x18screenCaptureFrameNotify\x18\n \x01(\x0b2;.com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify\x12Q\n\x12deviceTimestampRes\x18\x0b \x01(\x0b25.com.tencent.wetest.pb.cloudscreen.DeviceTimestampRes"\x98\x01\n\x0eCloudscreenPkg\x12D\n\x06header\x18\x01 \x01(\x0b24.com.tencent.wetest.pb.cloudscreen.CloudscreenHeader\x12@\n\x04body\x18\x02 \x01(\x0b22.com.tencent.wetest.pb.cloudscreen.CloudscreenBody*\x94\x05\n\x12CloudscreenCommand\x12\x17\n\x13UNKNOWN_CLOUDSCREEN\x10\x00\x12\x1d\n\x19CLOUDSCREEN_HEARTBEAT_REQ\x10\x01\x12\x1d\n\x19CLOUDSCREEN_HEARTBEAT_RES\x10\x02\x12\x1b\n\x17CLOUDSCREEN_VERSION_REQ\x10\x03\x12\x1b\n\x17CLOUDSCREEN_VERSION_RES\x10\x04\x12\x1b\n\x17DISPLAY_DEVICE_INFO_REQ\x10\x05\x12\x1b\n\x17DISPLAY_DEVICE_INFO_RES\x10\x06\x12\x16\n\x12SCREEN_CAPTURE_REQ\x10\x07\x12\x16\n\x12SCREEN_CAPTURE_RES\x10\x08\x12\x17\n\x13START_H264VIDEO_REQ\x10\t\x12\x17\n\x13START_H264VIDEO_RES\x10\n\x12\x16\n\x12STOP_H264VIDEO_REQ\x10\x0b\x12\x16\n\x12STOP_H264VIDEO_RES\x10\x0c\x12\x1a\n\x16H264VIDEO_FRAME_NOTIFY\x10\r\x12 \n\x1cSCREEN_CAPTURE_PUSH_MODE_REQ\x10\x0e\x12 \n\x1cSCREEN_CAPTURE_PUSH_MODE_RES\x10\x0f\x12 \n\x1cSCREEN_CAPTURE_PUSH_STOP_REQ\x10\x10\x12 \n\x1cSCREEN_CAPTURE_PUSH_STOP_RES\x10\x11\x12\x1f\n\x1bSCREEN_CAPTURE_FRAME_NOTIFY\x10\x12\x12\x18\n\x14DEVICE_TIMESTAMP_REQ\x10\x13\x12\x18\n\x14DEVICE_TIMESTAMP_RES\x10\x14\x12(\n$SCREEN_CAPTURE_PUSH_MODE_STOP_NOTIFY\x10\x15*þ\x03\n\x14CloudscreenErrorCode\x12\x14\n\x10CLOUDSCREEN_SUCC\x10\x00\x12&\n"CLOUDSCREEN_GET_DISPLAY_INFO_ERROR\x10\x01\x12\x1d\n\x19CLOUDSCREEN_CAPTURE_ERROR\x10\x02\x12$\n CLOUDSCREEN_CAPTURE_HEIGHT_ERROR\x10\x03\x12+\n\'CLOUDSCREEN_CAPTURE_JPEG_COMPRESS_ERROR\x10\x04\x12$\n CLOUDSCREEN_CREATE_PTHREAD_ERROR\x10\x05\x12"\n\x1eCLOUDSCREEN_CPU_CONSUMER_ERROR\x10\x06\x12\'\n#CLOUDSCREEN_MEDIACODEC_CONFIG_ERROR\x10\x07\x12)\n%CLOUDSCREEN_VIDEO_FPS_UNSUPPORT_ERROR\x10\x08\x12%\n!CLOUDSCREEN_SCREENCAP_OPEN_FAILED\x10\t\x12$\n CLOUDSCREEN_SCREENCAP_READ_ERROR\x10\n\x12#\n\x1fCLOUDSCREEN_SCREENCAP_EOF_ERROR\x10\x0b\x12&\n"CLOUDSCREEN_SCREENCAP_FORMAT_ERROR\x10\x0c*\x9f\x01\n\x11ScreenOrientation\x12\x18\n\x14SCREEN_ORIENTATION_0\x10\x00\x12\x19\n\x15SCREEN_ORIENTATION_90\x10\x01\x12\x1a\n\x16SCREEN_ORIENTATION_180\x10\x02\x12\x1a\n\x16SCREEN_ORIENTATION_270\x10\x03\x12\x1d\n\x19SCREEN_ORIENTATION_UNKNOW\x10\x04*Ì\x01\n\x11ScreenCaptureMode\x12\x1f\n\x1bUNKNOWN_SCREEN_CAPTURE_MODE\x10\x00\x12\x1c\n\x18FULL_SCREEN_CAPTURE_MODE\x10\x01\x12\x17\n\x13SCALED_CAPTURE_MODE\x10\x02\x12\x1f\n\x1bDEFAULT_CONFIG_CAPTURE_MODE\x10\x03\x12\x1e\n\x1aGLOBAL_CONFIG_CAPTURE_MODE\x10\x04\x12\x1e\n\x1aPRESET_CONFIG_CAPTURE_MODE\x10\x05*X\n\x11ScreenCaptureType\x12\x1f\n\x1bUNKWOWN_SCREEN_CAPTURE_TYPE\x10\x00\x12\x10\n\x0cJPEG_CAPTURE\x10\x01\x12\x10\n\x0cRGBA_CAPTURE\x10\x02*d\n\x12H264VideoFrameType\x12\x1f\n\x1bUNKOWN_H264VIDEO_FRAME_TYPE\x10\x00\x12\r\n\tSPS_FRAME\x10\x01\x12\r\n\tPPS_FRAME\x10\x02\x12\x0f\n\x0bVIDEO_FRAME\x10\x03B5\n!com.tencent.wetest.pb.cloudscreenB\x10CloudscrennPkgPBb\x06proto3'))
_CLOUDSCREENCOMMAND = _descriptor.EnumDescriptor(name='CloudscreenCommand', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenCommand', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='UNKNOWN_CLOUDSCREEN', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_HEARTBEAT_REQ', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_HEARTBEAT_RES', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_VERSION_REQ', index=3, number=3, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_VERSION_RES', index=4, number=4, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DISPLAY_DEVICE_INFO_REQ', index=5, number=5, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DISPLAY_DEVICE_INFO_RES', index=6, number=6, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_REQ', index=7, number=7, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_RES', index=8, number=8, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='START_H264VIDEO_REQ', index=9, number=9, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='START_H264VIDEO_RES', index=10, number=10, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='STOP_H264VIDEO_REQ', index=11, number=11, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='STOP_H264VIDEO_RES', index=12, number=12, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='H264VIDEO_FRAME_NOTIFY', index=13, number=13, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_PUSH_MODE_REQ', index=14, number=14, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_PUSH_MODE_RES', index=15, number=15, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_PUSH_STOP_REQ', index=16, number=16, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_PUSH_STOP_RES', index=17, number=17, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_FRAME_NOTIFY', index=18, number=18, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DEVICE_TIMESTAMP_REQ', index=19, number=19, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DEVICE_TIMESTAMP_RES', index=20, number=20, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_CAPTURE_PUSH_MODE_STOP_NOTIFY', index=21, number=21, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=3461, serialized_end=4121)
_sym_db.RegisterEnumDescriptor(_CLOUDSCREENCOMMAND)
CloudscreenCommand = enum_type_wrapper.EnumTypeWrapper(_CLOUDSCREENCOMMAND)
_CLOUDSCREENERRORCODE = _descriptor.EnumDescriptor(name='CloudscreenErrorCode', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenErrorCode', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_SUCC', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_GET_DISPLAY_INFO_ERROR', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_CAPTURE_ERROR', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_CAPTURE_HEIGHT_ERROR', index=3, number=3, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_CAPTURE_JPEG_COMPRESS_ERROR', index=4, number=4, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_CREATE_PTHREAD_ERROR', index=5, number=5, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_CPU_CONSUMER_ERROR', index=6, number=6, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_MEDIACODEC_CONFIG_ERROR', index=7, number=7, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_VIDEO_FPS_UNSUPPORT_ERROR', index=8, number=8, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_SCREENCAP_OPEN_FAILED', index=9, number=9, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_SCREENCAP_READ_ERROR', index=10, number=10, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_SCREENCAP_EOF_ERROR', index=11, number=11, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='CLOUDSCREEN_SCREENCAP_FORMAT_ERROR', index=12, number=12, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=4124, serialized_end=4634)
_sym_db.RegisterEnumDescriptor(_CLOUDSCREENERRORCODE)
CloudscreenErrorCode = enum_type_wrapper.EnumTypeWrapper(_CLOUDSCREENERRORCODE)
_SCREENORIENTATION = _descriptor.EnumDescriptor(name='ScreenOrientation', full_name='com.tencent.wetest.pb.cloudscreen.ScreenOrientation', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='SCREEN_ORIENTATION_0', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_ORIENTATION_90', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_ORIENTATION_180', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_ORIENTATION_270', index=3, number=3, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCREEN_ORIENTATION_UNKNOW', index=4, number=4, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=4637, serialized_end=4796)
_sym_db.RegisterEnumDescriptor(_SCREENORIENTATION)
ScreenOrientation = enum_type_wrapper.EnumTypeWrapper(_SCREENORIENTATION)
_SCREENCAPTUREMODE = _descriptor.EnumDescriptor(name='ScreenCaptureMode', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureMode', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='UNKNOWN_SCREEN_CAPTURE_MODE', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='FULL_SCREEN_CAPTURE_MODE', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SCALED_CAPTURE_MODE', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DEFAULT_CONFIG_CAPTURE_MODE', index=3, number=3, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='GLOBAL_CONFIG_CAPTURE_MODE', index=4, number=4, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PRESET_CONFIG_CAPTURE_MODE', index=5, number=5, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=4799, serialized_end=5003)
_sym_db.RegisterEnumDescriptor(_SCREENCAPTUREMODE)
ScreenCaptureMode = enum_type_wrapper.EnumTypeWrapper(_SCREENCAPTUREMODE)
_SCREENCAPTURETYPE = _descriptor.EnumDescriptor(name='ScreenCaptureType', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='UNKWOWN_SCREEN_CAPTURE_TYPE', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='JPEG_CAPTURE', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='RGBA_CAPTURE', index=2, number=2, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=5005, serialized_end=5093)
_sym_db.RegisterEnumDescriptor(_SCREENCAPTURETYPE)
ScreenCaptureType = enum_type_wrapper.EnumTypeWrapper(_SCREENCAPTURETYPE)
_H264VIDEOFRAMETYPE = _descriptor.EnumDescriptor(name='H264VideoFrameType', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='UNKOWN_H264VIDEO_FRAME_TYPE', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SPS_FRAME', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PPS_FRAME', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='VIDEO_FRAME', index=3, number=3, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=5095, serialized_end=5195)
_sym_db.RegisterEnumDescriptor(_H264VIDEOFRAMETYPE)
H264VideoFrameType = enum_type_wrapper.EnumTypeWrapper(_H264VIDEOFRAMETYPE)
UNKNOWN_CLOUDSCREEN = 0
CLOUDSCREEN_HEARTBEAT_REQ = 1
CLOUDSCREEN_HEARTBEAT_RES = 2
CLOUDSCREEN_VERSION_REQ = 3
CLOUDSCREEN_VERSION_RES = 4
DISPLAY_DEVICE_INFO_REQ = 5
DISPLAY_DEVICE_INFO_RES = 6
SCREEN_CAPTURE_REQ = 7
SCREEN_CAPTURE_RES = 8
START_H264VIDEO_REQ = 9
START_H264VIDEO_RES = 10
STOP_H264VIDEO_REQ = 11
STOP_H264VIDEO_RES = 12
H264VIDEO_FRAME_NOTIFY = 13
SCREEN_CAPTURE_PUSH_MODE_REQ = 14
SCREEN_CAPTURE_PUSH_MODE_RES = 15
SCREEN_CAPTURE_PUSH_STOP_REQ = 16
SCREEN_CAPTURE_PUSH_STOP_RES = 17
SCREEN_CAPTURE_FRAME_NOTIFY = 18
DEVICE_TIMESTAMP_REQ = 19
DEVICE_TIMESTAMP_RES = 20
SCREEN_CAPTURE_PUSH_MODE_STOP_NOTIFY = 21
CLOUDSCREEN_SUCC = 0
CLOUDSCREEN_GET_DISPLAY_INFO_ERROR = 1
CLOUDSCREEN_CAPTURE_ERROR = 2
CLOUDSCREEN_CAPTURE_HEIGHT_ERROR = 3
CLOUDSCREEN_CAPTURE_JPEG_COMPRESS_ERROR = 4
CLOUDSCREEN_CREATE_PTHREAD_ERROR = 5
CLOUDSCREEN_CPU_CONSUMER_ERROR = 6
CLOUDSCREEN_MEDIACODEC_CONFIG_ERROR = 7
CLOUDSCREEN_VIDEO_FPS_UNSUPPORT_ERROR = 8
CLOUDSCREEN_SCREENCAP_OPEN_FAILED = 9
CLOUDSCREEN_SCREENCAP_READ_ERROR = 10
CLOUDSCREEN_SCREENCAP_EOF_ERROR = 11
CLOUDSCREEN_SCREENCAP_FORMAT_ERROR = 12
SCREEN_ORIENTATION_0 = 0
SCREEN_ORIENTATION_90 = 1
SCREEN_ORIENTATION_180 = 2
SCREEN_ORIENTATION_270 = 3
SCREEN_ORIENTATION_UNKNOW = 4
UNKNOWN_SCREEN_CAPTURE_MODE = 0
FULL_SCREEN_CAPTURE_MODE = 1
SCALED_CAPTURE_MODE = 2
DEFAULT_CONFIG_CAPTURE_MODE = 3
GLOBAL_CONFIG_CAPTURE_MODE = 4
PRESET_CONFIG_CAPTURE_MODE = 5
UNKWOWN_SCREEN_CAPTURE_TYPE = 0
JPEG_CAPTURE = 1
RGBA_CAPTURE = 2
UNKOWN_H264VIDEO_FRAME_TYPE = 0
SPS_FRAME = 1
PPS_FRAME = 2
VIDEO_FRAME = 3
_CLOUDSCREENVERSIONRES = _descriptor.Descriptor(name='CloudscreenVersionRes', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenVersionRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='versioncode', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenVersionRes.versioncode', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='version', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenVersionRes.version', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=73, serialized_end=134)
_CLOUDSCREENRESULT = _descriptor.Descriptor(name='CloudscreenResult', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='errorcode', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenResult.errorcode', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='errordesc', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenResult.errordesc', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=136, serialized_end=250)
_DISPLAYDEVICEINFORES = _descriptor.Descriptor(name='DisplayDeviceInfoRes', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='width', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.width', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.height', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fps', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.fps', index=3, number=4, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='density', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.density', index=4, number=5, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='xdpi', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.xdpi', index=5, number=6, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='ydpi', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.ydpi', index=6, number=7, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='orientation', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.orientation', index=7, number=8, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='secure', full_name='com.tencent.wetest.pb.cloudscreen.DisplayDeviceInfoRes.secure', index=8, number=9, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=253, serialized_end=525)
_SCREENCAPTUREREQ = _descriptor.Descriptor(name='ScreenCaptureReq', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='index', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq.index', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='screenCaptureMode', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq.screenCaptureMode', index=1, number=2, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='captureType', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq.captureType', index=2, number=3, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq.height', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='quality', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq.quality', index=4, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='alignment', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureReq.alignment', index=5, number=6, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=528, serialized_end=769)
_SCREENCAPTURERES = _descriptor.Descriptor(name='ScreenCaptureRes', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='index', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.index', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='captureType', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.captureType', index=2, number=3, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='width', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.width', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.height', index=4, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='stride', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.stride', index=5, number=6, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bpp', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.bpp', index=6, number=7, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='orientation', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.orientation', index=7, number=8, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='len', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.len', index=8, number=9, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='datas', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureRes.datas', index=9, number=10, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=772, serialized_end=1059)
_STARTH264VIDEOREQ = _descriptor.Descriptor(name='StartH264VideoReq', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoReq', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='landscape', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoReq.landscape', index=0, number=1, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoReq.height', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bitrate', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoReq.bitrate', index=2, number=3, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='iFrameInterval', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoReq.iFrameInterval', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fps', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoReq.fps', index=4, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1061, serialized_end=1169)
_STARTH264VIDEORES = _descriptor.Descriptor(name='StartH264VideoRes', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='landscape', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes.landscape', index=1, number=3, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='width', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes.width', index=2, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes.height', index=3, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bitrate', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes.bitrate', index=4, number=6, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='iFrameInterval', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes.iFrameInterval', index=5, number=7, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fps', full_name='com.tencent.wetest.pb.cloudscreen.StartH264VideoRes.fps', index=6, number=8, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1172, serialized_end=1365)
_H264CONFIG = _descriptor.Descriptor(name='H264Config', full_name='com.tencent.wetest.pb.cloudscreen.H264Config', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='width', full_name='com.tencent.wetest.pb.cloudscreen.H264Config.width', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.H264Config.height', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1367, serialized_end=1410)
_H264VIDEOFRAMENOTIFY = _descriptor.Descriptor(name='H264VideoFrameNotify', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timestamp', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.timestamp', index=1, number=2, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pts', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.pts', index=2, number=3, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='delay', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.delay', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='orientation', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.orientation', index=4, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pkgSize', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.pkgSize', index=5, number=6, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='datas', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.datas', index=6, number=7, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='frameType', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.frameType', index=7, number=8, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='h264Config', full_name='com.tencent.wetest.pb.cloudscreen.H264VideoFrameNotify.h264Config', index=8, number=9, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1413, serialized_end=1746)
_SCREENCAPTUREPUSHMODEREQ = _descriptor.Descriptor(name='ScreenCapturePushModeReq', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeReq', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeReq.height', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='quality', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeReq.quality', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='minInterval', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeReq.minInterval', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='landscape', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeReq.landscape', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='alignment', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeReq.alignment', index=4, number=5, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1748, serialized_end=1866)
_SCREENCAPTUREPUSHMODERES = _descriptor.Descriptor(name='ScreenCapturePushModeRes', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCapturePushModeRes.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1868, serialized_end=1964)
_SCREENCAPTUREFRAMENOTIFY = _descriptor.Descriptor(name='ScreenCaptureFrameNotify', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='index', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify.index', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='width', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify.width', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='height', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify.height', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='orientation', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify.orientation', index=4, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='len', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify.len', index=5, number=6, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='datas', full_name='com.tencent.wetest.pb.cloudscreen.ScreenCaptureFrameNotify.datas', index=6, number=7, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1967, serialized_end=2158)
_DEVICETIMESTAMPRES = _descriptor.Descriptor(name='DeviceTimestampRes', full_name='com.tencent.wetest.pb.cloudscreen.DeviceTimestampRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='timestamp', full_name='com.tencent.wetest.pb.cloudscreen.DeviceTimestampRes.timestamp', index=0, number=1, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=2160, serialized_end=2199)
_CLOUDSCREENHEADER = _descriptor.Descriptor(name='CloudscreenHeader', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenHeader', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='sequenceId', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenHeader.sequenceId', index=0, number=1, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timestamp', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenHeader.timestamp', index=1, number=2, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='command', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenHeader.command', index=2, number=3, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=2202, serialized_end=2332)
_CLOUDSCREENBODY = _descriptor.Descriptor(name='CloudscreenBody', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='cloudscreenVersionRes', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.cloudscreenVersionRes', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='displayDeviceInfoRes', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.displayDeviceInfoRes', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='screenCaptureReq', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.screenCaptureReq', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='screenCaptureRes', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.screenCaptureRes', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='startH264VideoReq', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.startH264VideoReq', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='startH264VideoRes', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.startH264VideoRes', index=5, number=6, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='h264VideoFrameNotify', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.h264VideoFrameNotify', index=6, number=7, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='screenCapturePushModeReq', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.screenCapturePushModeReq', index=7, number=8, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='screenCapturePushModeRes', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.screenCapturePushModeRes', index=8, number=9, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='screenCaptureFrameNotify', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.screenCaptureFrameNotify', index=9, number=10, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='deviceTimestampRes', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenBody.deviceTimestampRes', index=10, number=11, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=2335, serialized_end=3303)
_CLOUDSCREENPKG = _descriptor.Descriptor(name='CloudscreenPkg', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenPkg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='header', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenPkg.header', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='body', full_name='com.tencent.wetest.pb.cloudscreen.CloudscreenPkg.body', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=3306, serialized_end=3458)
_CLOUDSCREENRESULT.fields_by_name['errorcode'].enum_type = _CLOUDSCREENERRORCODE
_DISPLAYDEVICEINFORES.fields_by_name['result'].message_type = _CLOUDSCREENRESULT
_DISPLAYDEVICEINFORES.fields_by_name['orientation'].enum_type = _SCREENORIENTATION
_SCREENCAPTUREREQ.fields_by_name['screenCaptureMode'].enum_type = _SCREENCAPTUREMODE
_SCREENCAPTUREREQ.fields_by_name['captureType'].enum_type = _SCREENCAPTURETYPE
_SCREENCAPTURERES.fields_by_name['result'].message_type = _CLOUDSCREENRESULT
_SCREENCAPTURERES.fields_by_name['captureType'].enum_type = _SCREENCAPTURETYPE
_STARTH264VIDEORES.fields_by_name['result'].message_type = _CLOUDSCREENRESULT
_H264VIDEOFRAMENOTIFY.fields_by_name['result'].message_type = _CLOUDSCREENRESULT
_H264VIDEOFRAMENOTIFY.fields_by_name['frameType'].enum_type = _H264VIDEOFRAMETYPE
_H264VIDEOFRAMENOTIFY.fields_by_name['h264Config'].message_type = _H264CONFIG
_SCREENCAPTUREPUSHMODERES.fields_by_name['result'].message_type = _CLOUDSCREENRESULT
_SCREENCAPTUREFRAMENOTIFY.fields_by_name['result'].message_type = _CLOUDSCREENRESULT
_CLOUDSCREENHEADER.fields_by_name['command'].enum_type = _CLOUDSCREENCOMMAND
_CLOUDSCREENBODY.fields_by_name['cloudscreenVersionRes'].message_type = _CLOUDSCREENVERSIONRES
_CLOUDSCREENBODY.fields_by_name['displayDeviceInfoRes'].message_type = _DISPLAYDEVICEINFORES
_CLOUDSCREENBODY.fields_by_name['screenCaptureReq'].message_type = _SCREENCAPTUREREQ
_CLOUDSCREENBODY.fields_by_name['screenCaptureRes'].message_type = _SCREENCAPTURERES
_CLOUDSCREENBODY.fields_by_name['startH264VideoReq'].message_type = _STARTH264VIDEOREQ
_CLOUDSCREENBODY.fields_by_name['startH264VideoRes'].message_type = _STARTH264VIDEORES
_CLOUDSCREENBODY.fields_by_name['h264VideoFrameNotify'].message_type = _H264VIDEOFRAMENOTIFY
_CLOUDSCREENBODY.fields_by_name['screenCapturePushModeReq'].message_type = _SCREENCAPTUREPUSHMODEREQ
_CLOUDSCREENBODY.fields_by_name['screenCapturePushModeRes'].message_type = _SCREENCAPTUREPUSHMODERES
_CLOUDSCREENBODY.fields_by_name['screenCaptureFrameNotify'].message_type = _SCREENCAPTUREFRAMENOTIFY
_CLOUDSCREENBODY.fields_by_name['deviceTimestampRes'].message_type = _DEVICETIMESTAMPRES
_CLOUDSCREENPKG.fields_by_name['header'].message_type = _CLOUDSCREENHEADER
_CLOUDSCREENPKG.fields_by_name['body'].message_type = _CLOUDSCREENBODY
DESCRIPTOR.message_types_by_name['CloudscreenVersionRes'] = _CLOUDSCREENVERSIONRES
DESCRIPTOR.message_types_by_name['CloudscreenResult'] = _CLOUDSCREENRESULT
DESCRIPTOR.message_types_by_name['DisplayDeviceInfoRes'] = _DISPLAYDEVICEINFORES
DESCRIPTOR.message_types_by_name['ScreenCaptureReq'] = _SCREENCAPTUREREQ
DESCRIPTOR.message_types_by_name['ScreenCaptureRes'] = _SCREENCAPTURERES
DESCRIPTOR.message_types_by_name['StartH264VideoReq'] = _STARTH264VIDEOREQ
DESCRIPTOR.message_types_by_name['StartH264VideoRes'] = _STARTH264VIDEORES
DESCRIPTOR.message_types_by_name['H264Config'] = _H264CONFIG
DESCRIPTOR.message_types_by_name['H264VideoFrameNotify'] = _H264VIDEOFRAMENOTIFY
DESCRIPTOR.message_types_by_name['ScreenCapturePushModeReq'] = _SCREENCAPTUREPUSHMODEREQ
DESCRIPTOR.message_types_by_name['ScreenCapturePushModeRes'] = _SCREENCAPTUREPUSHMODERES
DESCRIPTOR.message_types_by_name['ScreenCaptureFrameNotify'] = _SCREENCAPTUREFRAMENOTIFY
DESCRIPTOR.message_types_by_name['DeviceTimestampRes'] = _DEVICETIMESTAMPRES
DESCRIPTOR.message_types_by_name['CloudscreenHeader'] = _CLOUDSCREENHEADER
DESCRIPTOR.message_types_by_name['CloudscreenBody'] = _CLOUDSCREENBODY
DESCRIPTOR.message_types_by_name['CloudscreenPkg'] = _CLOUDSCREENPKG
DESCRIPTOR.enum_types_by_name['CloudscreenCommand'] = _CLOUDSCREENCOMMAND
DESCRIPTOR.enum_types_by_name['CloudscreenErrorCode'] = _CLOUDSCREENERRORCODE
DESCRIPTOR.enum_types_by_name['ScreenOrientation'] = _SCREENORIENTATION
DESCRIPTOR.enum_types_by_name['ScreenCaptureMode'] = _SCREENCAPTUREMODE
DESCRIPTOR.enum_types_by_name['ScreenCaptureType'] = _SCREENCAPTURETYPE
DESCRIPTOR.enum_types_by_name['H264VideoFrameType'] = _H264VIDEOFRAMETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
CloudscreenVersionRes = _reflection.GeneratedProtocolMessageType('CloudscreenVersionRes', (_message.Message,), dict(DESCRIPTOR=_CLOUDSCREENVERSIONRES, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(CloudscreenVersionRes)
CloudscreenResult = _reflection.GeneratedProtocolMessageType('CloudscreenResult', (_message.Message,), dict(DESCRIPTOR=_CLOUDSCREENRESULT, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(CloudscreenResult)
DisplayDeviceInfoRes = _reflection.GeneratedProtocolMessageType('DisplayDeviceInfoRes', (_message.Message,), dict(DESCRIPTOR=_DISPLAYDEVICEINFORES, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(DisplayDeviceInfoRes)
ScreenCaptureReq = _reflection.GeneratedProtocolMessageType('ScreenCaptureReq', (_message.Message,), dict(DESCRIPTOR=_SCREENCAPTUREREQ, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(ScreenCaptureReq)
ScreenCaptureRes = _reflection.GeneratedProtocolMessageType('ScreenCaptureRes', (_message.Message,), dict(DESCRIPTOR=_SCREENCAPTURERES, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(ScreenCaptureRes)
StartH264VideoReq = _reflection.GeneratedProtocolMessageType('StartH264VideoReq', (_message.Message,), dict(DESCRIPTOR=_STARTH264VIDEOREQ, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(StartH264VideoReq)
StartH264VideoRes = _reflection.GeneratedProtocolMessageType('StartH264VideoRes', (_message.Message,), dict(DESCRIPTOR=_STARTH264VIDEORES, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(StartH264VideoRes)
H264Config = _reflection.GeneratedProtocolMessageType('H264Config', (_message.Message,), dict(DESCRIPTOR=_H264CONFIG, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(H264Config)
H264VideoFrameNotify = _reflection.GeneratedProtocolMessageType('H264VideoFrameNotify', (_message.Message,), dict(DESCRIPTOR=_H264VIDEOFRAMENOTIFY, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(H264VideoFrameNotify)
ScreenCapturePushModeReq = _reflection.GeneratedProtocolMessageType('ScreenCapturePushModeReq', (_message.Message,), dict(DESCRIPTOR=_SCREENCAPTUREPUSHMODEREQ, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(ScreenCapturePushModeReq)
ScreenCapturePushModeRes = _reflection.GeneratedProtocolMessageType('ScreenCapturePushModeRes', (_message.Message,), dict(DESCRIPTOR=_SCREENCAPTUREPUSHMODERES, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(ScreenCapturePushModeRes)
ScreenCaptureFrameNotify = _reflection.GeneratedProtocolMessageType('ScreenCaptureFrameNotify', (_message.Message,), dict(DESCRIPTOR=_SCREENCAPTUREFRAMENOTIFY, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(ScreenCaptureFrameNotify)
DeviceTimestampRes = _reflection.GeneratedProtocolMessageType('DeviceTimestampRes', (_message.Message,), dict(DESCRIPTOR=_DEVICETIMESTAMPRES, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(DeviceTimestampRes)
CloudscreenHeader = _reflection.GeneratedProtocolMessageType('CloudscreenHeader', (_message.Message,), dict(DESCRIPTOR=_CLOUDSCREENHEADER, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(CloudscreenHeader)
CloudscreenBody = _reflection.GeneratedProtocolMessageType('CloudscreenBody', (_message.Message,), dict(DESCRIPTOR=_CLOUDSCREENBODY, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(CloudscreenBody)
CloudscreenPkg = _reflection.GeneratedProtocolMessageType('CloudscreenPkg', (_message.Message,), dict(DESCRIPTOR=_CLOUDSCREENPKG, __module__='cloudscreen.CloudscreenPkgPB_pb2'))
_sym_db.RegisterMessage(CloudscreenPkg)
DESCRIPTOR._options = None