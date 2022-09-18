"""
Testing executor_api
"""
from functools import wraps
import requests
import inspect

def bind(func):
    @wraps(func) 
    def wrapper():
        x = requests.get(
            'http://127.0.0.1:8080',
            params={
                'python_func': inspect.getsource(func),
                'func_name': func.__name__
            }
        )
        assert x.status_code == 200
    return wrapper


def demo_func():
    print('Inside the function:')
    print('Hello World')

execute_func = bind(demo_func)

if __name__ == '__main__':
    execute_func()