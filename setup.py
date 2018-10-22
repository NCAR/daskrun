#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()


requirements = ["dask-jobqueue]

test_requirements = ["pytest", "flake8"]

setup(
    maintainer="Anderson Banihirwe",
    maintainer_email="abanihi@ucar.edu",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    description="mpirun-like operation with dask-jobqueue",
    install_requires=requirements,
    license="https://github.com/NCAR/daskrun/blob/master/LICENSE.rst",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=["daskrun", "dask", "dask-jobqueue"],
    name="daskrun",
    packages=find_packages(include=["daskrun",]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/NCAR/daskrun",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points="""
      [console_scripts]
      daskrun=daskrun.core:cli
      """,
    zip_safe=False,
)
