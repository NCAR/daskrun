#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function

with open('~/.daskrun/dask-run-scheduler.json', 'r') as f:
    scheduler=json.loads(f.read())['scheduler']

