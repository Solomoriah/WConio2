import sys
import unittest
import time
from WConio2 import *

# indices into gettextinfo tuple
tiTEXTATTR = 4
tiNORMATTR = 5

if sys.version_info>=(3,0):
  # in 3.0, bytes[n] -> int
  # no need to convert
  def byte2int(x):
    return x
else:
  # in 2.x, bytes[n] = str[n] -> str
  # convert to int using ord
  def byte2int(x):
    return ord(x)

class WConioTest(unittest.TestCase):

    def test_goto(self):
        clrscr()
        self.assertEqual(wherex(), 0)
        self.assertEqual(wherey(), 0)
        gotoxy(4, 10)
        self.assertEqual(wherex(), 4)
        self.assertEqual(wherey(), 10)
        cputs("This text will be erased soon: good bye cruel world!\n"
          "but this line will remain for a while.")
        self.assertEqual(wherex(), 38)
        self.assertEqual(wherey(), 11)
        gotoxy(35, 10)
        clreol()
        self.assertEqual(wherex(), 35)
        self.assertEqual(wherey(), 10)
        # the following line depends on the old binary format for gettext()
        # self.assertEqual(gettext(29,10,38,11)[::2], b'soon:      a while. ')

    def test_cursor(self):
        clrscr()
        cputs("Look at the cursor.")
        setcursortype(0)
        cputs("\nInvisible cursor (press Y/N): ")
        self.assertEqual(getch()[1].lower(), 'y')
        setcursortype(2)
        cputs("\nBlock cursor (press Y/N): ")
        self.assertEqual(getch()[1].lower(), 'y')
        setcursortype(1)
        cputs("\nNormal cursor (press Y/N): ")
        self.assertEqual(getch()[1].lower(), 'y')

    def test_delline(self):
        # the original version of this test used gettext() and expected
        # the data to be in the original turbo c format; it's not, so the
        # test failed.  this test isn't really doing much anymore.
        clrscr()
        cputs("0\n1\n2")
        gotoxy(10, 1)
        delline()
        self.assertEqual(wherex(), 10)
        self.assertEqual(wherey(), 1)
        gotoxy(10, 0)
        delline()

    def test_insline(self):
        clrscr()
        cputs("0\n1\n2")
        # the following line depends on the old binary format for gettext()
        # self.assertEqual(gettext(0,0,0,2)[::2], b'012')
        gotoxy(10, 1)
        insline()
        self.assertEqual(wherex(), 10)
        self.assertEqual(wherey(), 1)
        # the following line depends on the old binary format for gettext()
        # self.assertEqual(gettext(0,0,0,3)[::2], b'0 12')
        gotoxy(10, 0)
        insline()
        # the following line depends on the old binary format for gettext()
        # self.assertEqual(gettext(0,0,0,4)[::2], b' 0 12')

    def test_putch(self):
        clrscr()
        putch(ord('1'))
        putch('2')
        putch(b'3')
        # the following line depends on the old binary format for gettext()
        # self.assertEqual(gettext(0, 0, 2, 0)[::2], b'123')

    def test_movetext(self):
        pass

# More code dependent on the internal representation of gettext().

#        clrscr()
#        cputs("0123456789" * 4 + "\n")
#        cputs(".1.3.5.7.9" * 4 + "\n")
#        cputs("0.2.4.6.8." * 4 + "\n")
#        cputs("0123456789" * 4 + "\n")
#        t1 = gettext(7, 1, 26, 3)[::2]
#        movetext(7, 1, 26, 3, 35, 0)
#        t2 = gettext(35, 0, 35+20-1, 3)[::2]
#        self.assertEqual(t1 + b"56789               ", t2)

    def test_puttext(self):
        clrscr()
        cputs("0123456789" * 4 + "\n")
        cputs(".1.3.5.7.9" * 4 + "\n")
        cputs("0.2.4.6.8." * 4 + "\n")
        cputs("0123456789" * 4 + "\n")
        saved = gettext(7, 1, 26, 3)
        clrscr()
        puttext(7, 1, 26, 3, saved)
        t1 = gettext(7, 1, 10, 2)[::2]
        # the following line depends on the old binary format for gettext()
        # self.assertEqual(t1, b"7.9..8.0")

    def test_input(self):
        clrscr()
        cputs("Press 'y' to continue: ")
        while not kbhit():
          cputs('.')
          time.sleep(0.2)
        self.assertEqual(getch(), (ord('y'), 'y'))
        cputs("\nPress 'y' again: ")
        self.assertEqual(getkey(), 'y')
        cputs("\nPress 'y' again (with echo): ")
        self.assertEqual(getche(), (ord('y'), 'y'))
        cputs("\nType 'yyy' and press <ENTER>: ")
        self.assertEqual(cgets(5), 'yyy')
        ungetch('*')
        self.assertEqual(getch(), (ord('*'), '*'))
        cputs("\nPress Alt-F1: ")
        self.assertEqual(getkey(), 'altf1')

    def test_attrs(self):
        attr = LIGHTGRAY
        textattr(attr)
        info = gettextinfo()
        self.assertEqual(info[tiTEXTATTR], attr)

# This whole section is dependent on the layout of the buffer returned
# by gettext(); WConio 2.0 uses the "raw" format provided by Win32
# rather than slavishly replicating the Turbo C format.  Thus, this
# section is commented as not useful right now.

#        attr = (CYAN<<4) | YELLOW
#        textattr(attr)
#        clrscr()
#        cputs("Hello world!\n")
#        ta = gettext(0,0,0,0)[1]
#        attr2 = byte2int(ta)
#        self.assertEqual(attr2, attr)
#        textbackground(BLUE)
#        textcolor(RED)
#        cputs("Red ")
#        textcolor(WHITE)
#        cputs("White")
#        ta = gettext(0,1,3,1)[1::2]
#        self.assertEqual(list(map(byte2int,ta)), [BLUE<<4|RED] * 4)
#        ta = gettext(4,1,8,1)[1::2]
#        self.assertEqual(list(map(byte2int,ta)), [BLUE<<4|WHITE] * 5)


if __name__ == '__main__':
    unittest.main()
