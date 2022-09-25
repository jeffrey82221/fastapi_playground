redis-server &
echo 'redis started'
env RAY_LOG_TO_STDERR=1 ray start --head --port=7000 --redis-shard-ports=6379
sleep 20
uvicorn executor_api:app --host 172.17.0.2 --port 9999

# ray.init(local_mode=True, include_dashboard=False, num_gpus=0, num_cpus=1, logging_level=logging.DEBUG)
