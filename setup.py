from setuptools import setup
from setup_info import console_scripts #@UnresolvedImport

setup(name='rfsee',
      version="0.5",
      package_dir={'':'src'},
      install_requires=[
       # for rfsee
       'python-cjson'],
      packages=['rfsee'],
      entry_points={ 'console_scripts': console_scripts},
)


