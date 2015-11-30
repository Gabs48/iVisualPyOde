"""VisualPyODE:  A framework for using iVisual Python and PyODE libraries together.

iVisualPyODE is a framework library to aid in using PyODE and Visual Python together.  When you create
objects they have both physical and visual properties.  Supports collision, assemblies, and comes
with some helpful enhanced joints to simplify creating your visualized simulation.  I have implemented
the PyODE tutorial demo programs using the library so you can see exactly how to use it.  There are also
a few extra demos that go beyond the tutorial.
"""

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# Valid development status values:
#     1 - Planning, 2 - Pre-Alpha, 3 - Alpha, 4 - Beta, 5 - Production/Stable, 6 - Mature, 7 - Inactive

classifiers = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Developers
License :: OSI Approved :: GPL or BSD
Programming Language :: Python
Topic :: Multimedia :: Graphics :: 3D Modeling
Topic :: Scientific/Engineering :: Physics
Topic :: Scientific/Engineering :: Visualization
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
"""

doclines = __doc__.splitlines()

setup(name="iVisualPyODE",
      version="0.1",
      description=doclines[0],
      classifiers = filter(None, classifiers.split("\n")),
      long_description="\n".join(doclines[2:]),
      author="Gabriel Urbain",
      author_email="gabriel.urbain@ugent.be",
      license = "BSD or LGPL",
      url="https://github.com/Gabs48/iVisualPyOde",
      packages=find_packages(exclude=('tests', 'demos')) )

