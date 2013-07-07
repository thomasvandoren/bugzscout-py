#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name            ='bugzscout-py',
    version         ='0.0.1',
    description     ='Python interface for the FogBugz BugzScout API.',
    long_description=open('README.rst').read(),
    author          ='Thomas Van Doren',
    author_email    ='thomas@thomasvandoren.com',
    maintainer      ='Thomas Van Doren',
    maintainer_email='thomas@thomasvandoren.com',
    url             ='https://github.com/thomasvandoren/bugzscout-py',
    keywords        =['BugzScout', 'FogBugz'],
    license         ='BSD',
    packages        =find_packages(exclude=('test',)),
    classifiers     =[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        ],
    )
