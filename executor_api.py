"""
1) How to setup executor_api?
ray start
pip install -r requirements.txt
uvicorn executor_api:app --host=127.0.0.1 --port=9999

2) How to test it?
python test_execution.py
"""
from ray import serve
from fastapi import FastAPI
import traceback
import ray
ray.init(address='auto')
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
        print('start:', func_name)
        eval_str = f'{func_name}({input_str})'
        print('eval_str:', eval_str)
        result = eval(eval_str)
        print('end:', func_name)
        return {"success": True, "result": result}
    except BaseException:
        return {"success": False, "msg": traceback.format_exc()}


serve.run(
    execute.bind()
)
