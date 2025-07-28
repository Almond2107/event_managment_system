# app/main.py

from fastapi import FastAPI
from app.routers import auth
from app.routers import events, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (frontend test qilish uchun kerak bo‘ladi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend URL yozsa bo‘ladi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
