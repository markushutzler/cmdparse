#!/usr/bin/env python

from distutils.core import setup

setup(
    name='cmdparse',
    packages=['cmdparse'],
    version='0.1',
    description='Argparse subclass with command support',
    author='Markus Hutzler',
    author_email='markus.hutzler@me.com',
    url='https://github.com/markushutzler/cmdparse',
    # download_url='https://github.com/markus.hutzler/cmdparse/tarball/0.1',
    keywords=['command line', 'argparse'],
    license='BSD3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
    ],
)
