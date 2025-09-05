from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes import base
from routes import chat_route


app = FastAPI()
app.include_router(base.base_router)
app.include_router(base.second_routes)
app.include_router(chat_route.chat_router)