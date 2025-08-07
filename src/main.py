from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from auth.router import router as auth_router
from router import router as api_router
from core.database import initialize_database
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await initialize_database()
        yield
    except:
        raise Exception("Failed to initialize database")

app = FastAPI(title="Inventory Management System", lifespan=lifespan)


@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)

app.include_router(auth_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
