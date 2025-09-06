from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes import base
from routes.chat_route import chat_router
from routes.upload_routes import upload_base_rotue


app = FastAPI()
app.include_router(base.base_router)
app.include_router(chat_router)
app.include_router(upload_base_rotue)