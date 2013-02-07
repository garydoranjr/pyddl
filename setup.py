try:
    from setuptools import setup
    setup  # quiet "redefinition of unused ..." warning from pyflakes
    # arguments that distutils doesn't understand
    setuptools_kwargs = {
        'provides': ['pyddl'],
    }
except ImportError:
    from distutils.core import setup
    setuptools_kwargs = {}

setup(name='pyddl',
      version="1.0",
      description=(
        'STRIPS planner with PDDL-like problem specification in Python'
      ),
      author='Gary Doran',
      author_email='gary.doran@case.edu',
      url='https://github.com/garydoranjr/pyddl.git',
      license="MIT (see the LICENSE file)",
      packages=['pyddl'],
      platforms=['unix'],
      **setuptools_kwargs
)

