# fastapi_playground
Place for studying and experimenting with FastAPI

# Install 

pip install -r requirements.txt


# Test the API

1) Run the API on terminal 

uvicorn executor_api:app --reload --host=127.0.0.1 --port=9999

2) Open the browser via localhost:9999

3) Goto the APIHub Page: localhost:9999/docs

4) Try executing the Put / Get Operation 

5) Run the apitest: 

python test_execution.py

# Run the API server on colab 

1) Open vscode on colab via https://colab.research.google.com/drive/1l5cbjum5I-qOxv_YFFVw2zfJQAyH9e2D (with Goole Drive mounted)

2) git clone and cd to this repo in Google Drive 
git clone https://github.com/jeffrey82221/fastapi_playground.git
cd fastapi_playground

3) Install python packages

python -m pip install -r requirements.txt

3) start fast api:
```bash
uvicorn executor_api:app --reload --host=127.0.0.1 --port=9999
```