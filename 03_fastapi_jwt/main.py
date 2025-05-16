from fastapi import FastAPI, HTTPException, Depends
from routers import auth
from utils.dependencies import get_current_user
from utils.schemas import TokenData
import uvicorn

app = FastAPI()

app.include_router(auth.router)



@app.get("/secure-data")
async def get_secure_data(current_user: TokenData = Depends(get_current_user)):
    """Example protected route."""
    return {
        "message": f" Hello {current_user.username}, this is sensitive data!",
        "status": "Authorized"
    }

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

