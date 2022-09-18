"""
How to setup executor_api? 
pip install -r requirements.txt
uvicorn executor_api:app --port 8080

How to test it? 
python test_execution.py
"""
from ray import serve
from fastapi import FastAPI

app = FastAPI()

@serve.deployment(
    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 8,
        "target_num_ongoing_requests_per_replica": 1,
    }
)
@app.get("/")
def execute(python_func: str, func_name: str, input_str: str):
    exec(python_func)
    print('start executing:', func_name)
    eval_str = f'{func_name}({input_str})'
    print('eval_str:', eval_str)
    result = eval(eval_str)
    print('end executing:', func_name)
    return {"result": result}


serve.run(
    execute.bind()
)