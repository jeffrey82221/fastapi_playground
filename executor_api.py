"""
How to setup executor_api? 
pip install -r requirements.txt
uvicorn executor_api:app --port 8080

How to test it? 
python test_execution.py
"""
from ray import serve
from fastapi import FastAPI
import time

app = FastAPI()

@serve.deployment(
    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 8,
        "target_num_ongoing_requests_per_replica": 1,
    }
)
@app.get("/")
def execute(python_func: str, func_name: str):
    exec(python_func)
    print('start executing:', func_name)   
    result = eval(f'{func_name}()')
    print(result)
    print('end execution')
    return {"result": result}


serve.run(
    execute.bind()
)