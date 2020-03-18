#!/usr/bin/env python

"""
WConio.py -- Windows Console I/O Module

This is version 2 of the WConio console io module.  It uses the ctypes module,
and thus does not need a subordinate C module, making it more portable and
easier to install.
"""

__version__ = "2.0"

BLACK = 0
BLUE = 1
GREEN = 2
CYAN = 3
RED = 4
MAGENTA = 5
BROWN = 6
LIGHTGRAY = LIGHTGREY = 7
DARKGRAY = DARKGREY = 8
LIGHTBLUE = 9
LIGHTGREEN = 10
LIGHTCYAN = 11
LIGHTRED = 12
LIGHTMAGENTA = 13
YELLOW = 14
WHITE = 15

FOREGROUND_INTENSITY = 8

NORM_ATTR = LIGHTGRAY
NORM_CURSOR_SIZE = 10
SOLID_CURSOR_SIZE = 99
C80 = 3

_NOCURSOR = 0
_SOLIDCURSOR = 1
_NORMALCURSOR = 2

__keydict = {
    0x3b : 'f1',
    0x3c : 'f2',
    0x3d : 'f3',
    0x3e : 'f4',
    0x3f : 'f5',
    0x40 : 'f6',
    0x41 : 'f7',
    0x42 : 'f8',
    0x43 : 'f9',
    0x44 : 'f10',

    0x68 : 'altf1',
    0x69 : 'altf2',
    0x6a : 'altf3',
    0x6b : 'altf4',
    0x6c : 'altf5',
    0x6d : 'altf6',
    0x6e : 'altf7',
    0x6f : 'altf8',
    0x70 : 'altf9',
    0x71 : 'altf10',

    0x5e : 'ctrlf1',
    0x5f : 'ctrlf2',
    0x60 : 'ctrlf3',
    0x61 : 'ctrlf4',
    0x62 : 'ctrlf5',
    0x63 : 'ctrlf6',
    0x64 : 'ctrlf7',
    0x65 : 'ctrlf8',
    0x66 : 'ctrlf9',
    0x67 : 'ctrlf10',

    0x54 : 'shiftf1',
    0x55 : 'shiftf2',
    0x56 : 'shiftf3',
    0x57 : 'shiftf4',
    0x58 : 'shiftf5',
    0x59 : 'shiftf6',
    0x5a : 'shiftf7',
    0x5b : 'shiftf8',
    0x5c : 'shiftf9',
    0x5d : 'shiftf10',

    0x52 : 'ins',
    0x53 : 'del',
    0x4f : 'end',
    0x50 : 'down',
    0x51 : 'pgdn',
    0x4b : 'left',
    0x4d : 'right',
    0x47 : 'home',
    0x48 : 'up',
    0x49 : 'pgup',

    0xa2 : 'altins',
    0xa3 : 'altdel',
    0x9f : 'altend',
    0xa0 : 'altdown',
    0xa1 : 'altpgdn',
    0x9b : 'altleft',
    0x9d : 'altright',
    0x97 : 'althome',
    0x98 : 'altup',
    0x99 : 'altpgup',

    0x92 : 'ctrlins',
    0x93 : 'ctrldel',
    0x75 : 'ctrlend',
    0x91 : 'ctrldown',
    0x76 : 'ctrlpgdn',
    0x73 : 'ctrlleft',
    0x74 : 'ctrlright',
    0x77 : 'ctrlhome',
    0x8d : 'ctrlup',
    0x84 : 'ctrlpgup',

    3 : 'ctrl2'
}

# connect to kernel32.dll, which actually does all the business.

import ctypes
from ctypes import windll
from ctypes.wintypes import *
import msvcrt

kernel32 = windll.kernel32

LPSECURITY_ATTRIBUTES = ctypes.c_void_p

############################################################################
# internal functions

class error(Exception):
    pass

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ('dwSize', ctypes.wintypes._COORD),
        ('dwCursorPosition', ctypes.wintypes._COORD),
        ('wAttributes', ctypes.c_ushort),
        ('srWindow', ctypes.wintypes._SMALL_RECT),
        ('dwMaximumWindowSize', ctypes.wintypes._COORD)
    ]

class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('bVisible', BOOL),
    ]

class Char(ctypes.Union):
    _fields_ = [
        ("UnicodeChar", WCHAR),
        ("AsciiChar", CHAR),
    ]

