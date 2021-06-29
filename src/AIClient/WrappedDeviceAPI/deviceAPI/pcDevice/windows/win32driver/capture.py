# -*- coding: utf-8 -*-
# uncompyle6 version 3.7.5.dev0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.10 (default, Apr 15 2021, 13:44:35) 
# [GCC 9.3.0]
# Embedded file name: ../../aisdk2/game_ai_sdk/tools/phone_aiclientapi/WrappedDeviceAPI/deviceAPI/pcDevice/windows/win32driver/capture.py
# Compiled at: 2020-12-29 09:26:39
# Size of source mod 2**32: 5422 bytes
"""
窗口（桌面）截屏。需依赖cv2helper、logger模块。
"""
import os, time, traceback, ctypes, platform, win32gui, win32con, win32ui, logging, cv2, numpy as np
_is_windows = platform.platform().upper().startswith('WINDOWS')
logger = logging.getLogger('capture')
COLOR_BGR2GRAY = 6
COLOR_RGB2GRAY = 7
COLOR_BGRA2BGR = cv2.COLOR_BGRA2BGR

class BITMAPINFOHEADER(ctypes.Structure):
    __doc__ = 'BITMAP Info Header\n    '
    _fields_ = [
     (
      'biSize', ctypes.c_uint32),
     (
      'biWidth', ctypes.c_long),
     (
      'biHeight', ctypes.c_long),
     (
      'biPlanes', ctypes.c_uint16),
     (
      'biBitCount', ctypes.c_uint16),
     (
      'biCompression', ctypes.c_uint32),
     (
      'biSizeImage', ctypes.c_uint32),
     (
      'biXPelsPerMeter', ctypes.c_long),
     (
      'biYPelsPerMeter', ctypes.c_long),
     (
      'biClrUsed', ctypes.c_uint32),
     (
      'biClrImportant', ctypes.c_uint32)]


class RGBTRIPLE(ctypes.Structure):
    __doc__ = 'RGB Define\n    '
    _fields_ = [
     (
      'rgbBlue', ctypes.c_byte),
     (
      'rgbGreen', ctypes.c_byte),
     (
      'rgbRed', ctypes.c_byte),
     (
      'rgbReserved', ctypes.c_byte)]


class BITMAPINFO(ctypes.Structure):
    __doc__ = 'BITMAP Info\n    '
    _fields_ = [
     (
      'bmiHeader', BITMAPINFOHEADER),
     (
      'bmciColors', RGBTRIPLE * 1)]


def roi(src, rc):
    l, t, r, b = rc
    h, w = src.shape[:2]
    if r - l >= w:
        return src
    if b - t >= h:
        return src
    return src[t:b, l:r].copy()


def reshape(src, w, h, channels):
    return np.reshape(src, (h, w, channels))


def from_buffer(buff, dtype='uint8'):
    return np.frombuffer(buff, dtype=dtype)


def cvt_color(src, flags=COLOR_BGR2GRAY):
    return cv2.cvtColor(src, flags)


def get_image(hwnd=None):
    if hwnd is None:
        hwnd = win32gui.GetDesktopWindow()
    try:
        dc = ctypes.windll.user32.GetWindowDC(hwnd)
        cdc = ctypes.windll.gdi32.CreateCompatibleDC(dc)
        l, t, r, b = win32gui.GetWindowRect(hwnd)
        w = r - l
        h = b - t
        lpBits = ctypes.c_void_p(0)
        bmiCapture = BITMAPINFO()
        bmiCapture.bmiHeader.biSize = ctypes.sizeof(BITMAPINFO)
        bmiCapture.bmiHeader.biWidth = w
        bmiCapture.bmiHeader.biHeight = h
        bmiCapture.bmiHeader.biPlanes = 1
        bmiCapture.bmiHeader.biBitCount = 32
        bmiCapture.bmiHeader.biCompression = win32con.BI_RGB
        bmiCapture.bmiHeader.biSizeImage = 0
        bmiCapture.bmiHeader.biXPelsPerMeter = 0
        bmiCapture.bmiHeader.biYPelsPerMeter = 0
        bmiCapture.bmiHeader.biClrUsed = 0
        bmiCapture.bmiHeader.biClrImportant = 0
        hbmCapture = ctypes.windll.gdi32.CreateDIBSection(cdc, ctypes.byref(bmiCapture), win32con.DIB_RGB_COLORS, ctypes.byref(lpBits), None, 0)
        cpy_bytes = 0
        imageData = None
        if hbmCapture:
            CAPTUREBLT = 1073741824
            hbmOld = ctypes.windll.gdi32.SelectObject(cdc, hbmCapture)
            ctypes.windll.gdi32.BitBlt(cdc, 0, 0, w, h, dc, 0, 0, win32con.SRCCOPY | CAPTUREBLT)
            alloced_bytes = w * h * 4
            pBuf = ctypes.create_string_buffer(alloced_bytes)
            bmiCapture.bmiHeader.biHeight = 0 - h
            cpy_bytes = ctypes.windll.gdi32.GetDIBits(cdc, hbmCapture, 0, h, ctypes.byref(pBuf), ctypes.byref(bmiCapture), win32con.DIB_RGB_COLORS)
            if cpy_bytes == h:
                pBuf2 = ctypes.create_string_buffer(h * w * 3)
                pBuf2[0::3] = pBuf[0::4]
                pBuf2[1::3] = pBuf[1::4]
                pBuf2[2::3] = pBuf[2::4]
                imageData = reshape(from_buffer(pBuf2), w, h, 3)
            ctypes.windll.gdi32.SelectObject(cdc, hbmOld)
            ctypes.windll.gdi32.DeleteObject(hbmCapture)
        ctypes.windll.gdi32.DeleteDC(cdc)
        ctypes.windll.gdi32.DeleteDC(dc)
        return imageData
    except:
        traceback.print_exc()
        logger.error(traceback.format_exc())
        return