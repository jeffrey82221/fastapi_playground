# fastapi_playground
Place for studying and experimenting with FastAPI

# Install 

pip install -r requirements.txt

# Locally test the API

1) Run the API on terminal 
```bash
uvicorn executor_api:app --reload --host=127.0.0.1 --port=9999
```
2) Goto the APIHub Page: localhost:9999/docs

3) Run the apitest: 

python test_execution.py

# Run the API server on colab and test it locally 

1) Run the colab notebook: ColabFastAPI.ipynb

2) Replace the api url in `test_colab_execution.py` with that shown in the last cell of colab:

e.g., Colab api url: <http://c26c-35-245-61-122.ngrok.io>

3) On local terminal, execute `test_colab_execution.py`

# Run the Ray server in container and port it to the internet via fastapi

1) Build a image with ray serving

```bash
docker build -t ray_server .
```

2) Run the image as container and start the API inside
```bash
docker run -it -p 9999:9999 --shm-size=4.80gb --rm ray_server bash
```

3) Run start.sh in the container
```bash
redis-server &
echo 'redis started'
env RAY_LOG_TO_STDERR=1 ray start --head --port=7000 --redis-shard-ports=6379
sleep 20
uvicorn executor_api:app --host 172.17.0.2 --port 9999
```
3) Build an router api that connect the in-container API to the outside world 


# Run on stand alone MAC account 

## Create a minimum privilege user account 

## Install python envirnoment for ray 

follow REF: https://docs.ray.io/en/master/ray-overview/installation.html#m1-mac-apple-silicon-support

## Install packages: 

```bash
pip install -r requirements.txt
```

## Run ray 

ray start --head

## Run API 

```bash
python3 porting.py
```