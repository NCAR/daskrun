#!/usr/bin/env python
""" The configuration utility script. This script is used
to pass scheduler address to the running dask program.
"""

from __future__ import absolute_import
from __future__ import print_function
import json
import os

HOME = os.environ["HOME"]
daskrun_dir = f"{HOME}/.daskrun/"
scheduler_file_path = f"{daskrun_dir}/dask-run-scheduler.json"

with open(scheduler_file_path, "r") as f:
    scheduler = json.loads(f.read())["scheduler"]
