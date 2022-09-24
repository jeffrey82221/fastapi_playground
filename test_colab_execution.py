"""
Testing executor_api
"""
from functools import wraps
import requests
import inspect
from textwrap import dedent

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
            'http://c26c-35-245-61-122.ngrok.io',
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
    print('create parquet')
    import pandas as pd
    pd.DataFrame([1, 2, 3], columns=['number']).to_parquet('tmp.parquet')
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