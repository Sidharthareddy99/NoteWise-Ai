from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from constants import SERVER_URL, PORT, ENV
import base64
from io import BytesIO
from utils import analyze_image
from schema import ImageData
from PIL import Image
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/calculate")
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(',')[1])
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    responses = analyze_image(image, data.dict_of_vars)
    data=[]
    for response in responses:
        data.append(response)
    print(data)
    return{
        "message" : "Image Processed Successfully",
        "type" : "success",
        "data" : data
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Get the PORT environment variable or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)

