from setuptools import setup, find_packages
from setup_info import console_scripts

setup(name='fsee_utils',
      version="0.5",
      package_dir={'':'src'},
      install_requires=['fsee','flydra','python-cjson','numpy'],
      packages=find_packages('src'),
      entry_points={ 'console_scripts': console_scripts},
)


