# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/pb/touch/TouchPkgPB_pb2.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 35131 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='touch/TouchPkgPB.proto', package='com.tencent.wetest.pb.touch', syntax='proto3', serialized_options=_b('\n\x1bcom.tencent.wetest.pb.touchB\nTouchPkgPB'), serialized_pb=_b('\n\x16touch/TouchPkgPB.proto\x12\x1bcom.tencent.wetest.pb.touch"7\n\x0fTouchVersionRes\x12\x13\n\x0bversioncode\x18\x01 \x01(\x05\x12\x0f\n\x07version\x18\x02 \x01(\t"`\n\x0bTouchResult\x12>\n\terrorcode\x18\x01 \x01(\x0e2+.com.tencent.wetest.pb.touch.TouchErrorCode\x12\x11\n\terrordesc\x18\x02 \x01(\t"Í\x02\n\x0fTouchDeviceInfo\x12\x0f\n\x07devpath\x18\x01 \x01(\t\x12\x12\n\ndevicename\x18\x02 \x01(\t\x12\x11\n\thasMTSlot\x18\x03 \x01(\x08\x12\x15\n\rhasTrackingID\x18\x04 \x01(\x08\x12\x13\n\x0bhasBtnTouch\x18\x05 \x01(\x08\x12\x15\n\rhasTouchMajor\x18\x06 \x01(\x08\x12\x15\n\rhasWidthMajor\x18\x07 \x01(\x08\x12\x13\n\x0bhasPressure\x18\x08 \x01(\x08\x12\x13\n\x0bminPressure\x18\t \x01(\x05\x12\x13\n\x0bmaxPressure\x18\n \x01(\x05\x12\x13\n\x0bmaxPostionX\x18\x0b \x01(\x05\x12\x13\n\x0bmaxPostionY\x18\x0c \x01(\x05\x12\x15\n\rmaxTrackingID\x18\r \x01(\x05\x12\x13\n\x0bminPostionX\x18\x0e \x01(\x05\x12\x13\n\x0bminPostionY\x18\x0f \x01(\x05"\x95\x01\n\x12TouchDeviceInitRes\x128\n\x06result\x18\x01 \x01(\x0b2(.com.tencent.wetest.pb.touch.TouchResult\x12E\n\x0ftouchDeviceInfo\x18\x02 \x01(\x0b2,.com.tencent.wetest.pb.touch.TouchDeviceInfo"\x95\x01\n\x12TouchDeviceInfoRes\x128\n\x06result\x18\x01 \x01(\x0b2(.com.tencent.wetest.pb.touch.TouchResult\x12E\n\x0ftouchDeviceInfo\x18\x02 \x01(\x0b2,.com.tencent.wetest.pb.touch.TouchDeviceInfo"\x91\x01\n\nTouchEvent\x129\n\ttouchType\x18\x01 \x01(\x0e2&.com.tencent.wetest.pb.touch.TouchType\x12\x0e\n\x06slotId\x18\x02 \x01(\x05\x12\t\n\x01x\x18\x03 \x01(\x05\x12\t\n\x01y\x18\x04 \x01(\x05\x12\x10\n\x08pressure\x18\x05 \x01(\x05\x12\x10\n\x08waittime\x18\x06 \x01(\x05"P\n\x10TouchEventNotify\x12<\n\x0btouchevents\x18\x01 \x03(\x0b2\'.com.tencent.wetest.pb.touch.TouchEvent"e\n\x10TouchErrorNotify\x12>\n\terrorcode\x18\x01 \x01(\x0e2+.com.tencent.wetest.pb.touch.TouchErrorCode\x12\x11\n\terrordesc\x18\x02 \x01(\t"p\n\x0bTouchHeader\x12\x12\n\nsequenceId\x18\x01 \x01(\x03\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12:\n\x07command\x18\x03 \x01(\x0e2).com.tencent.wetest.pb.touch.TouchCommand"þ\x02\n\tTouchBody\x12E\n\x0ftouchVersionRes\x18\x01 \x01(\x0b2,.com.tencent.wetest.pb.touch.TouchVersionRes\x12K\n\x12touchDeviceInitRes\x18\x02 \x01(\x0b2/.com.tencent.wetest.pb.touch.TouchDeviceInitRes\x12K\n\x12touchDeviceInfoRes\x18\x03 \x01(\x0b2/.com.tencent.wetest.pb.touch.TouchDeviceInfoRes\x12G\n\x10touchEventNotify\x18\x04 \x01(\x0b2-.com.tencent.wetest.pb.touch.TouchEventNotify\x12G\n\x10touchErrorNotify\x18\x05 \x01(\x0b2-.com.tencent.wetest.pb.touch.TouchErrorNotify"z\n\x08TouchPkg\x128\n\x06header\x18\x01 \x01(\x0b2(.com.tencent.wetest.pb.touch.TouchHeader\x124\n\x04body\x18\x02 \x01(\x0b2&.com.tencent.wetest.pb.touch.TouchBody*\x9d\x02\n\x0cTouchCommand\x12\x11\n\rUNKNOWN_TOUCH\x10\x00\x12\x17\n\x13TOUCH_HEARTBEAT_REQ\x10\x01\x12\x17\n\x13TOUCH_HEARTBEAT_RES\x10\x02\x12\x15\n\x11TOUCH_VERSION_REQ\x10\x03\x12\x15\n\x11TOUCH_VERSION_RES\x10\x04\x12\x19\n\x15TOUCH_DEVICE_INIT_REQ\x10\x05\x12\x19\n\x15TOUCH_DEVICE_INIT_RES\x10\x06\x12\x19\n\x15TOUCH_DEVICE_INFO_REQ\x10\x07\x12\x19\n\x15TOUCH_DEVICE_INFO_RES\x10\x08\x12\x16\n\x12TOUCH_EVENT_NOTIFY\x10\t\x12\x16\n\x12TOUCH_ERROR_NOTIFY\x10\n*5\n\x0eTouchErrorCode\x12\x0e\n\nTOUCH_SUCC\x10\x00\x12\x13\n\x0fTOUCH_NO_DEVICE\x10\x01*~\n\tTouchType\x12\x12\n\x0eTOUCH_TOUCH_UP\x10\x00\x12\x14\n\x10TOUCH_TOUCH_DOWN\x10\x01\x12\x14\n\x10TOUCH_TOUCH_MOVE\x10\x02\x12\x10\n\x0cTOUCH_COMMIT\x10\x03\x12\x0f\n\x0bTOUCH_RESET\x10\x04\x12\x0e\n\nTOUCH_WAIT\x10\x05B)\n\x1bcom.tencent.wetest.pb.touchB\nTouchPkgPBb\x06proto3'))
_TOUCHCOMMAND = _descriptor.EnumDescriptor(name='TouchCommand', full_name='com.tencent.wetest.pb.touch.TouchCommand', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='UNKNOWN_TOUCH', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_HEARTBEAT_REQ', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_HEARTBEAT_RES', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_VERSION_REQ', index=3, number=3, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_VERSION_RES', index=4, number=4, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_DEVICE_INIT_REQ', index=5, number=5, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_DEVICE_INIT_RES', index=6, number=6, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_DEVICE_INFO_REQ', index=7, number=7, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_DEVICE_INFO_RES', index=8, number=8, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_EVENT_NOTIFY', index=9, number=9, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_ERROR_NOTIFY', index=10, number=10, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=1807, serialized_end=2092)
_sym_db.RegisterEnumDescriptor(_TOUCHCOMMAND)
TouchCommand = enum_type_wrapper.EnumTypeWrapper(_TOUCHCOMMAND)
_TOUCHERRORCODE = _descriptor.EnumDescriptor(name='TouchErrorCode', full_name='com.tencent.wetest.pb.touch.TouchErrorCode', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='TOUCH_SUCC', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_NO_DEVICE', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=2094, serialized_end=2147)
_sym_db.RegisterEnumDescriptor(_TOUCHERRORCODE)
TouchErrorCode = enum_type_wrapper.EnumTypeWrapper(_TOUCHERRORCODE)
_TOUCHTYPE = _descriptor.EnumDescriptor(name='TouchType', full_name='com.tencent.wetest.pb.touch.TouchType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='TOUCH_TOUCH_UP', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_TOUCH_DOWN', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_TOUCH_MOVE', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_COMMIT', index=3, number=3, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_RESET', index=4, number=4, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TOUCH_WAIT', index=5, number=5, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=2149, serialized_end=2275)
_sym_db.RegisterEnumDescriptor(_TOUCHTYPE)
TouchType = enum_type_wrapper.EnumTypeWrapper(_TOUCHTYPE)
UNKNOWN_TOUCH = 0
TOUCH_HEARTBEAT_REQ = 1
TOUCH_HEARTBEAT_RES = 2
TOUCH_VERSION_REQ = 3
TOUCH_VERSION_RES = 4
TOUCH_DEVICE_INIT_REQ = 5
TOUCH_DEVICE_INIT_RES = 6
TOUCH_DEVICE_INFO_REQ = 7
TOUCH_DEVICE_INFO_RES = 8
TOUCH_EVENT_NOTIFY = 9
TOUCH_ERROR_NOTIFY = 10
TOUCH_SUCC = 0
TOUCH_NO_DEVICE = 1
TOUCH_TOUCH_UP = 0
TOUCH_TOUCH_DOWN = 1
TOUCH_TOUCH_MOVE = 2
TOUCH_COMMIT = 3
TOUCH_RESET = 4
TOUCH_WAIT = 5
_TOUCHVERSIONRES = _descriptor.Descriptor(name='TouchVersionRes', full_name='com.tencent.wetest.pb.touch.TouchVersionRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='versioncode', full_name='com.tencent.wetest.pb.touch.TouchVersionRes.versioncode', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='version', full_name='com.tencent.wetest.pb.touch.TouchVersionRes.version', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=55, serialized_end=110)
_TOUCHRESULT = _descriptor.Descriptor(name='TouchResult', full_name='com.tencent.wetest.pb.touch.TouchResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='errorcode', full_name='com.tencent.wetest.pb.touch.TouchResult.errorcode', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='errordesc', full_name='com.tencent.wetest.pb.touch.TouchResult.errordesc', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=112, serialized_end=208)
_TOUCHDEVICEINFO = _descriptor.Descriptor(name='TouchDeviceInfo', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='devpath', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.devpath', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='devicename', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.devicename', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='hasMTSlot', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.hasMTSlot', index=2, number=3, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='hasTrackingID', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.hasTrackingID', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='hasBtnTouch', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.hasBtnTouch', index=4, number=5, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='hasTouchMajor', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.hasTouchMajor', index=5, number=6, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='hasWidthMajor', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.hasWidthMajor', index=6, number=7, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='hasPressure', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.hasPressure', index=7, number=8, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='minPressure', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.minPressure', index=8, number=9, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='maxPressure', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.maxPressure', index=9, number=10, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='maxPostionX', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.maxPostionX', index=10, number=11, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='maxPostionY', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.maxPostionY', index=11, number=12, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='maxTrackingID', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.maxTrackingID', index=12, number=13, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='minPostionX', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.minPostionX', index=13, number=14, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='minPostionY', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfo.minPostionY', index=14, number=15, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=211, serialized_end=544)
_TOUCHDEVICEINITRES = _descriptor.Descriptor(name='TouchDeviceInitRes', full_name='com.tencent.wetest.pb.touch.TouchDeviceInitRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.touch.TouchDeviceInitRes.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='touchDeviceInfo', full_name='com.tencent.wetest.pb.touch.TouchDeviceInitRes.touchDeviceInfo', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=547, serialized_end=696)
_TOUCHDEVICEINFORES = _descriptor.Descriptor(name='TouchDeviceInfoRes', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfoRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfoRes.result', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='touchDeviceInfo', full_name='com.tencent.wetest.pb.touch.TouchDeviceInfoRes.touchDeviceInfo', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=699, serialized_end=848)
_TOUCHEVENT = _descriptor.Descriptor(name='TouchEvent', full_name='com.tencent.wetest.pb.touch.TouchEvent', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='touchType', full_name='com.tencent.wetest.pb.touch.TouchEvent.touchType', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='slotId', full_name='com.tencent.wetest.pb.touch.TouchEvent.slotId', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='x', full_name='com.tencent.wetest.pb.touch.TouchEvent.x', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='y', full_name='com.tencent.wetest.pb.touch.TouchEvent.y', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pressure', full_name='com.tencent.wetest.pb.touch.TouchEvent.pressure', index=4, number=5, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='waittime', full_name='com.tencent.wetest.pb.touch.TouchEvent.waittime', index=5, number=6, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=851, serialized_end=996)
_TOUCHEVENTNOTIFY = _descriptor.Descriptor(name='TouchEventNotify', full_name='com.tencent.wetest.pb.touch.TouchEventNotify', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='touchevents', full_name='com.tencent.wetest.pb.touch.TouchEventNotify.touchevents', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=998, serialized_end=1078)
_TOUCHERRORNOTIFY = _descriptor.Descriptor(name='TouchErrorNotify', full_name='com.tencent.wetest.pb.touch.TouchErrorNotify', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='errorcode', full_name='com.tencent.wetest.pb.touch.TouchErrorNotify.errorcode', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='errordesc', full_name='com.tencent.wetest.pb.touch.TouchErrorNotify.errordesc', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1080, serialized_end=1181)
_TOUCHHEADER = _descriptor.Descriptor(name='TouchHeader', full_name='com.tencent.wetest.pb.touch.TouchHeader', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='sequenceId', full_name='com.tencent.wetest.pb.touch.TouchHeader.sequenceId', index=0, number=1, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timestamp', full_name='com.tencent.wetest.pb.touch.TouchHeader.timestamp', index=1, number=2, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='command', full_name='com.tencent.wetest.pb.touch.TouchHeader.command', index=2, number=3, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1183, serialized_end=1295)
_TOUCHBODY = _descriptor.Descriptor(name='TouchBody', full_name='com.tencent.wetest.pb.touch.TouchBody', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='touchVersionRes', full_name='com.tencent.wetest.pb.touch.TouchBody.touchVersionRes', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='touchDeviceInitRes', full_name='com.tencent.wetest.pb.touch.TouchBody.touchDeviceInitRes', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='touchDeviceInfoRes', full_name='com.tencent.wetest.pb.touch.TouchBody.touchDeviceInfoRes', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='touchEventNotify', full_name='com.tencent.wetest.pb.touch.TouchBody.touchEventNotify', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='touchErrorNotify', full_name='com.tencent.wetest.pb.touch.TouchBody.touchErrorNotify', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1298, serialized_end=1680)
_TOUCHPKG = _descriptor.Descriptor(name='TouchPkg', full_name='com.tencent.wetest.pb.touch.TouchPkg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='header', full_name='com.tencent.wetest.pb.touch.TouchPkg.header', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='body', full_name='com.tencent.wetest.pb.touch.TouchPkg.body', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1682, serialized_end=1804)
_TOUCHRESULT.fields_by_name['errorcode'].enum_type = _TOUCHERRORCODE
_TOUCHDEVICEINITRES.fields_by_name['result'].message_type = _TOUCHRESULT
_TOUCHDEVICEINITRES.fields_by_name['touchDeviceInfo'].message_type = _TOUCHDEVICEINFO
_TOUCHDEVICEINFORES.fields_by_name['result'].message_type = _TOUCHRESULT
_TOUCHDEVICEINFORES.fields_by_name['touchDeviceInfo'].message_type = _TOUCHDEVICEINFO
_TOUCHEVENT.fields_by_name['touchType'].enum_type = _TOUCHTYPE
_TOUCHEVENTNOTIFY.fields_by_name['touchevents'].message_type = _TOUCHEVENT
_TOUCHERRORNOTIFY.fields_by_name['errorcode'].enum_type = _TOUCHERRORCODE
_TOUCHHEADER.fields_by_name['command'].enum_type = _TOUCHCOMMAND
_TOUCHBODY.fields_by_name['touchVersionRes'].message_type = _TOUCHVERSIONRES
_TOUCHBODY.fields_by_name['touchDeviceInitRes'].message_type = _TOUCHDEVICEINITRES
_TOUCHBODY.fields_by_name['touchDeviceInfoRes'].message_type = _TOUCHDEVICEINFORES
_TOUCHBODY.fields_by_name['touchEventNotify'].message_type = _TOUCHEVENTNOTIFY
_TOUCHBODY.fields_by_name['touchErrorNotify'].message_type = _TOUCHERRORNOTIFY
_TOUCHPKG.fields_by_name['header'].message_type = _TOUCHHEADER
_TOUCHPKG.fields_by_name['body'].message_type = _TOUCHBODY
DESCRIPTOR.message_types_by_name['TouchVersionRes'] = _TOUCHVERSIONRES
DESCRIPTOR.message_types_by_name['TouchResult'] = _TOUCHRESULT
DESCRIPTOR.message_types_by_name['TouchDeviceInfo'] = _TOUCHDEVICEINFO
DESCRIPTOR.message_types_by_name['TouchDeviceInitRes'] = _TOUCHDEVICEINITRES
DESCRIPTOR.message_types_by_name['TouchDeviceInfoRes'] = _TOUCHDEVICEINFORES
DESCRIPTOR.message_types_by_name['TouchEvent'] = _TOUCHEVENT
DESCRIPTOR.message_types_by_name['TouchEventNotify'] = _TOUCHEVENTNOTIFY
DESCRIPTOR.message_types_by_name['TouchErrorNotify'] = _TOUCHERRORNOTIFY
DESCRIPTOR.message_types_by_name['TouchHeader'] = _TOUCHHEADER
DESCRIPTOR.message_types_by_name['TouchBody'] = _TOUCHBODY
DESCRIPTOR.message_types_by_name['TouchPkg'] = _TOUCHPKG
DESCRIPTOR.enum_types_by_name['TouchCommand'] = _TOUCHCOMMAND
DESCRIPTOR.enum_types_by_name['TouchErrorCode'] = _TOUCHERRORCODE
DESCRIPTOR.enum_types_by_name['TouchType'] = _TOUCHTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TouchVersionRes = _reflection.GeneratedProtocolMessageType('TouchVersionRes', (_message.Message,), dict(DESCRIPTOR=_TOUCHVERSIONRES, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchVersionRes)
TouchResult = _reflection.GeneratedProtocolMessageType('TouchResult', (_message.Message,), dict(DESCRIPTOR=_TOUCHRESULT, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchResult)
TouchDeviceInfo = _reflection.GeneratedProtocolMessageType('TouchDeviceInfo', (_message.Message,), dict(DESCRIPTOR=_TOUCHDEVICEINFO, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchDeviceInfo)
TouchDeviceInitRes = _reflection.GeneratedProtocolMessageType('TouchDeviceInitRes', (_message.Message,), dict(DESCRIPTOR=_TOUCHDEVICEINITRES, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchDeviceInitRes)
TouchDeviceInfoRes = _reflection.GeneratedProtocolMessageType('TouchDeviceInfoRes', (_message.Message,), dict(DESCRIPTOR=_TOUCHDEVICEINFORES, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchDeviceInfoRes)
TouchEvent = _reflection.GeneratedProtocolMessageType('TouchEvent', (_message.Message,), dict(DESCRIPTOR=_TOUCHEVENT, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchEvent)
TouchEventNotify = _reflection.GeneratedProtocolMessageType('TouchEventNotify', (_message.Message,), dict(DESCRIPTOR=_TOUCHEVENTNOTIFY, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchEventNotify)
TouchErrorNotify = _reflection.GeneratedProtocolMessageType('TouchErrorNotify', (_message.Message,), dict(DESCRIPTOR=_TOUCHERRORNOTIFY, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchErrorNotify)
TouchHeader = _reflection.GeneratedProtocolMessageType('TouchHeader', (_message.Message,), dict(DESCRIPTOR=_TOUCHHEADER, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchHeader)
TouchBody = _reflection.GeneratedProtocolMessageType('TouchBody', (_message.Message,), dict(DESCRIPTOR=_TOUCHBODY, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchBody)
TouchPkg = _reflection.GeneratedProtocolMessageType('TouchPkg', (_message.Message,), dict(DESCRIPTOR=_TOUCHPKG, __module__='touch.TouchPkgPB_pb2'))
_sym_db.RegisterMessage(TouchPkg)
DESCRIPTOR._options = None