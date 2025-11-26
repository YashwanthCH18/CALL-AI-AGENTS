from fastapi import FastAPI
from app.routers import voice
import uvicorn

app = FastAPI(title="Voice AI Microservice")

app.include_router(voice.router)

@app.get("/")
def read_root():
    return {"message": "Voice AI Service is running"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
