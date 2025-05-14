from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return f'{item.name} {item.price}'

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

