"""
How to setup executor_api? 
pip install -r requirements.txt
uvicorn executor_api:app --port 8080


"""
from ray import serve
from fastapi import FastAPI
import time

app = FastAPI()
@serve.deployment(
    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 3,
        "target_num_ongoing_requests_per_replica": 1,
    }
)
@app.get("/")
def func(item_id: str):
    print('start func')
    time.sleep(15)
    print('end func')
    return {"item_id:", item_id}


serve.run(
    func.bind()
)