# -*- coding: utf-8 -*-
u"""
Copyright 2018 David Amrani Hernandez

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup, find_packages

def read_file(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='awspice',
    version=read_file('VERSION').strip(),
    install_requires=read_file('requirements.txt').splitlines(),
    packages=find_packages(),
    author='David Amrani Hernandez',
    author_email='davidmorenomad@gmail.com',
    url='https://github.com/davidmoremad',
    project_urls={
        "Documentation": "https://awspice.readthedocs.io",
        "Source Code": "https://github.com/davidmoremad/awspice",
    },
    description='Awspice is a wrapper tool of Boto3 library to list inventory and manage your AWS infrastructure The objective of the wrapper is to abstract the use of AWS, being able to dig through all the data of our account',
    long_description=open('README.rst').read(),
    keywords="aws amazon cloud platform boto3 wrapper security management region account",
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ],
)