class CHAR_INFO(ctypes.Structure):
    _anonymous_ = ("Char",)
    _fields_ = [
        ("Char", Char),
        ("Attributes", WORD),
    ]

def _getconhandle(pszName):
    return HANDLE(kernel32.CreateFileW(
        LPWSTR(pszName),
        DWORD(0xC0000000),
        DWORD(0x00000003),
        LPSECURITY_ATTRIBUTES(None),
        DWORD(3),
        DWORD(0),
        HANDLE(None)
    ))

def _getconout():
    hConOut = _getconhandle("CONOUT$")
    if hConOut == HANDLE(-1):
        raise error("_getconout() failed")
    return hConOut

def _releaseconout(h):
    return BOOL(kernel32.CloseHandle(h))

def _setcursortype(cur_t):
    cci = CONSOLE_CURSOR_INFO()
    hConOut = _getconout()
    kernel32.GetConsoleCursorInfo(hConOut, ctypes.byref(cci))
    if cur_t == _NOCURSOR:
        cci.dwSize = NORM_CURSOR_SIZE
        cci.bVisible = BOOL(0)
    elif cur_t == _SOLIDCURSOR:
        cci.dwSize = SOLID_CURSOR_SIZE
        cci.bVisible = BOOL(1)
    elif cur_t == _NORMALCURSOR:
        cci.dwSize = NORM_CURSOR_SIZE
        cci.bVisible = BOOL(1)
    kernel32.SetConsoleCursorInfo(hConOut, ctypes.byref(cci))
    _releaseconout(hConOut)

def _getscreeninfo():
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    hConOut = _getconout()
    if BOOL(kernel32.GetConsoleScreenBufferInfo(
            hConOut, ctypes.byref(csbi))):
        _releaseconout(hConOut)
        return csbi
    _releaseconout(hConOut)
    raise error("_getscreeninfo() failed")

def _conputs(pszText):
    hConOut = _getconout()
    kernel32.WriteConsoleA(hConOut,
        LPSTR(pszText),
        DWORD(len(pszText)),
        LPDWORD(ctypes.c_ulong(0)),
        None
    )
    _releaseconout(hConOut)

############################################################################
# control functions

def gettextinfo():

    csbi = _getscreeninfo()

    return (
        csbi.srWindow.Left,
        csbi.srWindow.Top,
        csbi.srWindow.Right,
        csbi.srWindow.Bottom,
        csbi.wAttributes,
        NORM_ATTR,
        C80,
        csbi.dwSize.Y,
        csbi.dwSize.X,
        csbi.dwCursorPosition.X,
        csbi.dwCursorPosition.Y,
    )

############################################################################
# cursor functions

def wherex():
    csbi = _getscreeninfo()
    if csbi is not None:
        return csbi.dwCursorPosition.X
    raise error("GetScreenInfo Failed")

def wherey():
    csbi = _getscreeninfo()
    if csbi is not None:
        return csbi.dwCursorPosition.Y
    raise error("GetScreenInfo Failed")

def gotoxy(x, y):
    coord = ctypes.wintypes._COORD()
    hConOut = _getconout()
    coord.X = x
    coord.Y = y
    kernel32.SetConsoleCursorPosition(hConOut, coord)
    _releaseconout(hConOut)

def setcursortype(cur_t):
    if cur_t == 0:
        _setcursortype(_NOCURSOR)
    elif cur_t == 1:
        _setcursortype(_NORMALCURSOR)
    elif cur_t == 2:
        _setcursortype(_SOLIDCURSOR)

def highvideo():
    hConOut = _getconout()
    csbi = _getscreeninfo()
    kernel32.SetConsoleTextAttribute(hConOut, 
        WORD(csbi.wAttributes | FOREGROUND_INTENSITY))
    return

def lowvideo():
    hConOut = _getconout()
    csbi = _getscreeninfo()
    kernel32.SetConsoleTextAttribute(hConOut, 
        WORD(
            (csbi.wAttributes | FOREGROUND_INTENSITY)
                - FOREGROUND_INTENSITY
        ))

def textattr(newattr):
    hConOut = _getconout()
    kernel32.SetConsoleTextAttribute(hConOut, WORD(newattr))
    _releaseconout(hConOut)

############################################################################
# text i/o functions

