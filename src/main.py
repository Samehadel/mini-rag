from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from controller import base_controller, chat_controller, upload_controller
from helper.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
import logging

app = FastAPI()
logger = logging.getLogger('uvicorn.info')

@app.on_event("startup")
async def setup_mongodb_connection():
    settings = get_settings()
    logger.info(f"Setting up MongoDB connection: \nMongoDB URL: {settings.MONGODB_URL}\nDatabase: {settings.MONGODB_DATABASE}")
    app.mongodb_connection = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb_client = app.mongodb_connection[settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def close_mongodb_connection():
    logger.info("Closing MongoDB connection")
    app.mongodb_connection.close()

app.include_router(base_controller.base_router)
app.include_router(chat_controller.chat_router)
app.include_router(upload_controller.upload_base_rotue)