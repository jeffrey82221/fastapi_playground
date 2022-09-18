"""
Testing executor_api
"""

def demo_func():
    print('Inside the function:')
    print('Hello World')
    return 'result_of_demo_func'


import requests
import inspect
x = requests.get(
    'http://127.0.0.1:8080',
    params={
        'python_func': inspect.getsource(demo_func),
        'func_name': demo_func.__name__
    }
)
print(x.status_code)
print(x.json())