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

config = configparser.ConfigParser()
config.read('config.ini')
URL = config.get('remote', 'url')


def bind(func, is_class_method=False):
    @wraps(func)
    def wrapper():
        if is_class_method:
            python_func = dedent(inspect.getsource(func))
            input_str = '"self"'
        else:
            python_func = inspect.getsource(func)
            input_str = ''
        x = requests.get(
            URL,
            params={
                'python_func': python_func,
                'func_name': func.__name__,
                'input_str': input_str
            }
        )
        assert x.status_code == 200, f'status code is {x.status_code}'
        assert x.json()['message'] == 'success', x.json()['message']
        print('Success with response:', x.json(), 'on', func)
    return wrapper


def demo_func():
    print('Inside the function:')
    print('Hello World')
    import pandas as pd
    pd.DataFrame([1, 2, 3], columns=['number']).to_parquet('tmp.parquet')
    print('create parquet')


execute_func = bind(demo_func)


class Demo:
    def __init__(self):
        self.run = bind(self.run, is_class_method=True)

    def run(self):
        import time
        print('Inside a class method')
        print("Hello World")
        time.sleep(0.5)


if __name__ == '__main__':
    execute_func()
    demo = Demo()
    demo.run()