def clreol():
    hConOut = _getconout()
    csbi = _getscreeninfo()
    kernel32.FillConsoleOutputCharacterA(hConOut,
        ctypes.c_char(b' '),
        csbi.dwSize.X - csbi.dwCursorPosition.X, 
        csbi.dwCursorPosition,
        LPDWORD(ctypes.c_ulong(0))
    )
    kernel32.FillConsoleOutputAttribute(hConOut,
        csbi.wAttributes, 
        csbi.dwSize.X - csbi.dwCursorPosition.X, 
        csbi.dwCursorPosition,
        LPDWORD(ctypes.c_ulong(0))
    )
    _releaseconout(hConOut)

def clrscr():
    hConOut = _getconout()
    csbi = _getscreeninfo()
    coord = ctypes.wintypes._COORD()
    coord.X = 0
    coord.Y = 0
    kernel32.FillConsoleOutputCharacterA(
        hConOut,
        ctypes.c_char(b' '), 
        csbi.dwSize.X * csbi.dwSize.Y,
        coord,
        LPDWORD(ctypes.c_ulong(0))
    )
    kernel32.FillConsoleOutputAttribute(
        hConOut,
        csbi.wAttributes, 
        csbi.dwSize.X * csbi.dwSize.Y,
        coord,
        LPDWORD(ctypes.c_ulong(0))
    )
    kernel32.SetConsoleCursorPosition(hConOut, coord)
    _releaseconout(hConOut)

def delline():
    srSource = ctypes.wintypes._SMALL_RECT()
    ciFill = CHAR_INFO()
    hConOut = _getconout()
    csbi = _getscreeninfo()
    srSource.Top = csbi.dwCursorPosition.Y
    srSource.Left = csbi.srWindow.Left
    srSource.Bottom = csbi.srWindow.Bottom
    srSource.Right = csbi.srWindow.Right
    dwDest.X = csbi.srWindow.Left
    dwDest.Y = csbi.dwCursorPosition.Y
    ciFill.Char.UnicodeChar = ctypes.c_char(b' ')
    ciFill.Attributes = csbi.wAttributes
    kernel32.ScrollConsoleScreenBuffer(hConOut,
        ctypes.byref(srSource),
        LPDWORD(ctypes.c_ulong(0)),
        dwDest, 
        ctypes.byref(ciFill)
    )

def insline():
    srSource = ctypes.wintypes._SMALL_RECT()
    ciFill = CHAR_INFO()
    hConOut = _getconout()
    csbi = _getscreeninfo()
    srSource.Top = csbi.dwCursorPosition.Y
    srSource.Left = csbi.srWindow.Left
    srSource.Bottom = csbi.srWindow.Bottom
    srSource.Right = csbi.srWindow.Right
    dwDest.X = csbi.srWindow.Left
    dwDest.Y = csbi.dwCursorPosition.Y
    ciFill.Char.UnicodeChar = ctypes.c_char(b' ')
    ciFill.Attributes = csbi.wAttributes
    kernel32.ScrollConsoleScreenBuffer(hConOut,
        ctypes.byref(srSource),
        LPDWORD(ctypes.c_ulong(0)),
        dwDest, 
        ctypes.byref(ciFill)
    )

def gettext(left, top, right, bottom):
    srSource = ctypes.wintypes._SMALL_RECT()
    dwBufferSize = ctypes.wintypes._COORD()
    dwBufferOrg = ctypes.wintypes._COORD()
    hConOut = _getconout()
    srSource.Left = left
    srSource.Top = top
    srSource.Right = right
    srSource.Bottom = bottom
    dwBufferSize.X = srSource.Right - srSource.Left + 1
    dwBufferSize.Y = srSource.Bottom - srSource.Top + 1
    dwBufferOrg.X = 0
    dwBufferOrg.Y = 0
    dwBuffLen = dwBufferSize.X * dwBufferSize.Y
    BufType = CHAR_INFO * dwBuffLen
    buf = BufType()
    if BOOL(kernel32.ReadConsoleOutputA(hConOut,
        ctypes.byref(buf),
        dwBufferSize, 
        dwBufferOrg,
        ctypes.byref(srSource))
    ):
        # previous versions of this function went to silly lengths
        # to replicate the Turbo C data structure.  however, we
        # almost never care about the internal structure, so here
        # we will just return the buffer we got from kernel32.
        _releaseconout(hConOut)
        return buf
    _releaseconout(hConOut)
    raise error("gettext() failed.")

