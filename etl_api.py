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
from pydantic import BaseModel
from typing import *
import pickle
import logging
import json
ray.init(address='auto', ignore_reinit_error=True)
app = FastAPI()


def load(input_name):
    with open(f'/tmp/{input_name}.pickle', 'rb') as f:
        ans = pickle.load(f)
    return ans


def save(result, output_name):
    with open(f'/tmp/{output_name}.pickle', 'wb') as f:
        pickle.dump(result, f)

class Item(BaseModel):
    class_func: bool
    python_func: str
    func_name: str
    arg_names: List[str]
    kwarg_names: Dict[str, str]
    output_names: List[str]

@serve.deployment(
    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 8,
        "target_num_ongoing_requests_per_replica": 1,
    }
)
@app.post("/")
def execute(item: Item):
    input_data = json.loads(item.json())
    print('input:', input_data)
    class_func = input_data['class_func']
    python_func = input_data['python_func']
    func_name = input_data['func_name']
    arg_names = input_data['arg_names']
    kwarg_names = input_data['kwarg_names']
    output_names = input_data['output_names']
    try:
        exec(python_func)
        logging.info(python_func)
        args = []
        for name in arg_names:
            args.append(load(name))
            logging.info(f'arg {name} pickle loaded')
        kwargs = dict()
        for key, name in kwarg_names.items():
            kwargs[key] = load(name)
            logging.info(f'kwargs {key} {name} pickles loaded')
        if class_func:
            eval_str = f'{func_name}("self", *args, **kwargs)'
        else:
            eval_str = f'{func_name}(*args, **kwargs)'
        logging.info(f'eval_str: {eval_str}')
        result = eval(eval_str)
        logging.info(f'func: {func_name} executed')
        if len(output_names) == 1:
            save(result, output_names[0])
            logging.info(f'result {output_names[0]} pickle saved')
        elif len(output_names) > 1:
            results = result
            for result, output_name in zip(results, output_names):
                save(result, output_name)
                logging.info(f'result {output_name} pickle saved')
        return {"success": True, "msg": 'process success'}
    except BaseException:
        return {"success": False, "msg": traceback.format_exc()}


serve.run(
    execute.bind()
)

if __name__ == '__main__':
    import nest_asyncio
    from pyngrok import ngrok
    import uvicorn
    ngrok.set_auth_token("296zATB6WYNOnhCSqlQJYyxwTor_69pPVvPvKTrskkTva7ok")
    ngrok_tunnel = ngrok.connect(9999)
    print('Public URL:', ngrok_tunnel.public_url)
    nest_asyncio.apply()
    uvicorn.run(app, port=9999)
