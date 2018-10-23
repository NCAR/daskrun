from dask.distributed import Client
from daskrun.config import scheduler

client = Client(scheduler)
client.write_scheduler_file("./dask-scheduler.json")
