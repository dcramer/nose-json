#!/usr/bin/env python

from setuptools import setup, find_packages

tests_require = [
]

setup(
    name='nose-json',
    version='0.2.1',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    description='A JSON report plugin for Nose.',
    url='http://github.com/dcramer/nose-json',
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    install_requires=[
        'nose>=0.9',
        'simplejson',
    ],
    entry_points={
       'nose.plugins.0.10': [
            'nose_json = nose_json.plugin:JsonReportPlugin'
        ]
    },
    license='Apache License 2.0',
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
