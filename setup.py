#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="millilauncher",
    version="0.1.0",
    # version=millilauncher.__version__,
    url="https://github.com/fhfuih/millilauncher",

    author="Sam Zeyu Huang",
    author_email="sam.zyhuang@outlook.com",

    description="A minimalist, line-oriented Minecraft launcher",
    long_description=open('README.md').read(),

    packages=[
        'millilauncher',
    ],
    # ? include_package_data=True,
    entry_points={
        'console_scripts': [
            'millilauncher=millilauncher.cli:main'
        ]
    },
    install_requires=[
        'Click>=6.0',
    ],
    platforms='any',

    license="WTFPL",
    keywords='millilauncher',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
    ],
)
