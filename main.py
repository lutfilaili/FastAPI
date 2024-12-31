from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# create the object
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

items = {}

@app.post("/items/")
def create_item(item_id: int, item: Item):
    items[item_id] = item
    return {"item_id": item_id, "item": item}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return items.get(item_id, {"error": "Item not found"})

@app.put("/items/{item_id}")
def update_item(item_id: int, item:Item):
    items[item_id] = item
    return {"items_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in items:
        del items[item_id]
        return {"message": "Item deleted"}
    return {"error": "Item not found"}