from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from controller import base_controller, chat_controller, upload_controller


app = FastAPI()
app.include_router(base_controller.base_router)
app.include_router(chat_controller.chat_router)
app.include_router(upload_controller.upload_base_rotue)