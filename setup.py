#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open('millilauncher/VERSION') as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="millilauncher",
    version=version,
    # version=millilauncher.__version__,
    url="https://github.com/fhfuih/millilauncher",

    author="Zeyu Huang",
    author_email="sam.zyhuang@outlook.com",

    description="A minimalist, line-oriented Minecraft launcher",
    long_description=open("README.md").read(),

    packages=[
        "millilauncher",
    ],
    # ? include_package_data=True,
    entry_points={
        "console_scripts": [
            "millilauncher=millilauncher.cli:main"
        ]
    },
    install_requires=[
        "Click>=6.0",
    ],
    platforms="any",

    license="WTFPL",
    keywords="millilauncher",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
    ],
)