def puttext(left, top, right, bottom, source):
    srDest = ctypes.wintypes._SMALL_RECT()
    dwBufferSize = ctypes.wintypes._COORD()
    dwBufferOrg = ctypes.wintypes._COORD()
    hConOut = _getconout()
    srDest.Left = left
    srDest.Top = top
    srDest.Right = right
    srDest.Bottom = bottom
    dwBufferSize.X = srDest.Right - srDest.Left + 1
    dwBufferSize.Y = srDest.Bottom - srDest.Top + 1
    dwBufferOrg.X = 0
    dwBufferOrg.Y = 0
    dwBuffLen = dwBufferSize.X * dwBufferSize.Y
    kernel32.WriteConsoleOutputA(hConOut,
        ctypes.byref(source),
        dwBufferSize, 
        dwBufferOrg,
        ctypes.byref(srDest))
    _releaseconout(hConOut)

def settitle(title):
    if kernel32.SetConsoleTitle(title) == 0:
        raise error("settitle failed")

def kbhit():
    return BOOL(msvcrt.kbhit())

def getch():
    rc = ctypes.c_char(msvcrt.getch())
    try:
        ch = chr(rc)
    except:
        ch = '\0'
    return (rc, ch)

def putch(ch):
    if type(ch) is int:
        ch = chr(ch).encode(encoding = 'UTF-8')
    elif type(ch) is bytes:
        pass
    else:
        ch = str(ch).encode(encoding = 'UTF-8')
    msvcrt.putch(ch)

def ungetch(ch):
    if type(ch) is int:
        msvcrt.ungetch(bytearray(chr(ch).encode('utf8')))
    else:
        msvcrt.ungetch(bytearray(ch))

############################################################################
# public functions

def cputs(s):
    for c in s:
        putch(c)

def getkey():
    n, c = getch()
    # 0xE0 is 'grey' keys.  change this if you don't like 
    # it, but I don't care what color the key is.  IMHO it
    # just confuses the end-user if they need to know.
    if n == 0 or n == 0xE0:
        n, c = getch()
        if __keydict.has_key(n):
            return __keydict[n]
        return "key%x" % n
    return c

def cgets(l):
    s = ""
    c = getkey()
    while c != '\n' and c != '\r':
        if c == '\010': # backspace
            if s:
                s = s[:-1]
                gotoxy(wherex() - 1, wherey())
                putch(" ")
                gotoxy(wherex() - 1, wherey())
        elif c >= " " and c <= "~":
            if len(s) < l:
                s = s + c
                putch(c)
        c = getkey()
    return s

def textmode():
    textattr(LIGHTGRAY)
    clrscr()
    setcursortype(_NORMALCURSOR)

def textcolor(c):
    bgcolor = gettextinfo()[4] & 0x00F0
    textattr(c | bgcolor)

def textbackground(c):
    fgcolor = gettextinfo()[4] & 0x000F
    textattr((c << 4) | fgcolor)

def getche():
    rc, s = getch()
    if s:
        putch(s)
    return (rc, s)

def normvideo():
    textattr(gettextinfo()[5])

def movetext(left, top, right, bottom, destleft, desttop):
    s = gettext(left, top, right, bottom)
    puttext(destleft, desttop, 
        right + (destleft - left), 
        bottom + (desttop - top), s)

class WCFile:
    def __init__(self):
        self.closed = 0
        self.mode = "r+"
        self.name = "<WConio>"
        self.softspace = 0
    def close(self):
        pass
    def flush(self):
        pass
    def isatty(self):
        return 1
    def read(self, size = 1):
        if size <= 1:
            return getch()[1]
        else:
            return cgets(size)
    def readline(self, size = 0):
        rc = cgets(size)
        if size:
            rc = rc[:size]
        return rc
    def readlines(self, sizehint = 0):
        "readlines() is pure nonsense for WConio, so this just calls readline."
        return readline(self, sizehint)
    def write(self, str):
        cputs(str)
    def writelines(self, l):
        for i in l:
            cputs(i)

File = WCFile()     # we just keep one of these around, so the
del WCFile          # class constructor gets used just once.


# end of file.
