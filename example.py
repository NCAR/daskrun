from dask.distributed import Client
import dask
from daskrun.config import scheduler

# Get the scheduler information
client = Client(scheduler)
df = dask.datasets.timeseries()
print(df.head(20))
print(df.describe().compute())
client.write_scheduler_file("./dask-scheduler.json")
