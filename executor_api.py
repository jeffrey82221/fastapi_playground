"""
How to setup executor_api? 
pip install -r requirements.txt
uvicorn executor_api:app --port 8080

How to test it? 
python test_execution.py
"""
from ray import serve
from fastapi import FastAPI
import traceback 
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
    try:
        exec(python_func)
        print('start executing:', func_name)
        eval_str = f'{func_name}({input_str})'
        print('eval_str:', eval_str)
        assert eval(eval_str) is None, 'executing python function should return None'
        print('end executing:', func_name)
        return {"message": "success"}
    except:
        return {"message": traceback.format_exc()}


serve.run(
    execute.bind()
)