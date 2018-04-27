#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(
    name='django-automationoauth',
    author='University of Cambridge Information Services',
    author_email='automation@uis.cam.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=[
        'django>=1.8,<2.1',
        'djangorestframework',
        'requests-oauthlib'
    ],
    tests_require=[],
)
