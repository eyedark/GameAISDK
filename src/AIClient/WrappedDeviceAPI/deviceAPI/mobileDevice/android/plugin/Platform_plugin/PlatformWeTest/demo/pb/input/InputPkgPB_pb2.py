# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/mobileDevice/android/plugin/Platform_plugin/PlatformWeTest/demo/pb/input/InputPkgPB_pb2.py
# Compiled at: 2020-12-29 09:26:44
# Size of source mod 2**32: 19130 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='input/InputPkgPB.proto', package='com.tencent.wetest.pb.input', syntax='proto3', serialized_options=_b('\n\x1bcom.tencent.wetest.pb.inputB\nInputPkgPB'), serialized_pb=_b('\n\x16input/InputPkgPB.proto\x12\x1bcom.tencent.wetest.pb.input"7\n\x0fInputVersionRes\x12\x13\n\x0bversioncode\x18\x01 \x01(\x05\x12\x0f\n\x07version\x18\x02 \x01(\t"G\n\x0eKeyEventNotify\x12\x0f\n\x07keyCode\x18\x01 \x01(\x05\x12\x11\n\tmetaState\x18\x02 \x01(\x05\x12\x11\n\tlongpress\x18\x03 \x01(\x08"\x1f\n\x0fTextEventNotify\x12\x0c\n\x04text\x18\x01 \x01(\t"\x82\x01\n\x15InputTouchEventNotify\x12\x0e\n\x06slotId\x18\x01 \x01(\x05\x12C\n\x0einputTouchType\x18\x02 \x01(\x0e2+.com.tencent.wetest.pb.input.InputTouchType\x12\t\n\x01x\x18\x03 \x01(\x05\x12\t\n\x01y\x18\x04 \x01(\x05"p\n\x0bInputHeader\x12\x12\n\nsequenceId\x18\x01 \x01(\x03\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12:\n\x07command\x18\x03 \x01(\x0e2).com.tencent.wetest.pb.input.InputCommand"±\x02\n\tInputBody\x12E\n\x0finputVersionRes\x18\x01 \x01(\x0b2,.com.tencent.wetest.pb.input.InputVersionRes\x12C\n\x0ekeyEventNotify\x18\x02 \x01(\x0b2+.com.tencent.wetest.pb.input.KeyEventNotify\x12E\n\x0ftextEventNotify\x18\x03 \x01(\x0b2,.com.tencent.wetest.pb.input.TextEventNotify\x12Q\n\x15inputTouchEventNotify\x18\x04 \x01(\x0b22.com.tencent.wetest.pb.input.InputTouchEventNotify"z\n\x08InputPkg\x128\n\x06header\x18\x01 \x01(\x0b2(.com.tencent.wetest.pb.input.InputHeader\x124\n\x04body\x18\x02 \x01(\x0b2&.com.tencent.wetest.pb.input.InputBody*ä\x01\n\x0cInputCommand\x12\x11\n\rUNKNOWN_INPUT\x10\x00\x12\x17\n\x13INPUT_HEARTBEAT_REQ\x10\x01\x12\x17\n\x13INPUT_HEARTBEAT_RES\x10\x02\x12\x15\n\x11INPUT_VERSION_REQ\x10\x03\x12\x15\n\x11INPUT_VERSION_RES\x10\x04\x12\x14\n\x10KEY_EVENT_NOTIFY\x10\x05\x12\x15\n\x11TEXT_EVENT_NOTIFY\x10\x06\x12\x1c\n\x18INPUT_TOUCH_EVENT_NOTIFY\x10\x07\x12\x16\n\x12INJECT_DENY_NOTIFY\x10\x08*P\n\x0eInputTouchType\x12\x12\n\x0eINPUT_TOUCH_UP\x10\x00\x12\x14\n\x10INPUT_TOUCH_DOWN\x10\x01\x12\x14\n\x10INPUT_TOUCH_MOVE\x10\x02B)\n\x1bcom.tencent.wetest.pb.inputB\nInputPkgPBb\x06proto3'))
_INPUTCOMMAND = _descriptor.EnumDescriptor(name='InputCommand', full_name='com.tencent.wetest.pb.input.InputCommand', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='UNKNOWN_INPUT', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INPUT_HEARTBEAT_REQ', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INPUT_HEARTBEAT_RES', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INPUT_VERSION_REQ', index=3, number=3, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INPUT_VERSION_RES', index=4, number=4, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='KEY_EVENT_NOTIFY', index=5, number=5, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TEXT_EVENT_NOTIFY', index=6, number=6, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INPUT_TOUCH_EVENT_NOTIFY', index=7, number=7, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INJECT_DENY_NOTIFY', index=8, number=8, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=898, serialized_end=1126)
_sym_db.RegisterEnumDescriptor(_INPUTCOMMAND)
InputCommand = enum_type_wrapper.EnumTypeWrapper(_INPUTCOMMAND)
_INPUTTOUCHTYPE = _descriptor.EnumDescriptor(name='InputTouchType', full_name='com.tencent.wetest.pb.input.InputTouchType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='INPUT_TOUCH_UP', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INPUT_TOUCH_DOWN', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INPUT_TOUCH_MOVE', index=2, number=2, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=1128, serialized_end=1208)
_sym_db.RegisterEnumDescriptor(_INPUTTOUCHTYPE)
InputTouchType = enum_type_wrapper.EnumTypeWrapper(_INPUTTOUCHTYPE)
UNKNOWN_INPUT = 0
INPUT_HEARTBEAT_REQ = 1
INPUT_HEARTBEAT_RES = 2
INPUT_VERSION_REQ = 3
INPUT_VERSION_RES = 4
KEY_EVENT_NOTIFY = 5
TEXT_EVENT_NOTIFY = 6
INPUT_TOUCH_EVENT_NOTIFY = 7
INJECT_DENY_NOTIFY = 8
INPUT_TOUCH_UP = 0
INPUT_TOUCH_DOWN = 1
INPUT_TOUCH_MOVE = 2
_INPUTVERSIONRES = _descriptor.Descriptor(name='InputVersionRes', full_name='com.tencent.wetest.pb.input.InputVersionRes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='versioncode', full_name='com.tencent.wetest.pb.input.InputVersionRes.versioncode', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='version', full_name='com.tencent.wetest.pb.input.InputVersionRes.version', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=55, serialized_end=110)
_KEYEVENTNOTIFY = _descriptor.Descriptor(name='KeyEventNotify', full_name='com.tencent.wetest.pb.input.KeyEventNotify', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='keyCode', full_name='com.tencent.wetest.pb.input.KeyEventNotify.keyCode', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='metaState', full_name='com.tencent.wetest.pb.input.KeyEventNotify.metaState', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='longpress', full_name='com.tencent.wetest.pb.input.KeyEventNotify.longpress', index=2, number=3, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=112, serialized_end=183)
_TEXTEVENTNOTIFY = _descriptor.Descriptor(name='TextEventNotify', full_name='com.tencent.wetest.pb.input.TextEventNotify', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='text', full_name='com.tencent.wetest.pb.input.TextEventNotify.text', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=185, serialized_end=216)
_INPUTTOUCHEVENTNOTIFY = _descriptor.Descriptor(name='InputTouchEventNotify', full_name='com.tencent.wetest.pb.input.InputTouchEventNotify', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='slotId', full_name='com.tencent.wetest.pb.input.InputTouchEventNotify.slotId', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='inputTouchType', full_name='com.tencent.wetest.pb.input.InputTouchEventNotify.inputTouchType', index=1, number=2, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='x', full_name='com.tencent.wetest.pb.input.InputTouchEventNotify.x', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='y', full_name='com.tencent.wetest.pb.input.InputTouchEventNotify.y', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=219, serialized_end=349)
_INPUTHEADER = _descriptor.Descriptor(name='InputHeader', full_name='com.tencent.wetest.pb.input.InputHeader', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='sequenceId', full_name='com.tencent.wetest.pb.input.InputHeader.sequenceId', index=0, number=1, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timestamp', full_name='com.tencent.wetest.pb.input.InputHeader.timestamp', index=1, number=2, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='command', full_name='com.tencent.wetest.pb.input.InputHeader.command', index=2, number=3, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=351, serialized_end=463)
_INPUTBODY = _descriptor.Descriptor(name='InputBody', full_name='com.tencent.wetest.pb.input.InputBody', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='inputVersionRes', full_name='com.tencent.wetest.pb.input.InputBody.inputVersionRes', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='keyEventNotify', full_name='com.tencent.wetest.pb.input.InputBody.keyEventNotify', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='textEventNotify', full_name='com.tencent.wetest.pb.input.InputBody.textEventNotify', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='inputTouchEventNotify', full_name='com.tencent.wetest.pb.input.InputBody.inputTouchEventNotify', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=466, serialized_end=771)
_INPUTPKG = _descriptor.Descriptor(name='InputPkg', full_name='com.tencent.wetest.pb.input.InputPkg', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='header', full_name='com.tencent.wetest.pb.input.InputPkg.header', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='body', full_name='com.tencent.wetest.pb.input.InputPkg.body', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=773, serialized_end=895)
_INPUTTOUCHEVENTNOTIFY.fields_by_name['inputTouchType'].enum_type = _INPUTTOUCHTYPE
_INPUTHEADER.fields_by_name['command'].enum_type = _INPUTCOMMAND
_INPUTBODY.fields_by_name['inputVersionRes'].message_type = _INPUTVERSIONRES
_INPUTBODY.fields_by_name['keyEventNotify'].message_type = _KEYEVENTNOTIFY
_INPUTBODY.fields_by_name['textEventNotify'].message_type = _TEXTEVENTNOTIFY
_INPUTBODY.fields_by_name['inputTouchEventNotify'].message_type = _INPUTTOUCHEVENTNOTIFY
_INPUTPKG.fields_by_name['header'].message_type = _INPUTHEADER
_INPUTPKG.fields_by_name['body'].message_type = _INPUTBODY
DESCRIPTOR.message_types_by_name['InputVersionRes'] = _INPUTVERSIONRES
DESCRIPTOR.message_types_by_name['KeyEventNotify'] = _KEYEVENTNOTIFY
DESCRIPTOR.message_types_by_name['TextEventNotify'] = _TEXTEVENTNOTIFY
DESCRIPTOR.message_types_by_name['InputTouchEventNotify'] = _INPUTTOUCHEVENTNOTIFY
DESCRIPTOR.message_types_by_name['InputHeader'] = _INPUTHEADER
DESCRIPTOR.message_types_by_name['InputBody'] = _INPUTBODY
DESCRIPTOR.message_types_by_name['InputPkg'] = _INPUTPKG
DESCRIPTOR.enum_types_by_name['InputCommand'] = _INPUTCOMMAND
DESCRIPTOR.enum_types_by_name['InputTouchType'] = _INPUTTOUCHTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
InputVersionRes = _reflection.GeneratedProtocolMessageType('InputVersionRes', (_message.Message,), dict(DESCRIPTOR=_INPUTVERSIONRES, __module__='input.InputPkgPB_pb2'))
_sym_db.RegisterMessage(InputVersionRes)
KeyEventNotify = _reflection.GeneratedProtocolMessageType('KeyEventNotify', (_message.Message,), dict(DESCRIPTOR=_KEYEVENTNOTIFY, __module__='input.InputPkgPB_pb2'))
_sym_db.RegisterMessage(KeyEventNotify)
TextEventNotify = _reflection.GeneratedProtocolMessageType('TextEventNotify', (_message.Message,), dict(DESCRIPTOR=_TEXTEVENTNOTIFY, __module__='input.InputPkgPB_pb2'))
_sym_db.RegisterMessage(TextEventNotify)
InputTouchEventNotify = _reflection.GeneratedProtocolMessageType('InputTouchEventNotify', (_message.Message,), dict(DESCRIPTOR=_INPUTTOUCHEVENTNOTIFY, __module__='input.InputPkgPB_pb2'))
_sym_db.RegisterMessage(InputTouchEventNotify)
InputHeader = _reflection.GeneratedProtocolMessageType('InputHeader', (_message.Message,), dict(DESCRIPTOR=_INPUTHEADER, __module__='input.InputPkgPB_pb2'))
_sym_db.RegisterMessage(InputHeader)
InputBody = _reflection.GeneratedProtocolMessageType('InputBody', (_message.Message,), dict(DESCRIPTOR=_INPUTBODY, __module__='input.InputPkgPB_pb2'))
_sym_db.RegisterMessage(InputBody)
InputPkg = _reflection.GeneratedProtocolMessageType('InputPkg', (_message.Message,), dict(DESCRIPTOR=_INPUTPKG, __module__='input.InputPkgPB_pb2'))
_sym_db.RegisterMessage(InputPkg)
DESCRIPTOR._options = None