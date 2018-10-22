#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function

import os 
import random 
import subprocess
import string

_JOB_TEMPLATE = """
#!/usr/bin/env bash
#PBS -N {name}
#PBS -q {queue}
#PBS -A {account_id}
#PBS -l select={num_nodes}:ncpus={num_cpus}:mpiprocs={num_mpiproc}
#PBS -l walltime={walltime}
#PBS -j oe
#PBS -m abe

# Setup dask worker
SCHEDULER=/glade/scratch/$USER/scheduler.json
mpirun --np {num_mpiproc} dask-mpi --nthreads 1 \
    --interface ib0 \
    --no-scheduler --local-directory /glade/scratch/$USER \
    --scheduler-file=$SCHEDULER
""".lstrip()


def random_id(length=8):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def submit_scheduler_job(name="dask-scheduler", queue="economy", account_id=None, num_nodes=1, num_cpus=1, num_mpiproc=1, walltime="01:00:00", cleanup=True):
    filled_form = _JOB_TEMPLATE.format(name=name, queue=queue, account_id=account_id, num_nodes=num_nodes, num_cpus=num_cpus, num_mpiproc=num_mpiproc, walltime=walltime)
    print(filled_form)
    base = f"submit_{name}_{random_id()}"
    print(base)
    open(f'{base}.sh', 'w').write(filled_form)
    try:
        cmd = ["qsub < ", f"{base}.sh"]
        print(cmd)
        subprocess.check_call(cmd, shell=True)

    finally:
        if cleanup:
            os.remove(f'{base}.sh')


submit_scheduler_job()