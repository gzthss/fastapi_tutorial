from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select
import uvicorn
from database import init_db, engine, get_session
from models import Item
from sqlmodel.ext.asyncio.session import AsyncSession


app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/items/{item_id}")
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Item).where(Item.id == item_id)
    result = await session.exec(query)
    item = result.one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

