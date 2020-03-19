# Setup for WConio

long_description = """
WConio2.py
----------

This module is a pure Python reimplementation of my WConio module, and is
generally API compatible with version 1.5.1 of that module.  WConio provides a
color console interface for Windows applications using an interface based
generally on the conio.h functions included with Turbo C 2.0.  While the
original module depended on code written by Daniel Guerrero Miralles, this
module includes none of his code.

The conio.h functions don't map perfectly to Python, so I have taken some
liberties.  In particular, the window() functionality is not provided, and
screen coordinates are based at 0, 0 (logical for Python, but counter to the
tradition of conio.h).

If you are porting an application written for the original WConio, it's
perfectly acceptable to say:

import WConio2 as WConio
"""

from distutils.core import setup
setup(
  name = 'WConio2',
  py_modules = ['WConio2'],
  version = '2.0',
  license='MIT',
  description="Windows Console I/O",
  long_description=long_description,
  author = 'Chris Gonnerman',
  author_email = 'chris@gonnerman.org',
  url = 'https://github.com/Solomoriah/WConio2',
  download_url = 'https://github.com/Solomoriah/WConio2/archive/v20.tar.gz', 
  keywords = [ "windows", "console", "screen", ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
  ],
)


# end of file.
