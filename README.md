# fastapi_playground
Place for studying and experimenting with FastAPI

# Install 

pip install -r requirements.txt

# Locally test the API

1) Run the API on terminal 

uvicorn executor_api:app --reload --host=127.0.0.1 --port=9999

2) Goto the APIHub Page: localhost:9999/docs

3) Run the apitest: 

python test_execution.py

# Run the API server on colab and test it locally 

1) Run the colab notebook: ColabFastAPI.ipynb

2) Replace the api url in `test_colab_execution.py` with that shown in the last cell of colab:

e.g., Colab api url: <http://c26c-35-245-61-122.ngrok.io>

3) On local terminal, execute `test_colab_execution.py`

# Run the API server on docker and port it to the internet

1) Build a image that has this api service 

2) Run the image as container and start the API inside

3) Build an router api that connect the in-container API to the outside world 
