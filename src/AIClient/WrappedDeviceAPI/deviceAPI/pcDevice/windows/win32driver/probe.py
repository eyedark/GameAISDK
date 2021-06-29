# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/pcDevice/windows/win32driver/probe.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 11465 bytes
"""
探测实现
"""
import time, re, pythoncom, win32gui, win32con, win32api, win32process, locale, ctypes
MAX_DEPTH = 'MAXDEPTH'
INSTANCE = 'INSTANCE'
os_encoding = locale.getdefaultlocale(None)[1]

def set_foreground_window(hwnd):
    fwnd = win32gui.GetForegroundWindow()
    if fwnd == hwnd:
        return
    if fwnd == 0:
        try:
            win32gui.SetForegroundWindow(hwnd)
            return
        except win32api.error:
            return

    ftid, _ = win32process.GetWindowThreadProcessId(fwnd)
    wtid, _ = win32process.GetWindowThreadProcessId(hwnd)
    ctypes.windll.user32.AttachThreadInput(wtid, ftid, True)
    st = time.time()
    while time.time() - st < 5:
        if win32gui.GetForegroundWindow() == hwnd:
            break
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)

    ctypes.windll.user32.AttachThreadInput(wtid, ftid, False)


class Win32Probe(object):

    def wait_for_element(self, locator, root=None, timeOut=20):
        st = time.time()
        while time.time() - st < timeOut:
            eles = self.search_element(locator, root)
            if eles:
                return eles
            time.sleep(0.5)

    def search_element(self, locator=None, root=None):
        if root is None:
            root = win32gui.GetDesktopWindow()
        if isinstance(root, int):
            pass
        else:
            if hasattr(root, 'Id'):
                root = getattr(root, 'Id')
            else:
                raise TypeError('root type(%s) not support!' % type(root))
            if not win32gui.IsWindow(root):
                raise ValueError('Window(%s) is not valid' % root)
            if locator is None:
                return [root]
            if not hasattr(locator, 'loads'):
                raise TypeError('type(%s) not supported' % type(locator))
            qpath = locator.loads()
            foundCtrls, _ = self._recursive_find(root, qpath)
        return foundCtrls

    def _match_control(self, control, props):
        """控件是否匹配给定的属性
        
        :param control: 控件
        :param props: 要匹配的控件属性字典，如{'classname':['=', 'window']}
        """
        for propname in props:
            try:
                act_prop_value = self.get_property(control, propname)
            except pythoncom.com_error as e:
                return False
            except win32gui.error as e:
                if e.winerror == 1400:
                    return False
                raise e

            operator, exp_prop_value = props[propname]
            if act_prop_value is None:
                return False
            if isinstance(act_prop_value, bool):
                if act_prop_value != bool(exp_prop_value):
                    return False
            else:
                if isinstance(act_prop_value, int):
                    if re.search('^0x', exp_prop_value) != None:
                        exp_prop_value = int(exp_prop_value, 16)
                    else:
                        exp_prop_value = int(exp_prop_value)
                    if act_prop_value != exp_prop_value:
                        return False
                else:
                    if isinstance(exp_prop_value, str):
                        isMatched = False
                        if operator == '=':
                            isMatched = act_prop_value == exp_prop_value
                        else:
                            isMatched = re.search(exp_prop_value, act_prop_value) and True or False
                        if not isMatched:
                            return False
                    else:
                        raise Exception('不支持控件属性值类型：%s' % type(act_prop_value))

        return True

    @staticmethod
    def __enum_childwin_callback(hwnd, hwnds):
        parent = hwnds[0]
        if parent == None:
            hwnds.append(hwnd)
        else:
            hparent = ctypes.windll.user32.GetAncestor(hwnd, win32con.GA_PARENT)
        if hparent == parent:
            hwnds.append(hwnd)

    def __get_children(self, hwnd):
        hwnds = []
        if hwnd == win32gui.GetDesktopWindow():
            hwnds.append(None)
            win32gui.EnumWindows(self._Win32Probe__enum_childwin_callback, hwnds)
        else:
            hwnds.append(hwnd)
        try:
            win32gui.EnumChildWindows(hwnd, self._Win32Probe__enum_childwin_callback, hwnds)
        except win32gui.error as e:
            if e.winerror == 0 or e.winerror == 1400:
                pass
            else:
                raise e

        del hwnds[0]
        return hwnds

    def _recursive_find(self, root, qpath):
        """递归查找控件
        
        :param root: 根控件
        :param qpath: 解析后的qpath结构
        :return: 返回(found_controls, remain_qpath)， 其中found_controls是找到的控件，remain_qpath
        是未能找到控件时剩下的未能匹配的qpath。
        """
        qpath = qpath[:]
        props = qpath[0]
        props = dict((entry[0].upper(), entry[1]) for entry in list(props.items()))
        max_depth = 1
        if MAX_DEPTH in props:
            max_depth = int(props[MAX_DEPTH][1])
            if max_depth <= 0:
                raise Exception('MaxDepth=%s应该>=1' % max_depth)
            del props[MAX_DEPTH]
        instance = None
        if INSTANCE in props:
            instance = int(props[INSTANCE][1])
            del props[INSTANCE]
        children = self._Win32Probe__get_children(root)
        found_child_controls = []
        for ctrl in children:
            if self._match_control(ctrl, props):
                found_child_controls.append(ctrl)
            if max_depth > 1:
                props_copy = props.copy()
                props_copy[MAX_DEPTH] = ['=', str(max_depth - 1)]
                _controls, _ = self._recursive_find(ctrl, [props_copy])
                found_child_controls += _controls

        if not found_child_controls:
            return ([], qpath)
        else:
            if instance != None:
                try:
                    found_child_controls = [
                     found_child_controls[instance]]
                except IndexError:
                    return ([], qpath)

            qpath.pop(0)
            if not qpath:
                return (
                 found_child_controls, qpath)
            found_ctrls = []
            error_path = qpath
            for root in found_child_controls:
                ctrls, remain_qpath = self._recursive_find(root, qpath)
                found_ctrls += ctrls
                if len(remain_qpath) < len(error_path):
                    error_path = remain_qpath

            return (
             found_ctrls, error_path)

    def set_property(self, element, propertyName, value):
        validProperties = ['TEXT', 'FOCUS', 'ACTIVE']
        name = propertyName.upper()
        if name not in validProperties:
            raise ValueError('%s not supported!' % name)
        if name == 'FOCUS' and value == True:
            current_id = win32api.GetCurrentThreadId()
            target_id = win32process.GetWindowThreadProcessId(element)[0]
            win32process.AttachThreadInput(target_id, current_id, True)
            win32gui.SetFocus(element)
            win32process.AttachThreadInput(target_id, current_id, False)
        else:
            if name == 'TEXT':
                pass
            elif name == 'active' and value == True:
                fwnd = win32gui.GetForegroundWindow()
                if fwnd == element:
                    return
                if fwnd == 0:
                    try:
                        win32gui.SetForegroundWindow(element)
                        return
                    except win32api.error:
                        Keyboard.inputKeys('{ESC}')
                        win32gui.SetForegroundWindow(element)
                        return

                    ftid, _ = win32process.GetWindowThreadProcessId(fwnd)
                    wtid, _ = win32process.GetWindowThreadProcessId(element)
                    ctypes.windll.user32.AttachThreadInput(wtid, ftid, True)
                    st = time.time()
                    while time.time() - st < 5:
                        if win32gui.GetForegroundWindow() == element:
                            break
                        ctypes.windll.user32.SetForegroundWindow(element)
                        time.sleep(0.5)

                    ctypes.windll.user32.AttachThreadInput(wtid, ftid, False)

    def __encode_locale(self, s, encoding='utf-8'):
        try:
            return s.decode(os_encoding).encode(encoding)
        except UnicodeDecodeError:
            return s
        except AttributeError:
            return s

    def __get_text(self, hwnd):
        buf_size = 0
        try:
            textlength = ctypes.c_long(0)
            hr = ctypes.windll.user32.SendMessageTimeoutA(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0, 0, 200, ctypes.byref(textlength))
            if hr == 0 or textlength.value < 0:
                return ''
            buf_size = textlength.value * 2 + 1
        except win32gui.error:
            return ''

        if buf_size <= 0:
            return ''
        else:
            pybuffer = win32gui.PyMakeBuffer(buf_size)
            ret = win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, pybuffer)
            if ret:
                address, length = win32gui.PyGetBufferAddressAndLen(pybuffer)
                text = win32gui.PyGetString(address, ret)
                return text
            return ''

    def get_property(self, element, propertyName):
        validProperties = ['TEXT', 'TYPE', 'CLASSNAME', 'VISIBLE', 'RECT', 'TOPLEVELWINDOW', 'ACTIVE']
        name = propertyName.upper()
        if name not in validProperties:
            raise ValueError('%s not supported!' % name)
        if not win32gui.IsWindow(element):
            return
            raise Exception('element(%s) is not valid!' % element)
        if name == 'TEXT':
            return self._Win32Probe__get_text(element)
        if name in ('CLASSNAME', 'TYPE'):
            return self._Win32Probe__encode_locale(win32gui.GetClassName(element))
        if name == 'VISIBLE':
            return win32gui.IsWindowVisible(element) == 1
        if name == 'RECT':
            return win32gui.GetWindowRect(element)
        if name == 'TOPLEVELWINDOW':
            style = win32gui.GetWindowLong(element, win32con.GWL_STYLE)
            if style & win32con.WS_CHILDWINDOW == 0:
                return element
            if element == win32gui.GetDesktopWindow():
                return
            parent = element
            while style & win32con.WS_CHILDWINDOW > 0:
                parent = win32gui.GetParent(parent)
                style = win32gui.GetWindowLong(parent, win32con.GWL_STYLE)

            return parent