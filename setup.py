#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'libvirt-python>=2.4',
]

test_requirements = [
    # put package test requirements here
]

setup(
    name='libvirt_provider',
    version='0.0.1',
    description="A handy wrapper around libvirt-api written in python.",
    long_description=readme + '\n\n' + history,
    author="Pranav Salunke",
    author_email='dguitarbite@gmail.com',
    url='https://github.com/dguitarbite/python-libvirt_provider',
    packages=[
        'libvirt_provider',
    ],
    package_dir={'libvirt_provider':
                 'libvirt_provider'},
    entry_points={
        'console_scripts': [
            'libvirt_provider=libvirt_provider.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='libvirt_provider',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
