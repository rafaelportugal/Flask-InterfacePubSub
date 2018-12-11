#!/usr/bin/env python

import re
import sys
from os import path
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "Flask>=0.12",
    "Flask-RESTful>=0.3.3",
    "mementos>=1.3.1",
    "google-cloud-pubsub>=0.38.0",
    "jsonschema>=2.6.0",
    "strict-rfc3339>=0.7",
]

version_file = path.join(
    path.dirname(__file__), "flask_interface_gcp_pubsub", "__version__.py")
with open(version_file, "r") as fp:
    m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", fp.read(), re.M)
    version = m.groups(1)[0]

setup(
    name="Flask-InterfacePubSub",
    version=version,
    author="Rafael Portugal",
    license="MIT",
    author_email="rafaelportugal05@gmail.com",
    description="Package for help to send contract to Google Pub Sub.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafaelportugal/Flask-InterfacePubSub",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Framework :: Flask",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requirements,
)
