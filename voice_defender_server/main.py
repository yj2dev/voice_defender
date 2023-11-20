from fastapi.middleware.cors import CORSMiddleware
from app.routes import index, ai
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def create_app():
    app = FastAPI(title="Voice Defender API")
    origins = [
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(index.router)
    app.include_router(ai.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=int(os.getenv("PORT")),
        host=os.getenv("HOST_IP"),
        # ssl_keyfile="./key.pem",
        # ssl_certfile="./cert.pem"
    )
