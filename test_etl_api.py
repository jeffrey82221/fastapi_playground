"""
Testing executor_api

TODO:
- [ ] Build api that takes input and output pickle paths, and a function and do the following:
    - [ ] extract elements from pickles on input paths
    - [ ] send the elements to the function
    - [ ] get the output from function
    - [ ] save the output as pickle to the path!
    - [ ] The API takes new input:
        - {
            'python_func': python_func,
            'args_paths': input_paths,
            'kwargs_paths': kwargs_paths,
            'output_paths': output_paths,
            'is_class_method': True/False
        }
    - [ ] If 'pickle' is not in the arg of input_paths , directly takes input from
        API input
    - [ ] If 'pickle' is not in the arg of output_paths, put the result into
        the API output "return" field
- [ ] Move here the Monad class, which automatically decorate `run` method as `binded_run`
- [ ] Build a decorator (bind) that takes a function as input, and adapt it to the remote
API
    - [ ] It determine python_func via the source code of the func
    - [ ] It determine args_paths & kwargs_paths via get_path of the args & kwargs ReturnObj
    - [ ] It determine output_paths via the pre-build ReturnObjs' get_path
        - [ ] ReturnObjs of output is build according to the Return __annotations__ of the func
"""
from functools import wraps
import requests
import inspect
from textwrap import dedent
import configparser
from typing import List, Dict
config = configparser.ConfigParser()
config.read('config.ini')
URL = config.get('remote', 'url')


def call_etl_api(class_func: bool, orig_func: str, arg_names: List[str], kwarg_names: Dict[str, str], output_names: List[str]):
    python_func = dedent(inspect.getsource(orig_func))
    response = requests.get(
        'http://127.0.0.1:9999',
        params={
            'class_func': class_func,
            'python_func': python_func,
            'func_name': orig_func.__name__,
            'arg_names': arg_names,
            'kwarg_names': kwarg_names,
            'output_names': output_names
        }
    )

    assert response.status_code == 200, f'status code is {response.status_code}'
    assert response.json()['success'], response.json()['msg']
    print(response.json())


def generate_result():
    if True:
        return 'hello_world'
    else:
        pass


if __name__ == '__main__':
    call_etl_api(False, generate_result, arg_names=[], kwarg_names=dict(), output_names=['hello_str'])
