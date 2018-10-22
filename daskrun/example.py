from dask.distributed import Client 
from daskrun.core import cluster 

client = Client(cluster)
client.write_scheduler_file('dask-scheduler.json')