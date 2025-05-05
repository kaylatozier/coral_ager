#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup

# build command
setup(
    name="coral_ager",
    version="0.0.1",
    author="Kayla Tozier",
    author_email="kmt2183@columbia.edu",
    license="GPLv3",
    description="A package for creating toy datasets for Ager/Timer inputs",
    classifiers=["Programming Language :: Python :: 3"],
    entry_points={
        "console_scripts": ["coral_ager = coral_ager.__main__:main"]
    },
)
