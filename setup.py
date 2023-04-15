#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
#import glob
#import subprocess
try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup
    setup

#githash = subprocess.check_output(["git", "log", "--format=%h"], universal_newlines=True).split('\n')[0]
vers = "1.0"
#githash = ""
#with open('prospect/_version.py', "w") as f:
#    f.write('__version__ = "{}"\n'.format(vers))
#    f.write('__githash__ = "{}"\n'.format(githash))

setup(
    name="ahc",
    version=vers,
    project_urls={"Source repo": "https://github.com/accuhijri/ahc"},
    author="Abdurrouf",
    author_email="abdurroufastro@gmail.com",
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Science/Research",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Natural Language :: English",
                 "Topic :: Scientific/Engineering :: Astronomy"],
    packages=["ahc",
              "ahc.sunmoon",
              "ahc.crescent",
              "ahc.hilal",
              "ahc.plotting"],
    python_requires=">=2.7, <4",
    license="MIT",
    description="A python package for calculating position and visibility of the crescent moon at the sunset time after the conjunction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"": ["README.md", "LICENSE"]},
    #scripts=glob.glob("scripts/*.py"),
    include_package_data=True,
    install_requires=["numpy", "skyfield=1.45", "datetime", "pytz", "pymeeus", "astropy", "matplotlib", "geopandas"],
)
