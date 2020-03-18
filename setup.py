# Setup for WConio
# Modified from samples by Alex Martelli.

from distutils.core import setup, Extension
import sys

# version of this WConio package
this_version = "2.0"

# Determine Python version (tested on 2.0 and 2.1)
v = sys.version_info
python_version = v[0] * 100 + v[1] * 10 + v[2]

# turn keyword-arguments into a directory object
def dict_of(**kws): return kws

# the minimal info, which Python 2.0's distutils can digest
setup_args = dict_of(name="WConio2",
          version=this_version,
          description="WConio2",
          long_description="Windows Console I/O",
          author="Chris Gonnerman",
          author_email="chris@gonnerman.org",
          url="http://newcenturycomputers.net/projects/wconio.html",
          py_modules=["WConio2"],
    )

# provide more metadata if we have Python 2.1 (better distutils)
if python_version > 200:
    setup_args.update(dict_of(
          platforms="Win32",
          keywords="console screen",
    ))

# and finally call the distutils' setup
setup(**setup_args)

