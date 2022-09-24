from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# GET requests should never be used when dealing with sensitive data


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# PUT is used to send data to a server to create/update a resource.


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

# POST is also used to send data to a server to create/update a resource.
# Unlike PUT, POST is not idempotent, meaning it may change
# the state of the server.
# NOTE: But, why we are using POST in MLaaS?
#


@app.post("/items/{item_id}")
def post_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
