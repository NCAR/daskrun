# daskrun
 daskrun allows the user to run a script that uses Dask for parallelism in the same way as running a script that uses MPI for parallelism.

## Difference between `mpirun` and `daskrun`

To illustrate differences between `mpirun` and `daskrun`, we are going to assume that we have a python script called `example.py`.

To execute this script with mpi, you might have to write another script, `submit_job.sh` with the following content:

```bash
  #!/bin/bash
  #PBS -N pangeo
  #PBS -q ${QUEUE}
  #PBS -A ${ACCOUNT}
  #PBS -l select=${NODES}:ncpus=${CORES}:mpiprocs=${CORES}
  #PBS -l walltime=$WALLTIME
  #PBS -j oe

  mpirun -np $CORES python example.py
```
Next, you would submit this script to the scheduler (in this case, we will assume that we are using `PBS`) by running:

        qsub submit_job.sh


With `daskrun`, everything is done for you from the command line:

    daskrun --script example.py --cores $NCORES --project $ACCOUNT --queue $QUEUE --walltime $WALLTIME


Another difference is that the `--cores`, `--memory`, `--num-processes` keywords used in `daskrun` correspond not to your full desired deployment, but rather to the size of a single job which should be no larger than the size of a single machine in your cluster. 
Separately **the number of jobs** to deploy corresponds to number of workers specified via `--num-workers` keyword argument. 


Under the hood, `daskrun` is doing the following:
- Get all the specific scheduler keywords such as `project`, `queue`, `walltime`, etc., and submits jobs to the scheduler via [dask-jobqueue](https://dask-jobqueue.readthedocs.io/en/latest/). This creates a dask cluster with the specified resources.  
- After this step, dask launches `dask-workers` on requested resources.
- Next, once the `dask-workers` are up and running, `dask-scheduler` is ready to launch, manage jobs on the created `dask-workers`. 
- Once all jobs are finished, the created dask cluster is teared down, and we are done. 

NOTE: 


## Installation 

To install the most recent stable version (`v.0.1.0`), run:
```bash
pip install git+git://github.com/NCAR/daskrun.git@v.0.1.0
```



```bash
abanihi@cheyenne5: ~ $ daskrun --help
Usage: daskrun [OPTIONS]

Options:
  --version                Show the version and exit.
  -s, --script PATH        Script to run
  -q, --queue TEXT         Destination queue for each worker job. Passed to
                           #PBS -q option.  [default: economy]
  -p, --project TEXT       Accounting string associated with each worker job.
                           Passed to #PBS -A option.  [default: ]
  -w, --walltime TEXT      Walltime for each worker job.  [default: 00:20:00]
  --num-workers INTEGER    Number of workers  [default: 1]
  --num-processes INTEGER  Number of Python processes to cut up each job
                           [default: 1]
  --cores INTEGER          Total number of cores per job  [default: 1]
  --memory TEXT            Total amount of memory per job
  --local-directory TEXT   Location to put temporary data if necessary
                           [default: /glade/scratch/abanihi]
  --help                   Show this message and exit.
```


## Usage 

To use daskrun, you need to include the following lines in your script:

```python
from daskrun.config import scheduler

client = Client(scheduler)
```

This allows the script to retrieve needed information about where dask scheduler is running from. 

An example `example.py` script is provided below:

```python
from dask.distributed import Client
import dask

# Make sure you include the following line in your script
# to get the scheduler information
from daskrun.config import scheduler

client = Client(scheduler)
df = dask.datasets.timeseries()
print(df.head(20))
print(df.describe().compute())
client.write_scheduler_file("./dask-scheduler.json")
```

```daskrun --script example.py --num-workers 2 --project PROJECTID --cores 1```

By inspecting the created `dask-scheduler.json` file, we expect to see two dask workers information along side dask's scheduler information.

```json
{
  "type": "Scheduler",
  "id": "Scheduler-f828319a-a327-4860-90b9-d863ef97cd9b",
  "address": "tcp://xx.xxx.x.x:51034",
  "services": {
    "bokeh": 8787
  },
  "workers": {
    "tcp://xx.xxx.x.x:34137": {
      "type": "Worker",
      "id": "dask-worker--3081414--",
      "host": "xx.xxx.x.xxx",
      "resources": {},
      "local_directory": "/glade/scratch/abanihi/worker-i68z06t5",
      "name": "dask-worker--3081414--",
      "ncores": 1,
      "memory_limit": 3000000000,
      "last_seen": 1540312311.5554748,
      "services": {
        "nanny": 41957,
        "bokeh": 33914
      },
      "metrics": {
        "cpu": 108.2,
        "memory": 123023360,
        "time": 1540312311.0555336,
        "read_bytes": 488117.31111868663,
        "write_bytes": 66659.12169260635,
        "num_fds": 27,
        "executing": 0,
        "in_memory": 94,
        "ready": 0,
        "in_flight": 0
      }
    },
    "tcp://xx.xxx.x.x:57886": {
      "type": "Worker",
      "id": "dask-worker--3081413--",
      "host": "xx.xxx.x.x",
      "resources": {},
      "local_directory": "/glade/scratch/abanihi/worker-tfduys7x",
      "name": "dask-worker--3081413--",
      "ncores": 1,
      "memory_limit": 3000000000,
      "last_seen": 1540312311.5556846,
      "services": {
        "nanny": 55003,
        "bokeh": 57435
      },
      "metrics": {
        "cpu": 112.0,
        "memory": 128286720,
        "time": 1540312311.0591698,
        "read_bytes": 528809.3225060791,
        "write_bytes": 65662.37663631311,
        "num_fds": 26,
        "executing": 0,
        "in_memory": 52,
        "ready": 0,
        "in_flight": 0
      }
    }
  }
```

