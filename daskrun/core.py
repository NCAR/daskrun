#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import click
import os
import random
import subprocess
import string
from dask_jobqueue import PBSCluster
import daskrun

global cluster 
cluster = None

version = daskrun.__version__

_JOB_TEMPLATE = """
#!/usr/bin/env bash
#PBS -N {name}
#PBS -q {queue}
#PBS -A {project}
#PBS -l select={num_nodes}:ncpus={num_cpus}:mpiprocs={num_mpiproc}
#PBS -l walltime={walltime}
#PBS -j oe
#PBS -m abe

# Setup dask worker
SCHEDULER=/glade/scratch/$USER/scheduler.json
rm -f $SCHEDULER
mpirun --np {num_mpiproc} dask-mpi --nthreads 1 \
    --interface ib0 \
    --no-scheduler --local-directory /glade/scratch/$USER \
    --scheduler-file=$SCHEDULER
""".lstrip()


def random_id(length=8):
    return "".join(random.sample(string.ascii_letters + string.digits, length))


def submit_scheduler_job(
    name="dask-scheduler",
    queue="economy",
    project=None,
    num_nodes=1,
    num_cpus=1,
    num_mpiproc=1,
    walltime="01:00:00",
    cleanup=True,
):
    filled_form = _JOB_TEMPLATE.format(
        name=name,
        queue=queue,
        project=project,
        num_nodes=num_nodes,
        num_cpus=num_cpus,
        num_mpiproc=num_mpiproc,
        walltime=walltime,
    )
    base = f"submit_{name}_{random_id()}"
    open(f"{base}.sh", "w").write(filled_form)
    try:
        cmd = ["qsub", f"{base}.sh"]
        print(cmd)
        subprocess.check_call(cmd)

    finally:
        if cleanup:
            os.remove(f"{base}.sh")


@click.command()
@click.version_option(version=version)
@click.option("--script", default=None, type=str, show_default=True, help="Script to run")
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
    print(script, num_workers, cores, memory, walltime, queue, project)
    # submit_scheduler_job(queue=queue, project=project, walltime=walltime)
    if not cluster or not isinstance(cluster, PBSCluster):
        cluster = PBSCluster(
            cores=cores, memory=memory, walltime=walltime, queue=queue, project=project
        )
        cluster.scale(num_workers)

    cmd = ["python", script]
    subprocess.check_call(cmd)

# submit_scheduler_job()
if __name__ == "__main__":
    cli()
