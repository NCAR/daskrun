#!/usr/bin/env python
"""
The main command line script. This is the script that is
executed when using `daskrun`
"""

from __future__ import absolute_import
from __future__ import print_function
import click
import os
import subprocess
from dask_jobqueue import PBSCluster
import daskrun
import json
import time


version = daskrun.__version__


@click.command()
@click.version_option(version=version)
@click.option(
    "--script", default=None, type=str, show_default=True, help="Script to run"
)
@click.option(
    "--num-workers", default=1, type=int, show_default=True, help="Number of workers"
)
@click.option(
    "--cores",
    default=5,
    type=int,
    show_default=True,
    help="Total number of cores per job",
)
@click.option(
    "--memory",
    default=None,
    type=str,
    show_default=True,
    help="Total amount of memory per job",
)
@click.option(
    "--walltime",
    default="00:20:00",
    type=str,
    show_default=True,
    help="Walltime for each worker job.",
)
@click.option(
    "--queue",
    default="economy",
    type=str,
    show_default=True,
    help="Destination queue for each worker job. Passed to #PBS -q option.",
)
@click.option(
    "--project",
    default="",
    type=str,
    show_default=True,
    help="Accounting string associated with each worker job. Passed to #PBS -A option.",
)
def cli(script, num_workers, cores, memory, walltime, queue, project):

    cluster = PBSCluster(
        cores=cores, memory=memory, walltime=walltime, queue=queue, project=project
    )

    # Write scheduler address to a file on a disk.
    # This allows us to pass this info to the dask script
    HOME = os.environ["HOME"]
    daskrun_dir = f"{HOME}/.daskrun/"
    scheduler_file_path = f"{daskrun_dir}/dask-run-scheduler.json"
    if os.path.exists(scheduler_file_path):
        os.remove(scheduler_file_path)

    os.makedirs(daskrun_dir, exist_ok=True)
    with open(scheduler_file_path, "w") as f:
        f.write(json.dumps({"scheduler": cluster.scheduler_address}))
    cluster.scale(num_workers)

    # Make sure all reqeuested resources are available before
    # Executing the script.
    # cluster.pending_jobs is an OrderedDict.
    # The script should be executed when this dict is empty
    while not cluster.pending_jobs:
        time.sleep(0.5)

    # Get absolute path of the script
    script_path = os.path.abspath(script)
    cmd = ["python", script_path]

    # Run the script via subprocess
    subprocess.check_call(cmd)


if __name__ == "__main__":
    cli()
