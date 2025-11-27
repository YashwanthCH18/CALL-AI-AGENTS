from fastapi import FastAPI
from app.routers import voice
import uvicorn
from fastapi import FastAPI
from app.routers import voice
from mangum import Mangum

app = FastAPI()

app.include_router(voice.router)

# Lambda handler
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
